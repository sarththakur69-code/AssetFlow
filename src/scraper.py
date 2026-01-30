from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import os
import time
from urllib.parse import urljoin, urlparse
from PIL import Image
from io import BytesIO
import concurrent.futures
from collections import deque

class AssetScraper:
    def __init__(self, download_folder="assets"):
        self.download_folder = download_folder
        self.options = Options()
        self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.driver = None
        self.visited_urls = set()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        # Add reliable headless options
        self.options.add_argument("--disable-dev-shm-usage")

    def _init_driver(self):
        if not self.driver:
            # Check for Streamlit Cloud / Linux environment paths
            if os.path.exists("/usr/bin/chromium") and os.path.exists("/usr/bin/chromedriver"):
                self.options.binary_location = "/usr/bin/chromium"
                service = Service("/usr/bin/chromedriver")
            else:
                # Local Windows/Mac fallback
                self.options.binary_location = None
                service = Service(ChromeDriverManager().install())
                
            self.driver = webdriver.Chrome(service=service, options=self.options)

    def scrape(self, start_url, max_pages=15, progress_callback=None):
        """
        Crawls the website starting from start_url.
        """
        self._init_driver()
        
        # 1. Scraping Phase
        if progress_callback: progress_callback(f"Starting Smart Crawl (Max {max_pages} pages)...")
        
        # Initial Selenium load for homepage (critical for JS nav)
        self.driver.get(start_url)
        self._scroll_page()
        homepage_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # Extract Fonts from homepage (best source)
        fonts = self._extract_fonts()
        
        # Queue for crawling
        queue = deque([start_url])
        self.visited_urls = {start_url}
        all_image_urls = set()
        
        # Get initial images from home
        home_imgs = self._extract_image_urls(homepage_soup, start_url)
        all_image_urls.update(home_imgs)
        
        # Get links
        links = self._extract_internal_links(homepage_soup, start_url)
        # Prioritize relevant pages
        for link in links:
            if link not in self.visited_urls:
                queue.append(link)
                self.visited_urls.add(link)
        
        # Crawl Loop (Limit concurrent pages to avoid timeouts, but use threads)
        pages_scanned = 1
        
        if progress_callback: progress_callback(f"Homepage scanned. Found {len(queue)} links. Crawling...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {}
            
            # Submit initial batch
            while queue and pages_scanned < max_pages:
                url = queue.popleft()
                future_to_url[executor.submit(self._fetch_page_fast, url)] = url
                pages_scanned += 1
                
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    soup = future.result()
                    if soup:
                        new_imgs = self._extract_image_urls(soup, url)
                        all_image_urls.update(new_imgs)
                        
                        # Add more links if we still need pages? 
                        # (Optional: for deep crawl. Skipping for speed to focus on depth 1)
                        
                        if progress_callback: 
                            progress_callback(f"Scanned: {urlparse(url).path[:20]}... ({len(all_image_urls)} assets found)")
                except Exception as e:
                    pass
                    
        # 2. Download Phase
        if progress_callback: progress_callback(f"Downloading {len(all_image_urls)} assets...")
        downloaded_paths = self._download_images_concurrent(list(all_image_urls), start_url)
        
        self.driver.quit()
        self.driver = None
        
        return downloaded_paths, fonts

    def _fetch_page_fast(self, url):
        """Fetches page using Requests (much faster than Selenium)."""
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, 'html.parser')
        except:
            return None
        return None

    def _extract_internal_links(self, soup, base_url):
        links = set()
        domain = urlparse(base_url).netloc.replace('www.', '')
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            
            # strict domain match
            if domain in parsed.netloc and parsed.scheme in ['http', 'https']:
                # Filter noise
                if any(x in parsed.path.lower() for x in ['login', 'signup', 'cart', 'account', 'policy', 'terms']):
                    continue
                # Extension filter
                if any(parsed.path.lower().endswith(ext) for ext in ['.pdf', '.zip', '.png', '.jpg']):
                    continue
                    
                links.add(full_url)
        return list(links)

    # ... [Keep existing _extract_fonts, _scroll_page, _try_get_high_res, _extract_image_urls] ...
    
    def _extract_fonts(self):
        script = """
        function getFont(selector) {
            const el = document.querySelector(selector);
            return el ? window.getComputedStyle(el).fontFamily : null;
        }
        return {
            'headers': getFont('h1') || getFont('h2') || 'Unknown',
            'body': getFont('p') || getFont('body') || 'Unknown'
        };
        """
        try:
            return self.driver.execute_script(script)
        except:
            return {'headers': 'Unknown', 'body': 'Unknown'}

    def _scroll_page(self):
        try:
            for i in range(3): # reduced scroll for speed
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * arguments[0] / 3);", i + 1)
                time.sleep(0.5)
        except: pass

    def _try_get_high_res(self, url):
        """
        Attempts to convert a thumbnail URL into a high-res URL 
        by stripping common resizing patterns.
        """
        import re
        
        # 1. Remove dimensions like 100x100, 50x50, etc.
        # e.g. image-100x100.jpg -> image.jpg
        # Expanded to catch more variants like _1024x, x1024, etc.
        new_url = re.sub(r'[-_]\d{2,}x\d*', '', url) # catch _500x, _500x500
        new_url = re.sub(r'x\d{2,}[-_]', '', new_url) # catch x500_
        
        # 2. Remove Shopify/CDN resize params and common quality reducers
        # e.g. /products/image_200x.jpg?v=123 -> /products/image.jpg?v=123
        new_url = re.sub(r'_(small|thumb|medium|large|grande|icon|square|compact|portrait|landscape|cropped|\d+x)\.', '.', new_url, flags=re.IGNORECASE)
        
        if new_url != url: return new_url
        
        # 3. Strip query params that resize
        if '?' in url:
            base, qs = url.split('?', 1)
            # If query has 'width=', 'w=', 'height=', 'h=', drop common resize params
            if any(x in qs for x in ['width=', 'w=', 'height=', 'h=', 'size=', 'quality=', 'q=']):
                # Return base url without params is usually safer for getting original
                return base 
                
        return url

    def _extract_image_urls(self, soup, base_url):
        urls = set()
        # <img> tags
        for img in soup.find_all('img'):
            # Check srcset first (usually has high-res)
            srcset = img.get('srcset') or img.get('data-srcset')
            if srcset:
                try:
                    candidates = srcset.split(',')
                    # Sort primarily by width descriptor (e.g. 1024w)
                    parsed_candidates = []
                    for c in candidates:
                        parts = c.strip().split(' ')
                        if not parts: continue
                        url_part = parts[0]
                        size_score = 0
                        if len(parts) > 1 and 'w' in parts[1]:
                             size_score = int(parts[1].replace('w', ''))
                        parsed_candidates.append((url_part, size_score))
                    
                    parsed_candidates.sort(key=lambda x: x[1])
                    best_url = parsed_candidates[-1][0]
                    urls.add(urljoin(base_url, best_url))
                except: pass

            # Fallback to src/data-src
            src = img.get('src') or img.get('data-src') or img.get('data-original')
            if src:
                full = urljoin(base_url, src)
                if full.startswith('http'): 
                    urls.add(full)
                    # Always try to "upgrade" to high-res
                    urls.add(self._try_get_high_res(full))
                
        # CSS Backgrounds
        for tag in soup.find_all(style=True):
            if 'url(' in tag['style']:
                try:
                    part = tag['style'].split('url(')[1].split(')')[0].strip('"\'')
                    full = urljoin(base_url, part)
                    urls.add(full)
                    urls.add(self._try_get_high_res(full))
                except: pass
                
        # Validation
        valid_exts = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif')
        return [u for u in urls if any(u.lower().endswith(ext) for ext in valid_exts) or 'images' in u]

    def _download_images_concurrent(self, urls, base_url):
        paths = []
        domain_name = urlparse(base_url).netloc.replace('www.', '').split('.')[0]
        save_dir = os.path.join(self.download_folder, domain_name)
        os.makedirs(save_dir, exist_ok=True)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self._download_single_image, url, save_dir, i): url for i, url in enumerate(urls)}
            
            for future in concurrent.futures.as_completed(futures):
                path = future.result()
                if path:
                    paths.append(path)
                    
        return paths

    def _download_single_image(self, url, save_dir, index):
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                # Guess extension
                ext = '.jpg'
                ct = resp.headers.get('content-type', '').lower()
                if 'png' in ct: ext = '.png'
                elif 'svg' in ct: ext = '.svg'
                elif 'webp' in ct: ext = '.webp'
                elif 'gif' in ct: ext = '.gif'
                
                filename = f"asset_{index}_{int(time.time()*1000) % 10000}{ext}"
                filepath = os.path.join(save_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(resp.content)
                
                # Check Size & Optimize
                if ext != '.svg':
                    try:
                        with Image.open(filepath) as img:
                            # 1. Prevent Blur: Reject anything smaller than 300px
                            if img.width < 300 or img.height < 300:
                                os.remove(filepath)
                                return None
                            
                            # 2. Prevent "High Quality" Bloat: Resize if too huge
                            # User requested: "Don't want high quality" (interpreted as massive file size)
                            # But "Not Blur" -> So we keep reasonable HD (e.g., 1500px)
                            if img.width > 1500 or img.height > 1500:
                                img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
                                img.save(filepath, quality=85, optimize=True) # Good quality, efficient size
                                
                    except:
                        os.remove(filepath)
                        return None
                return filepath
        except:
            pass
        return None

if __name__ == "__main__":
    s = AssetScraper()
    # s.scrape("https://example.com") 

import streamlit as st
import os
import time
from datetime import datetime
from urllib.parse import urlparse
from scraper import AssetScraper
from analysis import AssetAnalyzer
from utils import clean_filename, zip_assets
from analytics_engine import calculate_global_palette, calculate_top_tags, analyze_typography


from dotenv import load_dotenv

# Page Configuration
st.set_page_config(
    page_title="WEB SCRAPER",
    page_icon="assets/favicon.jpg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = None
if 'zip_path' not in st.session_state:
    st.session_state.zip_path = None

if 'global_stats' not in st.session_state:
    st.session_state.global_stats = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Battle Mode State
if 'battle_mode' not in st.session_state:
    st.session_state.battle_mode = False
if 'scraped_data_2' not in st.session_state:
    st.session_state.scraped_data_2 = None
if 'global_stats_2' not in st.session_state:
    st.session_state.global_stats_2 = None

# Load Custom CSS
def load_css():
    try:
        with open("src/styles.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()
def load_api_key():
    """Robustly load API key from .env file"""
    import os
    
    # 1. HARDCODED PATH FOR WINDOWS (Most reliable)
    # Using raw string for backslashes
    explicit_path = r"c:\Users\Sarth\DS004\AssetFlow\.env"
    
    if os.path.exists(explicit_path):
        try:
            with open(explicit_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for line in content.splitlines():
                    if line.strip().startswith("GEMINI_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if key: 
                            print(f"DEBUG: Found key in {explicit_path}")
                            return key
        except Exception as e:
            print(f"DEBUG: Error reading explicit path: {e}")
    else:
        print(f"DEBUG: Explicit path not found: {explicit_path}")

    # 2. Try environment variable
    key = os.getenv("GEMINI_API_KEY")
    if key and key.strip(): return key.strip()
            
    return None

api_key = load_api_key()

if not api_key:
    print("WARNING: Gemini API Key could not be loaded. AI features will be disabled.")



# Main Header
# Main Header - Hero Section
# Main Header - Hero Section
st.markdown("""
    <div style="text-align: center; padding: 4rem 0;">
        <h1 class="gradient-text animate-fade-in" style="font-size: 4rem; margin-bottom: 0.5rem;">WEB SCRAPER</h1>
        <p class="animate-fade-in" style="font-size: 1.2rem; color: #a0a0a0; font-weight: 300; animation-delay: 0.2s; opacity: 0; animation-fill-mode: forwards;">
            The Intelligent Competitor Analysis Engine
        </p>
    </div>
""", unsafe_allow_html=True)

# Input Section
with st.sidebar:
    st.header("CONFIGURATION")
    st.toggle("BATTLE MODE", key="battle_mode", help="Compare two brands side-by-side")
    st.divider()
    
    # Scan Depth Configuration
    scan_depth = st.radio(
        "SCAN DEPTH", 
        ["FAST (3 Pages)", "DEEP (15 Pages)"], 
        index=1,
        help="FAST: Quick preview. DEEP: Scans entire site (slower)."
    )
    
    # Display Scan History
    from history_manager import HistoryManager
    HistoryManager.display_history_sidebar()


# Initialize reset counter if not exists
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

# Input Section
# Input Section - Centered Focus
col_center_Input = st.columns([1, 4, 1])[1]
with col_center_Input:
    if st.session_state.battle_mode:
        url_1 = st.text_input("COMPETITOR A URL", placeholder="https://nike.com", key=f"url_input_1_{st.session_state.reset_counter}")
        url_2 = st.text_input("COMPETITOR B URL", placeholder="https://adidas.com", key=f"url_input_2_{st.session_state.reset_counter}")
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            analyze_btn = st.button("BATTLE SCAN", type="primary", use_container_width=True)
        with btn_col2:
            clear_btn = st.button("START NEW SCAN", use_container_width=True, help="Clear results and start fresh")
    else:
        url = st.text_input("ENTER TARGET URL", placeholder="https://www.nike.com", key=f"url_input_single_{st.session_state.reset_counter}")
        # Map single url to url_1 for unified logic
        url_1 = url
        url_2 = None
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            analyze_btn = st.button("SCRAPE SCAN", use_container_width=True)
        with btn_col2:
            clear_btn = st.button("START NEW SCAN", use_container_width=True, help="Clear results and start fresh")

# Handle clear button
if 'clear_btn' in locals() and clear_btn:
    # Clear all session state
    keys_to_clear = ['scraped_data', 'scraped_data_2', 'global_stats', 'global_stats_2', 'zip_path', 'messages']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    # Increment reset counter to force new input widgets with empty values
    st.session_state.reset_counter += 1
    
    st.success("**Results and URLs cleared! Ready for a new scan.**")
    st.rerun()




if analyze_btn:
    if not url_1:
         st.error("**Please enter a URL**")
         st.info("**Example:** `https://www.nike.com` or `https://adidas.com`")
    elif st.session_state.battle_mode and not url_2:
         st.error("**Battle Mode requires two URLs**")
         st.info("Enter both **Competitor A** and **Competitor B** URLs to compare.")
    elif not url_1.startswith(('http://', 'https://')):
         st.error("**Invalid URL format**")
         st.info("URL must start with `http://` or `https://`")
    else:
         status_text = st.empty()
         progress_bar = st.progress(0)
         
         # --- SKELETON UI (Dynamic) ---
         skeleton_placeholder = st.empty()
         with skeleton_placeholder.container():
            if st.session_state.battle_mode:
                # BATTLE MODE SKELETON (Two Columns)
                st.markdown("""
                <div class="skeleton-grid-2">
                    <div>
                        <div class="skeleton skeleton-title" style="width: 40%;"></div>
                        <div class="skeleton skeleton-card" style="height: 300px;"></div>
                        <div class="skeleton skeleton-text" style="margin-top: 10px;"></div>
                        <div class="skeleton skeleton-text" style="width: 80%;"></div>
                    </div>
                    <div>
                        <div class="skeleton skeleton-title" style="width: 40%;"></div>
                        <div class="skeleton skeleton-card" style="height: 300px;"></div>
                        <div class="skeleton skeleton-text" style="margin-top: 10px;"></div>
                        <div class="skeleton skeleton-text" style="width: 80%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # NORMAL MODE SKELETON (Gallery + Stats)
                st.markdown("""
                <div style="display: flex; gap: 20px; margin-bottom: 20px;">
                    <div class="skeleton skeleton-card" style="width: 70%; height: 400px;"></div>
                    <div class="skeleton skeleton-card" style="width: 30%; height: 400px;"></div>
                </div>
                <div class="skeleton-grid-3">
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                </div>
                """, unsafe_allow_html=True)
         # -------------------
         
         try:
            # Initialize engines
            scraper = AssetScraper(download_folder="assets")
            analyzer = AssetAnalyzer(api_key=api_key)
            
            # --- SCAN LOGIC URL 1 ---
            status_text.text(f"Scanning Target A: {url_1}...")
            # Determine pages based on selection
            pages_limit = 3 if "FAST" in scan_depth else 15
            
            # 1. Scrape A
            try:
                image_paths_1, fonts_1 = scraper.scrape(url_1, max_pages=pages_limit, progress_callback=lambda m: status_text.text(f"Target A: {m}"))
            except Exception as e:
                st.error(f"❌ Failed to reach Target A ({url_1})")
                st.warning(f"Connection Error: {e}")
                st.info("💡 Tip: Check if the URL is correct and accessible.")
                skeleton_placeholder.empty()
                st.stop()
            
            if not image_paths_1:
                st.error(f"Target A ({url_1}) returned no assets.")
                st.stop()
                
            progress_bar.progress(30)
            
            # 2. Analyze A
            status_text.text("Analyzing Assets A...")
            
            def update_progress_a(current, total, msg):
                status_text.text(msg)
                # Map 0-100% of analysis to 30-50% of total bar
                p = 0.3 + (0.2 * (current / total))
                progress_bar.progress(min(p, 0.5))

            analyzed_data_1 = analyzer.analyze_batch(image_paths_1, progress_callback=update_progress_a)
            
            # FIX: Properly construct dictionary for A
            palette_1 = calculate_global_palette(analyzed_data_1)
            tags_1 = calculate_top_tags(analyzed_data_1)
            typo_1 = analyze_typography(fonts_1)

            global_stats_1 = {
                "palette": palette_1,
                "top_tags": tags_1,
                "typography": typo_1
            }
            
            # --- SCAN LOGIC URL 2 (Battle) ---
            if st.session_state.battle_mode and url_2:
                progress_bar.progress(50)
                status_text.text(f"Scanning Target B: {url_2}...")
                
                # 1. Scrape B
                try:
                    image_paths_2, fonts_2 = scraper.scrape(url_2, max_pages=pages_limit, progress_callback=lambda m: status_text.text(f"Target B: {m}"))
                except Exception as e:
                    st.error(f"❌ Failed to reach Target B ({url_2})")
                    st.warning(f"Connection Error: {e}")
                    st.info("💡 Tip: Check if the URL is correct and accessible.")
                    skeleton_placeholder.empty()
                    st.stop()
                
                if not image_paths_2:
                    st.error(f"Target B ({url_2}) returned no assets.")
                    st.stop()
                
                # 2. Analyze B
                status_text.text("Analyzing Assets B...")
                
                def update_progress_b(current, total, msg):
                    status_text.text(msg)
                    # Map 0-100% of analysis B to 70-90% of total bar (assuming A is done)
                    # Actually B starts at 50%
                    p = 0.5 + (0.4 * (current / total))
                    progress_bar.progress(min(p, 0.9))

                analyzed_data_2 = analyzer.analyze_batch(image_paths_2, progress_callback=update_progress_b)
                
                # FIX: Properly construct dictionary for B
                palette_2 = calculate_global_palette(analyzed_data_2)
                tags_2 = calculate_top_tags(analyzed_data_2)
                typo_2 = analyze_typography(fonts_2)
                
                global_stats_2 = {
                    "palette": palette_2,
                    "top_tags": tags_2,
                    "typography": typo_2
                }
                
                # Save State B
                st.session_state.scraped_data_2 = analyzed_data_2
                st.session_state.global_stats_2 = global_stats_2
            
            # Finalize State A (Primary)
            st.session_state.scraped_data = analyzed_data_1
            st.session_state.global_stats = global_stats_1
            st.session_state.scanned_url = url_1  # Save URL for PDF export
            
            # Save URL 2 if battle mode
            if st.session_state.battle_mode and url_2:
                st.session_state.scanned_url_2 = url_2
            
            # Save to history (for non-battle mode, only if scan succeeded)
            if not st.session_state.battle_mode and st.session_state.get('scraped_data'):
                from history_manager import HistoryManager
                HistoryManager.save_scan(url_1, None, is_battle=False)
            
            
            # Zip A (standard)
            # Fix: pass directory path, not list of files
            if image_paths_1:
                zip_file = zip_assets(os.path.dirname(image_paths_1[0]), "brand_assets")
            else:
                zip_file = None
            
            st.session_state.zip_path = zip_file
            
            st.session_state.messages = [] 
            
            # Save to history (only if scan succeeded)
            # Save to history (only if scan succeeded)
            from history_manager import HistoryManager
            if st.session_state.get('scraped_data') and st.session_state.get('scraped_data_2'):
                HistoryManager.save_scan(url_1, url_2, is_battle=True)
                
                # --- PRE-GENERATE REPORTS FOR ONE-CLICK DOWNLOAD ---
                try:
                    # 1. Generate PDF
                    from export_engine import PDFReportGenerator
                    pdf_gen = PDFReportGenerator()
                    
                    data1 = {
                        'url': url_1,
                        'images': st.session_state.scraped_data,
                        'fonts': st.session_state.global_stats.get('fonts', []),
                        'colors': st.session_state.global_stats.get('palette', []),
                        'vibe': st.session_state.global_stats.get('vibe', {})
                    }
                    data2 = {
                        'url': url_2,
                        'images': st.session_state.scraped_data_2,
                        'fonts': st.session_state.global_stats_2.get('fonts', []),
                        'colors': st.session_state.global_stats_2.get('palette', []),
                        'vibe': st.session_state.global_stats_2.get('vibe', {})
                    }
                    
                    pdf_filename = f"web_scraper_battle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    pdf_gen.generate_battle_report(data1, data2, pdf_filename)
                    
                    with open(pdf_filename, "rb") as f:
                        st.session_state.battle_pdf_bytes = f.read()
                    os.remove(pdf_filename)
                    
                    # 2. Generate CSV ZIP
                    from export_engine import CSVExporter
                    import zipfile
                    csv_exp = CSVExporter()
                    
                    zip_filename = f"web_scraper_battle_csv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                    with zipfile.ZipFile(zip_filename, 'w') as zipf:
                        # Brand A
                        csv_exp.export_assets(st.session_state.scraped_data, "brand_a_assets.csv")
                        csv_exp.export_global_stats(st.session_state.global_stats, "brand_a_stats.csv")
                        zipf.write("brand_a_assets.csv")
                        zipf.write("brand_a_stats.csv")
                        os.remove("brand_a_assets.csv")
                        os.remove("brand_a_stats.csv")
                        
                        # Brand B
                        csv_exp.export_assets(st.session_state.scraped_data_2, "brand_b_assets.csv")
                        csv_exp.export_global_stats(st.session_state.global_stats_2, "brand_b_stats.csv")
                        zipf.write("brand_b_assets.csv")
                        zipf.write("brand_b_stats.csv")
                        os.remove("brand_b_assets.csv")
                        os.remove("brand_b_stats.csv")
                        
                    with open(zip_filename, "rb") as f:
                        st.session_state.battle_csv_bytes = f.read()
                    os.remove(zip_filename)
                    
                except Exception as e:
                    print(f"Error pre-generating reports: {e}")
            
            skeleton_placeholder.empty()
            progress_bar.progress(100)
            status_text.text(">> BATTLE COMPLETE")
            time.sleep(1)
            st.rerun()
            
         except Exception as e:
            import traceback
            st.error(f"CRITICAL ERROR: {str(e)}")
            st.code(traceback.format_exc())

# Results Dashboard
if st.session_state.scraped_data:
    st.markdown("---")
    
    # ---------------------------
    # BATTLE MODE DASHBOARD
    # ---------------------------
    if st.session_state.battle_mode and st.session_state.scraped_data_2:
        st.subheader("BATTLE MODE ARENA")
        
        # Export Buttons for Battle Mode
        export_col1, export_col2, export_col3 = st.columns([1, 1, 2])
        
        # 1. PDF EXPORT
        with export_col1:
            if 'battle_pdf_bytes' in st.session_state:
                # ONE-CLICK DOWNLOAD
                st.download_button(
                    label="Download Battle Report (PDF)",
                    data=st.session_state.battle_pdf_bytes,
                    file_name=f"web_scraper_battle_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                # Fallback for old scans
                if st.button("Generate Battle Report (PDF)", use_container_width=True):
                    with st.spinner("Generating PDF report..."):
                        try:
                            from export_engine import PDFReportGenerator
                            generator = PDFReportGenerator()
                            
                            data1 = {
                                'url': st.session_state.get('scanned_url', 'Unknown'),
                                'images': st.session_state.scraped_data,
                                'fonts': st.session_state.global_stats.get('fonts', []),
                                'colors': st.session_state.global_stats.get('palette', []),
                                'vibe': st.session_state.global_stats.get('vibe', {})
                            }
                            data2 = {
                                'url': st.session_state.get('scanned_url_2', 'Unknown'),
                                'images': st.session_state.scraped_data_2,
                                'fonts': st.session_state.global_stats_2.get('fonts', []),
                                'colors': st.session_state.global_stats_2.get('palette', []),
                                'vibe': st.session_state.global_stats_2.get('vibe', {})
                            }
                            
                            pdf_path = f"web_scraper_battle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                            generator.generate_battle_report(data1, data2, pdf_path)
                            
                            with open(pdf_path, 'rb') as f:
                                st.session_state.battle_pdf_bytes = f.read()
                            os.remove(pdf_path)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Generation Failed: {str(e)}")

        # 2. CSV EXPORT
        with export_col2:
            if 'battle_csv_bytes' in st.session_state:
                # ONE-CLICK DOWNLOAD
                st.download_button(
                    label="Download Battle Data (CSV)",
                    data=st.session_state.battle_csv_bytes,
                    file_name="web_scraper_battle_data.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            else:
                # Fallback
                if st.button("Generate CSV Data", use_container_width=True):
                    try:
                        from export_engine import CSVExporter
                        import zipfile
                        exporter = CSVExporter()
                        
                        zip_path = f"battle_data.zip"
                        with zipfile.ZipFile(zip_path, 'w') as zipf:
                            exporter.export_assets(st.session_state.scraped_data, "brand_a.csv")
                            zipf.write("brand_a.csv")
                            os.remove("brand_a.csv")
                            
                            exporter.export_assets(st.session_state.scraped_data_2, "brand_b.csv")
                            zipf.write("brand_b.csv")
                            os.remove("brand_b.csv")
                            
                        with open(zip_path, "rb") as f:
                            st.session_state.battle_csv_bytes = f.read()
                        os.remove(zip_path)
                        st.rerun()
                    except Exception as e:
                        st.error(f"CSV Error: {e}")

        st.divider()
        
        # Main Split
        col_a, col_b = st.columns(2)
        
        # --- LEFT: BRAND A ---
        with col_a:
            st.markdown(f"### BRAND A: {urlparse(url_1).netloc if url_1 else 'Brand A'}")
            
            # A Stats
            stats_a = st.session_state.global_stats
            if stats_a:
                # Vibe Check A
                if 'vibe' not in stats_a:
                     with st.spinner("Analyzing Vibe A..."):
                        try:
                            v = analyzer.analyze_vibe([t['tag'] for t in stats_a['top_tags']], stats_a['palette'])
                            import json
                            stats_a['vibe'] = json.loads(v.replace("```json", "").replace("```", ""))
                        except: pass
                
                if 'vibe' in stats_a:
                    v = stats_a['vibe']
                    st.info(f"**Vibe:** {', '.join(v.get('vibe_keywords', []))}  \n**Score:** {v.get('personality_score')}")

                # Palette A
                pal_html = "".join([f'<div style="background-color:{c}; width:25px; height:25px; display:inline-block; margin-right:4px; border-radius:4px;" title="{c}"></div>' for c in stats_a['palette']])
                st.markdown(f"**Palette:** {pal_html}", unsafe_allow_html=True)
                
                # Tags A
                tags = ", ".join([t['tag'] for t in stats_a['top_tags'][:5]])
                st.markdown(f"**Themes:** {tags}")
                
                # Typo A
                typo = stats_a.get('typography', {})
                st.markdown(f"**Fonts:** H: {typo.get('headers', 'N/A')} | P: {typo.get('body', 'N/A')}")
            
            st.divider()
            st.markdown("#### ASSETS (TOP 6)")
            # Gallery A
            cols_a_gal = st.columns(2)
            for i, item in enumerate(st.session_state.scraped_data[:6]):
                with cols_a_gal[i % 2]:
                     st.image(item['path'], use_container_width=True)
                     if item.get('colors'):
                        c_html = "".join([f'<span style="background:{c};width:15px;height:15px;display:inline-block;margin-right:2px;border-radius:50%;"></span>' for c in item['colors']])
                        st.markdown(f"<div style='margin-top:5px'>{c_html}</div>", unsafe_allow_html=True)

        # --- RIGHT: BRAND B ---
        with col_b:
            st.markdown(f"### BRAND B: {urlparse(url_2).netloc if url_2 else 'Brand B'}")
            
            # B Stats
            stats_b = st.session_state.global_stats_2
            if stats_b:
                 # Vibe Check B
                if 'vibe' not in stats_b:
                     with st.spinner("Analyzing Vibe B..."):
                        try:
                            v = analyzer.analyze_vibe([t['tag'] for t in stats_b['top_tags']], stats_b['palette'])
                            import json
                            stats_b['vibe'] = json.loads(v.replace("```json", "").replace("```", ""))
                        except: pass
                
                if 'vibe' in stats_b:
                    v = stats_b['vibe']
                    st.success(f"**Vibe:** {', '.join(v.get('vibe_keywords', []))}  \n**Score:** {v.get('personality_score')}")

                # Palette B
                pal_html_2 = "".join([f'<div style="background-color:{c}; width:25px; height:25px; display:inline-block; margin-right:4px; border-radius:4px;" title="{c}"></div>' for c in stats_b['palette']])
                st.markdown(f"**Palette:** {pal_html_2}", unsafe_allow_html=True)
                
                # Tags B
                tags_2 = ", ".join([t['tag'] for t in stats_b['top_tags'][:5]])
                st.markdown(f"**Themes:** {tags_2}")
                
                # Typo B
                typo_2 = stats_b.get('typography', {})
                st.markdown(f"**Fonts:** H: {typo_2.get('headers', 'N/A')} | P: {typo_2.get('body', 'N/A')}")

            st.divider()
            st.markdown("#### ASSETS (TOP 6)")
            # Gallery B
            cols_b_gal = st.columns(2)
            for i, item in enumerate(st.session_state.scraped_data_2[:6]):
                with cols_b_gal[i % 2]:
                     st.image(item['path'], use_container_width=True)
                     if item.get('colors'):
                        c_html = "".join([f'<span style="background:{c};width:15px;height:15px;display:inline-block;margin-right:2px;border-radius:50%;"></span>' for c in item['colors']])
                        st.markdown(f"<div style='margin-top:5px'>{c_html}</div>", unsafe_allow_html=True)

    # ---------------------------
    # STANDARD SINGLE DASHBOARD
    # ---------------------------
    else:

        
        
        # --- 3D ASSET ORBIT (PREMIUM HEADER) ---
        if 'scraped_data' in st.session_state and st.session_state.scraped_data:
            from orbit_component import get_orbit_html
            import streamlit.components.v1 as components
            
            
            # Filter valid images
            img_list = [item['path'] for item in st.session_state.scraped_data if os.path.exists(item['path'])]
            if img_list:
                orbit_html = get_orbit_html(img_list)
                components.html(orbit_html, height=450)
                st.divider()

        res_col1, res_col2 = st.columns([3, 1])
        with res_col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("BRAND DNA")
            
            if st.session_state.global_stats:
                
                # --- AI VIBE CHECK ---
                if 'vibe' not in st.session_state.global_stats:
                    # Trigger analysis if key exists
                    with st.spinner("Analyzing Brand Personality..."):
                        try:
                            top_tags = [t['tag'] for t in st.session_state.global_stats.get('top_tags', [])]
                            palette = st.session_state.global_stats.get('palette', [])
                            vibe = analyzer.analyze_vibe(top_tags, palette)
                            if vibe:
                                import json
                                clean_json = vibe.replace("```json", "").replace("```", "")
                                st.session_state.global_stats['vibe'] = json.loads(clean_json)
                        except Exception as e:
                            print(f"Vibe Error: {e}")

                # Color Palette, Themes, and Typography
                dna_cols = st.columns(3)
                
                with dna_cols[0]:
                    st.markdown("**OFFICIAL BRAND PALETTE**")
                    pal = st.session_state.global_stats.get('palette', [])
                    palette_html = "".join([f'<div style="background-color:{c}; width:40px; height:40px; display:inline-block; margin-right:5px; border-radius:5px;" title="{c}"></div>' for c in pal])
                    st.markdown(f"<div>{palette_html}</div>", unsafe_allow_html=True)
                    
                with dna_cols[1]:
                    st.markdown("**KEY VISUAL THEMES**")
                    
                    # 1. AI Vibe (if available)
                    if 'vibe' in st.session_state.global_stats:
                        vibe = st.session_state.global_stats['vibe']
                        
                        # Score Badge
                        st.caption(f"**Personality:** {vibe.get('personality_score', 'N/A')}")
                        
                        # Vibe Keywords
                        kw_html = "".join([f"<span style='background: #00f3ff; color: #000; padding: 2px 8px; margin-right: 5px; border-radius: 4px; font-weight: bold; font-size: 0.8em;'>{k}</span>" for k in vibe.get('vibe_keywords', [])])
                        st.markdown(f"<div style='margin-bottom: 8px;'>{kw_html}</div>", unsafe_allow_html=True)
                    
                    # 2. Tags
                    tags = st.session_state.global_stats.get('top_tags', [])
                    tags_html = "".join([f'<span style="background-color: #333; color: white; padding: 4px 8px; border-radius: 4px; margin-right: 5px; margin-bottom: 5px; display: inline-block;">{t["tag"]}</span>' for t in tags[:5]])
                    st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
                
                with dna_cols[2]:
                    st.markdown("**TYPOGRAPHY**")
                    type_data = st.session_state.global_stats.get('typography', {})
                    st.markdown(f"**Headers:** {type_data.get('headers', 'N/A')}")
                    st.markdown(f"**Body:** {type_data.get('body', 'N/A')}")
                
                
                st.markdown('</div>', unsafe_allow_html=True)
                # Removed divider line here as requested

            st.subheader("ASSET INTELLIGENCE GRID")
            
            # Display Gallery
            cols = st.columns(3)
            for idx, item in enumerate(st.session_state.scraped_data):
                with cols[idx % 3]:
                    st.image(item['path'], use_container_width=True)
                    
                    # Tags
                    if item['tags']:
                        st.caption(f"{', '.join(item['tags'][:3])}")
                    
                    # Colors
                    if item['colors']:
                        color_html = "".join([f'<span style="background-color:{c}; width:20px; height:20px; display:inline-block; margin-right:5px; border-radius:50%;"></span>' for c in item['colors']])
                        st.markdown(f"<div>{color_html}</div>", unsafe_allow_html=True)
                    st.markdown("---")

        with res_col2:
            # Mood Board Generator (removed duplicate OPERATIONS section)
            # Mood Board Generator
            if st.session_state.scraped_data:
                
                if st.button("GENERATE MOOD BOARD", use_container_width=True):
                    with st.spinner("Designing Mood Board..."):
                        from moodboard import MoodBoardGenerator
                        generator = MoodBoardGenerator(output_folder="assets")
                        
                        # Gather data
                        top_images = [item['path'] for item in st.session_state.scraped_data if os.path.exists(item['path'])]
                        palette = st.session_state.global_stats.get('palette', [])
                        # brand_name = urlparse(url).netloc.replace('www.', '').split('.')[0] if url else "brand"
                        brand_name = "Brand A"
                        
                        # Generate
                        board_path = generator.generate(top_images, palette, brand_name)
                        st.session_state.moodboard_path = board_path
                        st.success("Mood Board Created!")

                # Show C for Mood Board
                if 'moodboard_path' in st.session_state and st.session_state.moodboard_path:
                    st.image(st.session_state.moodboard_path, caption="Auto-Generated Brand Board", use_container_width=True)
                    with open(st.session_state.moodboard_path, "rb") as fp:
                        st.download_button(
                            label="DOWNLOAD MOOD BOARD (JPG)",
                            data=fp,
                            file_name=os.path.basename(st.session_state.moodboard_path),
                            mime="image/jpeg",
                            use_container_width=True
                        )

                
            # Zip Download
            if st.session_state.zip_path:
                try:
                    with open(st.session_state.zip_path, "rb") as fp:
                        st.download_button(
                            label="DOWNLOAD RAW ASSETS (ZIP)",
                            data=fp,
                            file_name=os.path.basename(st.session_state.zip_path),
                            mime="application/zip",
                            use_container_width=True
                        )
                except Exception:
                     st.caption("Zip gen failed")
            
            
            # PDF Export - ONE CLICK DOWNLOAD
            if st.session_state.get('scraped_data'):
                try:
                    from export_engine import PDFReportGenerator
                    from datetime import datetime
                    import io
                    
                    # Generate PDF in memory
                    def generate_pdf():
                        generator = PDFReportGenerator()
                        data = {
                            'url': st.session_state.get('scanned_url', 'Unknown'),
                            'images': st.session_state.scraped_data if st.session_state.scraped_data else [],
                            'fonts': st.session_state.global_stats.get('fonts', []) if st.session_state.global_stats else [],
                            'colors': st.session_state.global_stats.get('palette', []) if st.session_state.global_stats else [],
                            'vibe': st.session_state.global_stats.get('vibe', {}) if st.session_state.global_stats else {}
                        }
                        pdf_path = f"assetflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        generator.generate_normal_report(data, pdf_path)
                        with open(pdf_path, 'rb') as f:
                            pdf_data = f.read()
                        os.remove(pdf_path)
                        return pdf_data
                    
                    st.download_button(
                        label=" Download Report (PDF)",
                        data=generate_pdf(),
                        file_name=f"assetflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f" PDF generation failed: {str(e)}")
            
            # CSV Export - ONE CLICK DOWNLOAD
            if st.session_state.get('scraped_data'):
                try:
                    from export_engine import CSVExporter
                    from datetime import datetime
                    import zipfile
                    import io
                    
                    # Generate CSV ZIP in memory
                    def generate_csv_zip():
                        exporter = CSVExporter()
                        zip_path = f"assetflow_csv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                        
                        with zipfile.ZipFile(zip_path, 'w') as zipf:
                            # SUMMARY CSV (NEW - Most Important!)
                            csv_summary = "summary_report.csv"
                            exporter.export_summary(
                                st.session_state.get('scanned_url', 'Unknown'),
                                st.session_state.global_stats,
                                csv_summary
                            )
                            zipf.write(csv_summary)
                            os.remove(csv_summary)
                            
                            # Assets CSV
                            csv_assets = "assets.csv"
                            exporter.export_assets(st.session_state.scraped_data, csv_assets)
                            zipf.write(csv_assets)
                            os.remove(csv_assets)
                            
                            # Fonts CSV
                            if st.session_state.global_stats and st.session_state.global_stats.get('fonts'):
                                csv_fonts = "fonts.csv"
                                exporter.export_fonts(st.session_state.global_stats['fonts'], csv_fonts)
                                zipf.write(csv_fonts)
                                os.remove(csv_fonts)
                            
                            # Colors CSV
                            if st.session_state.global_stats and st.session_state.global_stats.get('palette'):
                                csv_colors = "colors.csv"
                                exporter.export_colors(st.session_state.global_stats['palette'], csv_colors)
                                zipf.write(csv_colors)
                                os.remove(csv_colors)
                        
                        with open(zip_path, 'rb') as f:
                            zip_data = f.read()
                        os.remove(zip_path)
                        return zip_data
                    
                    st.download_button(
                        label="Export Data (CSV)",
                        data=generate_csv_zip(),
                        file_name=f"assetflow_csv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"CSV export failed: {str(e)}")
            
            


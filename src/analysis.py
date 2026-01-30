from colorthief import ColorThief
import google.generativeai as genai
import os
from PIL import Image

class AssetAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key
        print(f"DEBUG: AssetAnalyzer initialized with key: {str(self.api_key)[:5]}... (Type: {type(self.api_key)})")
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("DEBUG: Gemini Model Configured Successfully")
            except Exception as e:
                print(f"DEBUG: Gemini Configuration Failed: {e}")
                self.model = None
        else:
            print("DEBUG: No API Key provided to AssetAnalyzer")
            self.model = None

    def get_dominant_colors(self, image_path, count=5):
        """
        Extracts dominant colors from an image.
        Returns a list of hex color codes.
        """
        try:
            if image_path.endswith('.svg'):
                return [] # ColorThief doesn't support SVG
                
            color_thief = ColorThief(image_path)
            palette = color_thief.get_palette(color_count=count)
            # Convert RGB to Hex
            return ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in palette]
        except Exception as e:
            print(f"Color extraction failed for {image_path}: {e}")
            return []

    def generate_tags(self, image_path):
        """
        Uses Gemini to generate tags for the image.
        """
        if not self.model or not self.api_key:
            return ["AI Not Configured"]
            
        try:
            if image_path.endswith('.svg'):
                return ["Vector Graphic"] 
                
            img = Image.open(image_path)
            prompt = "Analyze this image and provide 3-5 short, relevant tags describing the subject matter, style, and visual elements. Return them as a comma-separated list."
            response = self.model.generate_content([prompt, img])
            return [tag.strip() for tag in response.text.split(',')]
        except Exception as e:
            error_msg = str(e)
            print(f"AI tagging failed for {image_path}: {error_msg}")
            # Return a short error for the UI
            if "403" in error_msg:
                return ["Error: Invalid API Key"]
            elif "429" in error_msg:
                return ["Error: Rate Limit"]
            else:
                return [f"Error: {error_msg[:20]}..."]

    def analyze_batch(self, image_paths, progress_callback=None):
        results = []
        total = len(image_paths)
        
        for i, path in enumerate(image_paths):
            if progress_callback:
                progress_callback(i + 1, total, f"Analyzing asset {i+1}/{total}...")
                
            colors = self.get_dominant_colors(path)
            tags = self.generate_tags(path)
            
            results.append({
                "path": path,
                "filename": os.path.basename(path),
                "colors": colors,
                "tags": tags
            })
            
        return results

    def analyze_vibe(self, tags, palette):
        """
        Generates a 'Vibe Check' for the brand based on aggregated data.
        """
        if not self.model:
            return None
            
        try:
            # Construct a prompt for high-level analysis
            prompt = f"""
            You are a Brand Strategist. Analyze these visual elements:
            
            Top Visual Tags: {', '.join(tags[:15])}
            Dominant Colors (Hex): {', '.join(palette[:5])}
            
            Task:
            1. Describe the brand's 'Vibe' in exactly 3 adjectives.
            2. Give a 'Personality Score' in the format "Trait: X/10". Choose a trait relevant to the vibe (e.g., Luxury, Playfulness, Minimalism, Aggression).
            3. Write a 1-sentence explanation.
            
            Output strictly as valid JSON:
            {{
                "vibe_keywords": ["Adj1", "Adj2", "Adj3"],
                "personality_score": "Trait: X/10",
                "explanation": "..."
            }}
            """
            
            response = self.model.generate_content(prompt)
            # Simple cleaning in case of markdown blocks
            text = response.text.replace('```json', '').replace('```', '').strip()
            return text
        except Exception as e:
            print(f"Vibe check failed: {e}")
            return None

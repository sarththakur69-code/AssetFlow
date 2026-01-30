from PIL import Image, ImageDraw, ImageFont
import os

class MoodBoardGenerator:
    def __init__(self, output_folder="assets"):
        self.output_folder = output_folder
        self.width = 3840 # 4K Resolution
        self.height = 2160
        self.background_color = (20, 20, 20) # Dark theme background

    def generate(self, image_paths, palette, brand_name):
        """
        Generates a mood board collage from images and palette.
        """
        # Create canvas
        canvas = Image.new('RGB', (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(canvas)
        
        # --- 1. Layout Images (Grid Logic) ---
        # We will take up to 6 images and arrange them on the left 2/3rds
        # Grid: 2 columns, 3 rows (approx) or 3x2
        
        padding = 20
        work_area_width = int(self.width * 0.70)
        col_width = (work_area_width - (3 * padding)) // 2
        row_height = (self.height - (4 * padding)) // 3
        
        images_to_use = image_paths[:6] # Top 6 images
        
        current_x = padding
        current_y = padding
        
        for i, img_path in enumerate(images_to_use):
            try:
                with Image.open(img_path) as img:
                    # Resize to fit the grid cell (Crop to fill)
                    img = self._resize_and_crop(img, col_width, row_height)
                    canvas.paste(img, (current_x, current_y))
                    
                    # Move cursor
                    if i % 2 == 1: # End of row (2 cols)
                        current_x = padding
                        current_y += row_height + padding
                    else:
                        current_x += col_width + padding
            except Exception as e:
                print(f"Failed to load image for moodboard: {e}")

        # --- 2. Right Sidebar (Branding & Palette) ---
        sidebar_x = work_area_width + padding
        sidebar_w = self.width - sidebar_x - padding
        
        # A. Brand Name
        # Since we don't have custom fonts easily guaranteed, use default but large
        # Or try to load a system font. For robustness, we'll draw text manually.
        
        # We'll calculate text size roughly or just place it
        draw.text((sidebar_x, padding + 50), brand_name.upper(), fill="white", font_size=80)
        draw.text((sidebar_x, padding + 150), "MOOD BOARD // 2026", fill="#666666", font_size=30)
        
        # B. Color Palette Swatches
        swatch_y = padding + 300
        swatch_height = 80
        
        for hex_color in palette:
            # Draw rectangle
            rgb = self._hex_to_rgb(hex_color)
            draw.rectangle(
                [sidebar_x, swatch_y, sidebar_x + sidebar_w, swatch_y + swatch_height], 
                fill=rgb
            )
            # Draw hex code text
            # Determine contrast text color
            lum = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
            text_color = "black" if lum > 128 else "white"
            
            draw.text(
                (sidebar_x + 20, swatch_y + 25), 
                hex_color, 
                fill=text_color,
                font_size=30
            )
            
            swatch_y += swatch_height + 15 # Gap
            
        # Save
        filename = f"{brand_name}_moodboard.jpg"
        save_path = os.path.join(self.output_folder, filename)
        canvas.save(save_path, quality=100, subsampling=0) # Max quality
        
        return save_path

    def _resize_and_crop(self, img, target_w, target_h):
        """
        Resizes and center crops an image to fit target dimensions.
        """
        img_ratio = img.width / img.height
        target_ratio = target_w / target_h
        
        if img_ratio > target_ratio:
            # Image is wider than target -> Resize based on height
            new_h = target_h
            new_w = int(new_h * img_ratio)
        else:
            # Image is taller/square -> Resize based on width
            new_w = target_w
            new_h = int(new_w / img_ratio)
            
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Center Crop
        left = (new_w - target_w) / 2
        top = (new_h - target_h) / 2
        right = (new_w + target_w) / 2
        bottom = (new_h + target_h) / 2
        
        return img.crop((left, top, right, bottom))
    
    def _hex_to_rgb(self, hex_val):
        hex_val = hex_val.lstrip('#')
        return tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))

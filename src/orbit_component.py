import streamlit as st
import base64

def get_orbit_html(image_paths, height=400):
    """
    Generates a 3D CSS Orbit Carousel.
    """
    
    # We need to serve local images or encode them if they are local paths
    # For Streamlit, local paths outside static folder is tricky in HTML.
    # We will base64 encode the images to ensure they display.
    
    encoded_images = []
    import os
    
    # Limit to top 12 images for performance and aesthetics
    target_images = [img for img in image_paths if os.path.exists(img)][:12]
    
    if not target_images:
        return "<div>No images for 3D Orbit</div>"

    for path in target_images:
        try:
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                ext = "png" if path.endswith(".png") else "jpeg"
                encoded_images.append(f"data:image/{ext};base64,{encoded_string}")
        except: pass
        
    num_images = len(encoded_images)
    if num_images == 0: return ""
    
    # Angle calculation
    angle_step = 360 / num_images
    translate_z = 300 + (num_images * 20) # Push out based on count
    
    cards_html = ""
    for i, img_src in enumerate(encoded_images):
        rotation = i * angle_step
        cards_html += f"""
        <div class="orbit-item" style="transform: rotateY({rotation}deg) translateZ({translate_z}px);">
            <img src="{img_src}" />
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; overflow: hidden; background: transparent; display: flex; justify-content: center; align-items: center; height: {height}px; perspective: 1000px; }}
        
        .scene {{
            width: 200px;
            height: 150px;
            position: relative;
            transform-style: preserve-3d;
            animation: spin 30s infinite linear;
            cursor: grab;
        }}
        
        .scene:active {{
            cursor: grabbing;
            animation-play-state: paused;
        }}
        
        .orbit-item {{
            position: absolute;
            width: 200px;
            height: 150px;
            left: 0;
            top: 0;
            border: 2px solid #00f3ff;
            background: rgba(0,0,0,0.8);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.3);
            transition: transform 0.3s;
        }}
        
        .orbit-item img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        @keyframes spin {{
            from {{ transform: rotateY(0deg); }}
            to {{ transform: rotateY(360deg); }}
        }}
        
        /* Interactive Hover Pause */
        .scene:hover {{
            animation-play-state: paused;
        }}
        
    </style>
    </head>
    <body>
        <div class="scene" id="scene">
            {cards_html}
        </div>
        
        <script>
            const scene = document.getElementById('scene');
            let isDragging = false;
            let startX, currentRotation = 0;
            
            document.addEventListener('mousedown', (e) => {{
                isDragging = true;
                startX = e.clientX;
                scene.style.animation = 'none'; // Kill auto transform to take manual control
            }});
            
            document.addEventListener('mouseup', () => {{
                isDragging = false;
                scene.style.animation = 'spin 30s infinite linear'; // Resume (optional, or keep static)
            }});
            
            document.addEventListener('mousemove', (e) => {{
                if (!isDragging) return;
                const dx = e.clientX - startX;
                // Add logic for manual rotation if needed, 
                // but simple CSS hover pause is usually smoother for basic integration without complex JS state.
            }});
        </script>
    </body>
    </html>
    """
    return html

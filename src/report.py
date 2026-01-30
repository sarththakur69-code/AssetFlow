from fpdf import FPDF
import os
from datetime import datetime

class BrandReportPDF(FPDF):
    def header(self):
        # Logo/Title
        self.set_font('Arial', 'B', 15)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, 'WebScraper // Competitor Intelligence', 0, 1, 'R')
        self.line(10, 20, 200, 20)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_brand_report(target_url, global_stats, scraped_data, output_folder="assets"):
    pdf = BrandReportPDF()
    pdf.add_page()
    
    # 1. Cover Section
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 20, 'BRAND AUDIT REPORT', 0, 1, 'L')
    
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Target: {target_url}", 0, 1, 'L')
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'L')
    pdf.ln(10)
    
    # 2. Brand DNA (Global Palette)
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, '1. Brand DNA (Dominant Colors)', 0, 1, 'L')
    pdf.ln(5)
    
    colors = global_stats.get('palette', [])
    if colors:
        start_x = pdf.get_x()
        y = pdf.get_y()
        for i, color_hex in enumerate(colors):
            # Draw color box
            r = int(color_hex[1:3], 16)
            g = int(color_hex[3:5], 16)
            b = int(color_hex[5:7], 16)
            
            pdf.set_fill_color(r, g, b)
            pdf.rect(start_x + (i * 35), y, 30, 30, 'F')
            
            # Label
            pdf.set_xy(start_x + (i * 35), y + 32)
            pdf.set_font('Arial', '', 9)
            pdf.cell(30, 5, color_hex, 0, 0, 'C')
            
        pdf.set_xy(start_x, y + 45)
    else:
        pdf.cell(0, 10, "No color data available.", 0, 1)
        
    pdf.ln(10)
    
    # 3. Key Themes (Top Tags)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '2. Key Visual Themes', 0, 1, 'L')
    pdf.ln(5)
    
    tags = global_stats.get('top_tags', [])
    if tags:
        pdf.set_font('Arial', '', 11)
        # formatted list
        tag_str = ", ".join([f"{t['tag']} ({t['count']})" for t in tags])
        pdf.multi_cell(0, 8, tag_str)
    else:
        pdf.cell(0, 10, "No tag data available.", 0, 1)
        
    pdf.ln(10)
    
    # 3. Typography
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '3. Corporate Typography', 0, 1, 'L')
    pdf.ln(5)
    
    type_data = global_stats.get('typography', {})
    pdf.set_font('Arial', '', 11)
    if type_data:
        pdf.cell(0, 8, f"Header Font: {type_data.get('headers', 'N/A')}", 0, 1)
        pdf.cell(0, 8, f"Body Font: {type_data.get('body', 'N/A')}", 0, 1)
    else:
        pdf.cell(0, 8, "Typography data unavailable", 0, 1)
        
    pdf.ln(15)
    
    # 4. Asset Highlights
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '4. Asset Highlights', 0, 1, 'L')
    pdf.ln(5)
    
    # Grid of top images (limit to 4 for PDF cleanliness)
    top_assets = scraped_data[:4]
    
    x_start = 10
    y_start = pdf.get_y()
    
    for i, asset in enumerate(top_assets):
        if i % 2 == 0:
            x = x_start
            if i > 0: y_start += 90 
        else:
            x = x_start + 95
            
        # Check page break
        if y_start > 250:
            pdf.add_page()
            y_start = 20
        
        try:
            # Add Image
            # basic check to ensure we only include supported image types in PDF (jpg/png)
            ext = os.path.splitext(asset['path'])[1].lower()
            if ext in ['.jpg', '.jpeg', '.png']:
                pdf.image(asset['path'], x, y_start, w=90)
            
            # Caption
            pdf.set_xy(x, y_start + 65) # approximate height of image if aspect ratio was handled, simplifying here
            if asset.get('tags'):
                pdf.set_font('Arial', 'I', 8)
                tags_short = ", ".join(asset['tags'][:3])
                pdf.cell(90, 5, tags_short[:50] + "...", 0, 0, 'C')
                
        except Exception as e:
            print(f"Error adding image to PDF: {e}")
            
    # Output
    domain = target_url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
    filename = f"{domain}_brand_report.pdf"
    output_path = os.path.join(output_folder, filename)
    pdf.output(output_path)
    
    return output_path

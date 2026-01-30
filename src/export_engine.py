"""
PDF Report Generator for AssetFlow
Generates comprehensive competitor analysis reports in PDF format.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io
import os
from PIL import Image as PILImage

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#00f3ff'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#00f3ff'),
            spaceAfter=12,
            spaceBefore=20
        )
    
    def generate_normal_report(self, data, output_path):
        """
        Generate detailed PDF report for normal scan mode.
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        story = []
        
        # --- STYLES ---
        # Professional Colors
        primary_color = colors.HexColor('#0e1117') # Dark background essentially
        accent_color = colors.HexColor('#00f3ff') # Brand Cyan
        text_color = colors.HexColor('#333333')
        light_gray = colors.HexColor('#f0f2f6')
        
        # Custom Paragraph Styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.black,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.gray,
            spaceAfter=40,
            alignment=TA_CENTER
        )
        
        section_header = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.black,
            spaceBefore=20,
            spaceAfter=10,
            allowWidows=0,
            borderPadding=(0, 0, 5, 0),
            borderWidth=0,
            fontName='Helvetica-Bold'
        )
        
        normal_text = ParagraphStyle(
            'NormalText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=text_color,
            spaceAfter=12
        )

        # --- CONTENT GENERATION ---
        
        # 1. HEADER
        story.append(Paragraph("WEB SCRAPER", subtitle_style))
        story.append(Paragraph("Scrape & Analyze Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # 2. SCAN METADATA TABLE
        # Clean clean data
        target_url = data.get('url', 'N/A')
        scan_date = datetime.now().strftime('%B %d, %Y')
        img_count = str(len(data.get('images', [])))
        font_count = str(len(data.get('fonts', [])))
        
        meta_data = [
            ['TARGET URL', target_url],
            ['SCAN DATE', scan_date],
            ['ASSETS FOUND', f"{img_count} Images"],
            ['TYPOGRAPHY', f"{font_count} Fonts Detected"]
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 4.5*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), light_gray),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.3*inch))
        
        # 3. AI VIBE ANALYSIS (If available)
        if 'vibe' in data:
            story.append(Paragraph("BRAND PERSONALITY (AI ANALYSIS)", section_header))
            
            vibe_text = data['vibe'].get('description', 'No analysis available.')
            score = data['vibe'].get('score', 'N/A')
            
            # Box-like container for vibe
            vibe_data = [[
                Paragraph(f"<b>Vibe Score: {score}/10</b><br/><br/>{vibe_text}", normal_text)
            ]]
            vibe_table = Table(vibe_data, colWidths=[6.5*inch])
            vibe_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#b3e5fc')),
                ('PADDING', (0, 0), (-1, -1), 12),
            ]))
            story.append(vibe_table)
            story.append(Spacer(1, 0.2*inch))

        # 4. COLOR PALETTE (Grid Layout)
        if 'colors' in data and data['colors']:
            story.append(Paragraph("DOMINANT COLOR PALETTE", section_header))
            
            # Helper to create swatch
            def create_swatch(hex_code):
                return Table([['', hex_code]], colWidths=[0.5*inch, 1*inch], rowHeights=[0.5*inch])

            # Prepare data row by row (5 colors per row)
            color_row = []
            palette_table_data = []
            
            valid_colors = [c for c in data['colors'] if c.startswith('#')][:10]
            
            for color in valid_colors:
                try:
                    # Create a mini table for each color cell: [Color Block] [Hex Text]
                    # Actually better: Just a cell with background color, and text below it?
                    # Let's do a table where row 1 is colors, row 2 is text
                    pass 
                except: continue

            # Let's stick to a simpler clean list for stability
            # Row 1: Swatches
            # Row 2: Hex Codes
            
            swatch_row = []
            hex_row = []
            
            for color in valid_colors[:5]: # Top 5
                swatch_row.append('') # Empty content, just background
                hex_row.append(color)
            
            # Create table
            if swatch_row:
                p_data = [swatch_row, hex_row]
                p_table = Table(p_data, colWidths=[1.2*inch]*5, rowHeights=[0.6*inch, 0.3*inch])
                
                # Dynamic styles for backgrounds
                styles = [
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('FONTNAME', (0,1), (-1,1), 'Helvetica'),
                    ('FONTSIZE', (0,1), (-1,1), 8),
                    ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
                    ('GRID', (0,0), (-1,-1), 0, colors.white) # No grid lines
                ]
                
                for i, col in enumerate(valid_colors[:5]):
                    styles.append(('BACKGROUND', (i, 0), (i, 0), colors.HexColor(col)))
                
                p_table.setStyle(TableStyle(styles))
                story.append(p_table)
            
            story.append(Spacer(1, 0.2*inch))

        
        # 5. VISUAL ASSET GALLERY
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("SELECTED ASSETS", section_header))
        
        if 'images' in data and data['images']:
            img_grid = []
            row = []
            
            possible_images = [img for img in data['images'] if img.get('path') and os.path.exists(img.get('path'))]
            
            for i, img in enumerate(possible_images[:6]):
                try:
                    img_path = img['path']
                    # Maintain Aspect Ratio logic
                    with PILImage.open(img_path) as pil_img:
                        w, h = pil_img.size
                        aspect = h / float(w)
                    
                    target_w = 2.8 * inch # Slightly smaller for grid
                    target_h = target_w * aspect
                    if target_h > 2.0 * inch:
                        target_h = 2.0 * inch
                        target_w = target_h / aspect
                        
                    report_img = Image(img_path, width=target_w, height=target_h)
                    
                    # Caption
                    fname = os.path.basename(img_path)
                    if len(fname) > 20: fname = fname[:17] + "..."
                    caption = Paragraph(f"{fname}", normal_text)
                    
                    cell_content = [report_img, Spacer(1, 5), caption]
                    row.append(cell_content)
                    
                    if len(row) == 2:
                        img_grid.append(row)
                        row = []
                except:
                    continue
            
            if row:
                row.append([])
                img_grid.append(row)
            
            if img_grid:
                gallery_tbl = Table(img_grid, colWidths=[3.25*inch, 3.25*inch])
                gallery_tbl.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('LEFTPADDING', (0,0), (-1,-1), 10),
                    ('RIGHTPADDING', (0,0), (-1,-1), 10),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 20),
                ]))
                story.append(gallery_tbl)

        # 6. RAW DATA LIST
        story.append(PageBreak())
        story.append(Paragraph("Detailed Asset Inventory", section_header))
        
        asset_rows = [['Index', 'Filename', 'Resolution', 'Type']]
        for i, img in enumerate(data['images'][:40], 1):
             fname = os.path.basename(img.get('path', 'Unknown'))
             if len(fname) > 35: fname = fname[:32] + "..."
             res = img.get('resolution', '-')
             ftype = fname.split('.')[-1].upper() if '.' in fname else 'IMG'
             
             asset_rows.append([str(i), fname, res, ftype])
        
        detail_tbl = Table(asset_rows, colWidths=[0.5*inch, 3.5*inch, 1.5*inch, 1*inch])
        detail_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#333333')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f9f9')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(detail_tbl)

        # BUILD
        try:
            doc.build(story)
        except Exception as e:
            print(f"PDF Build Error: {e}")
            # Simplified fallback
            simple = SimpleDocTemplate(output_path)
            simple.build([Paragraph(f"Critical Error: {e}", self.styles['Normal'])])
    
    def generate_battle_report(self, data1, data2, output_path):
        """
        Generate Detailed Professional Battle Report (Side-by-Side).
        """
        doc = SimpleDocTemplate(output_path, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        story = []
        
        # --- STYLES (MATCHING NORMAL REPORT) ---
        title_style = ParagraphStyle('Title', parent=self.styles['Heading1'], fontSize=24, textColor=colors.black, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=20)
        subtitle_style = ParagraphStyle('Subtitle', parent=self.styles['Normal'], fontSize=12, textColor=colors.gray, alignment=TA_CENTER, spaceAfter=40)
        section_header = ParagraphStyle('SectionHeader', parent=self.styles['Heading2'], fontSize=16, textColor=colors.black, spaceBefore=20, spaceAfter=15, fontName='Helvetica-Bold')
        normal_style = ParagraphStyle('Normal', parent=self.styles['Normal'], fontSize=10, textColor=colors.HexColor('#333333'))
        
        # 1. HEADER
        story.append(Paragraph("WEB SCRAPER", subtitle_style))
        story.append(Paragraph("Competitive Analysis Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # 2. COMPARISON MATRIX (METADATA)
        story.append(Paragraph("1. Executive Summary", section_header))
        
        comp_data = [
            ['Metric', 'COMPETITOR A', 'COMPETITOR B'],
            ['Target URL', Paragraph(data1.get('url', 'N/A'), normal_style), Paragraph(data2.get('url', 'N/A'), normal_style)],
            ['Scan Date', datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d')],
            ['Assets Found', str(len(data1.get('images', []))), str(len(data2.get('images', [])))],
            ['Fonts Detect', str(len(data1.get('fonts', []))), str(len(data2.get('fonts', [])))]
        ]
        
        t = Table(comp_data, colWidths=[2*inch, 4*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f2f6')), # Light Gray Header
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('PADDING', (0,0), (-1,-1), 12),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.3*inch))
        
        # 3. VISUAL DNA (COLORS)
        story.append(Paragraph("2. Visual DNA Comparison", section_header))
        
        # Helper for Color Grids
        def render_palette_row(colors_list):
            cells = []
            for c in colors_list[:5]:
                try:
                    cells.append(Table([['', c]], colWidths=[0.3*inch, 0.8*inch], style=[
                        ('BACKGROUND', (0,0), (0,0), colors.HexColor(c)),
                        ('BOX', (0,0), (0,0), 0.5, colors.grey),
                        ('FONTSIZE', (1,0), (1,0), 8),
                        ('ALIGN', (1,0), (1,0), 'LEFT'),
                        ('VALIGN', (1,0), (1,0), 'MIDDLE'),
                        ('LEFTPADDING', (1,0), (1,0), 5),
                    ]))
                except: pass
            return cells

        # Color Table
        pal1 = render_palette_row(data1.get('colors', []))
        pal2 = render_palette_row(data2.get('colors', []))
        
        # Determine max length for table
        # We'll just show up to 5 side-by-side
        
        color_rows = [['Start', 'Competitor A Palette', 'Competitor B Palette']]
        
        # Construct a table that holds the sub-tables
        # A simple way: row 1 is A, row 2 is B
        
        c_table_data = [
            ['Competitor A', Table([pal1], colWidths=[1.2*inch]*len(pal1))],
            ['Competitor B', Table([pal2], colWidths=[1.2*inch]*len(pal2))]
        ]
        
        ct = Table(c_table_data, colWidths=[2*inch, 8*inch])
        ct.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('PADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ]))
        story.append(ct)
        story.append(Spacer(1, 0.3*inch))
        
        # 4. ASSET GALLERY SIDE-BY-SIDE
        story.append(Paragraph("3. Asset Comparison Gallery", section_header))
        
        imgs1 = [img['path'] for img in data1.get('images', []) if os.path.exists(img.get('path', ''))][:4]
        imgs2 = [img['path'] for img in data2.get('images', []) if os.path.exists(img.get('path', ''))][:4]
        
        # Create rows of 2 images (1 from A, 1 from B)
        
        gal_data = [['Competitor A (Top Assets)', 'Competitor B (Top Assets)']]
        
        for i in range(4):
            row = []
            # Image A
            if i < len(imgs1):
                try:
                    img = Image(imgs1[i])
                    aspect = img.imageWidth / float(img.imageHeight)
                    display_width = 3.5*inch
                    display_height = display_width / aspect
                    if display_height > 2.5*inch: # Cap height
                        display_height = 2.5*inch
                        display_width = display_height * aspect
                    row.append(Image(imgs1[i], width=display_width, height=display_height))
                except: row.append("Error loading image")
            else:
                row.append("-")
                
            # Image B
            if i < len(imgs2):
                try:
                    img = Image(imgs2[i])
                    aspect = img.imageWidth / float(img.imageHeight)
                    display_width = 3.5*inch
                    display_height = display_width / aspect
                    if display_height > 2.5*inch: # Cap height
                        display_height = 2.5*inch
                        display_width = display_height * aspect
                    row.append(Image(imgs2[i], width=display_width, height=display_height))
                except: row.append("Error loading image")
            else:
                row.append("-")
            
            gal_data.append(row)
            
        gt = Table(gal_data, colWidths=[5*inch, 5*inch])
        gt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f2f6')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('padding', (0,0), (-1,-1), 10),
        ]))
        story.append(gt)

        # BUILD
        try:
            doc.build(story)
        except Exception as e:
            print(f"Battle PDF Error: {e}")



class CSVExporter:
    """Export scan data to CSV format"""
    
    def export_summary(self, url, global_stats, output_path):
        """Export comprehensive scan summary to CSV"""
        import csv
        from datetime import datetime
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['AssetFlow Scan Summary Report'])
            writer.writerow(['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            # Basic Info
            writer.writerow(['SCAN INFORMATION'])
            writer.writerow(['Target URL', url])
            writer.writerow(['Total Images', len(global_stats.get('images', []))])
            writer.writerow(['Total Fonts', len(global_stats.get('fonts', []))])
            writer.writerow(['Total Colors', len(global_stats.get('palette', []))])
            writer.writerow([])
            
            # Typography
            writer.writerow(['TYPOGRAPHY'])
            typo = global_stats.get('typography', {})
            writer.writerow(['Header Font', typo.get('headers', 'N/A')])
            writer.writerow(['Body Font', typo.get('body', 'N/A')])
            writer.writerow([])
            
            # AI Vibe (if available)
            if 'vibe' in global_stats and global_stats['vibe']:
                writer.writerow(['AI VIBE ANALYSIS'])
                vibe = global_stats['vibe']
                writer.writerow(['Brand Personality', vibe.get('description', 'N/A')])
                writer.writerow(['Confidence Score', f"{vibe.get('score', 0)}/10"])
                
                # Vibe keywords
                keywords = vibe.get('vibe_keywords', [])
                if keywords:
                    writer.writerow(['Vibe Keywords', ', '.join(keywords)])
                
                writer.writerow(['Explanation', vibe.get('explanation', 'N/A')])
                writer.writerow([])
            
            # Top Themes
            writer.writerow(['TOP VISUAL THEMES'])
            writer.writerow(['Theme', 'Frequency'])
            for tag in global_stats.get('top_tags', [])[:10]:
                writer.writerow([tag.get('tag', ''), tag.get('count', 0)])
            writer.writerow([])
            
            # Color Palette
            writer.writerow(['BRAND COLOR PALETTE'])
            writer.writerow(['Index', 'Hex Color'])
            for i, color in enumerate(global_stats.get('palette', [])[:10], 1):
                writer.writerow([i, color])
        
        return output_path
    
    def export_assets(self, images, output_path):
        """Export comprehensive image asset data to CSV"""
        import csv
        import os
        from PIL import Image as PILImage
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header with all comprehensive fields
            writer.writerow([
                'Asset #',
                'Filename', 
                'File Type',
                'File Size (KB)',
                'Dimensions (W x H)',
                'Aspect Ratio',
                'Source URL',
                'Dominant Colors',
                'AI Tags',
                'Primary Theme'
            ])
            
            for i, img in enumerate(images, 1):
                # Basic info
                path = img.get('path', '')
                filename = img.get('filename', os.path.basename(path) if path else 'Unknown')
                url = img.get('url', 'N/A')
                
                # File type
                file_ext = os.path.splitext(filename)[1].upper().replace('.', '') if filename else 'Unknown'
                
                # File size
                try:
                    file_size = os.path.getsize(path) / 1024 if path and os.path.exists(path) else 0
                    file_size_str = f"{file_size:.1f}" if file_size > 0 else "N/A"
                except:
                    file_size_str = "N/A"
                
                # Dimensions and aspect ratio
                try:
                    if path and os.path.exists(path) and not path.endswith('.svg'):
                        with PILImage.open(path) as pil_img:
                            width, height = pil_img.size
                            dimensions = f"{width} x {height}"
                            
                            # Calculate aspect ratio
                            gcd_val = self._gcd(width, height)
                            aspect_ratio = f"{width//gcd_val}:{height//gcd_val}"
                    else:
                        dimensions = "N/A"
                        aspect_ratio = "N/A"
                except:
                    dimensions = "N/A"
                    aspect_ratio = "N/A"
                
                # Colors
                colors = img.get('colors', [])
                if colors and isinstance(colors, list):
                    # Clean hex codes
                    clean_colors = [c for c in colors if isinstance(c, str) and c.startswith('#')]
                    colors_str = ', '.join(clean_colors[:5]) if clean_colors else 'N/A'
                else:
                    colors_str = 'N/A'
                
                # Tags & Theme - SANITIZED
                tags = img.get('tags', [])
                clean_tags = []
                if tags and isinstance(tags, list):
                    for t in tags:
                        # Filter out error messages from being dumped into CSV
                        if isinstance(t, str) and not t.lower().startswith(('error:', 'ai not configured')):
                            clean_tags.append(t)
                
                if clean_tags:
                    tags_str = ', '.join(clean_tags)
                    primary_theme = clean_tags[0]
                else:
                    # Check if we had an error to report nicely
                    raw_tags = img.get('tags', [])
                    if raw_tags and isinstance(raw_tags, list) and any('error' in str(t).lower() for t in raw_tags):
                        tags_str = "Analysis Failed"
                        primary_theme = "N/A"
                    elif raw_tags and isinstance(raw_tags, list) and any('configured' in str(t).lower() for t in raw_tags):
                         tags_str = "AI Not Enabled"
                         primary_theme = "N/A"
                    else:
                        tags_str = "N/A"
                        primary_theme = "N/A"
                
                # Write row
                writer.writerow([
                    i,
                    filename,
                    file_ext,
                    file_size_str,
                    dimensions,
                    aspect_ratio,
                    url,
                    colors_str,
                    tags_str,
                    primary_theme
                ])
        
        return output_path
    
    def _gcd(self, a, b):
        """Calculate Greatest Common Divisor for aspect ratio"""
        while b:
            a, b = b, a % b
        return a
    
    def export_fonts(self, fonts, output_path):
        """Export font data to CSV"""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'Font Family'])
            
            for i, font in enumerate(fonts, 1):
                writer.writerow([i, font])
        
        return output_path
    
    def export_colors(self, colors, output_path):
        """Export color palette to CSV"""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'Hex Color'])
            
            for i, color in enumerate(colors, 1):
                writer.writerow([i, color])
        
        return output_path

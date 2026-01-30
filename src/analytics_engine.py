from collections import Counter

def calculate_global_palette(scraped_data, top_n=5):
    """
    Aggregates all colors from scraped data and returns the top N most frequent global colors.
    """
    if not scraped_data:
        return []
        
    all_colors = []
    for item in scraped_data:
        if item.get('colors'):
            all_colors.extend(item['colors'])
            
    # Simple frequency count
    # In a more advanced version, we might cluster similar colors
    return [color for color, count in Counter(all_colors).most_common(top_n)]

def calculate_top_tags(scraped_data, top_n=10):
    """
    Aggregates all tags and returns the most frequent ones to identify brand themes.
    """
    if not scraped_data:
        return []
        
    all_tags = []
    for item in scraped_data:
        if item.get('tags'):
            # Filter out error messages if any slipped through
            valid_tags = [t for t in item['tags'] if not t.lower().startswith('error')]
            all_tags.extend(valid_tags)
            
    return [{"tag": tag, "count": count} for tag, count in Counter(all_tags).most_common(top_n)]

def analyze_typography(fonts):
    """
    Cleans up font strings.
    """
    if not fonts: return {}
    
    clean_fonts = {}
    for key, value in fonts.items():
        if value:
            # Remove quotes and extra spaces
            clean_fonts[key] = value.replace('"', '').replace("'", "")
        else:
            clean_fonts[key] = "Not Detected"
            
    return clean_fonts

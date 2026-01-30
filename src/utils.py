import os
import shutil
import re

def clean_filename(url):
    """
    Sanitizes a URL to be a valid folder name.
    """
    clean = re.sub(r'^https?://', '', url)
    clean = re.sub(r'www\.', '', clean)
    clean = re.sub(r'[^a-zA-Z0-9]', '_', clean)
    return clean[:50]  # Limit length

def zip_assets(folder_path, output_path):
    """
    Zips a directory.
    """
    shutil.make_archive(output_path, 'zip', folder_path)
    return f"{output_path}.zip"

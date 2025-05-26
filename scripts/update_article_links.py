#!/usr/bin/env python3
"""
Update existing HTML pages to link to new combined PDF+Text pages
"""

import os
import re
from pathlib import Path

def update_links_in_file(file_path):
    """Update PDF links to point to combined pages"""
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all links to PDFs in scans folder
    # Pattern: href="scans/filename.pdf"
    pattern = r'href="scans/([^"]+\.pdf)"'
    
    def replace_link(match):
        pdf_filename = match.group(1)
        # Extract filename without extension
        base_name = pdf_filename.rsplit('.', 1)[0]
        # Return new link to articles folder
        return f'href="articles/{base_name}.html"'
    
    # Replace all PDF links
    updated_content = re.sub(pattern, replace_link, content, flags=re.IGNORECASE)
    
    # Also update links that might have ../scans/ format
    pattern2 = r'href="../scans/([^"]+\.pdf)"'
    
    def replace_link2(match):
        pdf_filename = match.group(1)
        base_name = pdf_filename.rsplit('.', 1)[0]
        return f'href="../articles/{base_name}.html"'
    
    updated_content = re.sub(pattern2, replace_link2, updated_content, flags=re.IGNORECASE)
    
    # Write back if changes were made
    if updated_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return True
    return False

def main():
    """Update all HTML files"""
    
    base_dir = Path(__file__).parent.parent
    
    print("Updating links to point to combined PDF+Text pages...")
    
    # Get all HTML files
    html_files = list(base_dir.glob('*.htm')) + list(base_dir.glob('*.html'))
    
    updated_count = 0
    for html_file in html_files:
        if 'articles' not in str(html_file):  # Skip articles folder
            if update_links_in_file(html_file):
                print(f"Updated: {html_file.name}")
                updated_count += 1
    
    print(f"\nUpdated {updated_count} files")

if __name__ == "__main__":
    main()
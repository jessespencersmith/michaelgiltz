#!/usr/bin/env python3
"""
Fix remaining extracted_content links and convert them to articles links
"""

import os
import re
from pathlib import Path

def fix_links_in_file(file_path):
    """Fix all remaining extracted_content links"""
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0
    
    changes = 0
    
    # Replace extracted_content links with articles links
    def replace_extracted_link(match):
        nonlocal changes
        original = match.group(0)
        path = match.group(1)
        
        # Replace extracted_content with articles
        new_path = path.replace('extracted_content/', 'articles/')
        new_href = f'href="{new_path}"'
        changes += 1
        return new_href
    
    # Update the content
    updated_content = re.sub(r'href="(extracted_content/[^"]+)"', replace_extracted_link, content)
    
    # Write back if changes were made
    if changes > 0:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Fixed {file_path}: {changes} links updated")
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return 0
    
    return changes

def main():
    """Fix all HTML files in the GiltzWeb 2 directory"""
    
    base_dir = Path('/Users/spencejb/Documents/GiltzWeb 2')
    
    # Get all HTML files
    html_files = list(base_dir.glob('*.htm')) + list(base_dir.glob('*.html'))
    
    total_changes = 0
    
    print("Fixing remaining extracted_content links...")
    print("=" * 50)
    
    for html_file in html_files:
        if html_file.name not in ['search.php', 'template.htm']:
            changes = fix_links_in_file(html_file)
            total_changes += changes
    
    print("=" * 50)
    print(f"Total fixes: {total_changes} links updated")

if __name__ == "__main__":
    main()
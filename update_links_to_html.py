#!/usr/bin/env python3
"""
Update all links in HTML files from .pdf to .html
This updates links to point to the new combined HTML pages instead of direct PDF links
"""

import os
import re
from pathlib import Path

def update_links_in_file(file_path):
    """Update all PDF links to HTML links in a file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0
    
    # Count changes before modifying
    pdf_links = re.findall(r'href="([^"]*\.pdf)"', content, re.IGNORECASE)
    changes = 0
    
    # Replace PDF links with HTML links
    # Pattern matches href="...scans/filename.pdf" and converts to href="articles/filename.html"
    def replace_pdf_link(match):
        nonlocal changes
        original = match.group(0)
        href_part = match.group(1)
        
        # Extract just the filename from the path
        filename = os.path.basename(href_part)
        if filename.endswith('.pdf'):
            # Change extension from .pdf to .html
            new_filename = filename[:-4] + '.html'
            # Point to articles directory
            new_href = f'href="articles/{new_filename}"'
            changes += 1
            return new_href
        
        return original
    
    # Update the content
    updated_content = re.sub(r'href="[^"]*scans/([^"]+\.pdf)"', replace_pdf_link, content, flags=re.IGNORECASE)
    
    # Also handle links that might not have 'scans/' in the path
    def replace_direct_pdf_link(match):
        nonlocal changes
        original = match.group(0)
        href_part = match.group(1)
        
        # Skip if it's already pointing to articles/ or if it's a full URL
        if 'articles/' in href_part or href_part.startswith('http'):
            return original
            
        # Only process if it's a PDF file
        if href_part.endswith('.pdf'):
            # Extract just the filename
            filename = os.path.basename(href_part)
            # Change extension from .pdf to .html
            new_filename = filename[:-4] + '.html'
            # Point to articles directory
            new_href = f'href="articles/{new_filename}"'
            changes += 1
            return new_href
        
        return original
    
    # Second pass for direct PDF links without 'scans/' path
    updated_content = re.sub(r'href="([^"]+\.pdf)"', replace_direct_pdf_link, updated_content, flags=re.IGNORECASE)
    
    # Write back if changes were made
    if changes > 0:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated {file_path}: {changes} links changed")
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return 0
    
    return changes

def main():
    """Update all HTML files in the GiltzWeb 2 directory"""
    
    base_dir = Path('/Users/spencejb/Documents/GiltzWeb 2')
    
    # HTML files to update
    html_files = [
        'index.htm',
        'AMERICAblog.htm',
        'About.htm',
        'Advocate.htm',
        'Alligator.htm',
        'BBC_Portfolio.htm',
        'BookFilter.htm',
        'Bookandfilmglobe.htm',
        'Books.htm',
        'BroadwayDirect.htm',
        'CDReview.htm',
        'Contact.htm',
        'DVDs.htm',
        'EntertainmentWeekly.htm',
        'Fired.htm',
        'Flowers_Portfolio.htm',
        'Fox_Portfolio.htm',
        'General.htm',
        'HuffingtonPost.htm',
        'IRAAwards.htm',
        'LATimes.htm',
        'Lists.htm',
        'Misc.htm',
        'Movies.htm',
        'Music.htm',
        'MyFavoriteThings.htm',
        'MyFirstTime.htm',
        'NYDailyNews.htm',
        'NYPost.htm',
        'NewYork.htm',
        'Parade.htm',
        'People.htm',
        'Politics.htm',
        'Popsurfing.htm',
        'Premiere.htm',
        'Sports.htm',
        'TV.htm',
        'TheIRAs.htm',
        'TheLists.htm',
        'Theater.htm'
    ]
    
    total_changes = 0
    
    print("Updating links in HTML files...")
    print("=" * 50)
    
    for html_file in html_files:
        file_path = base_dir / html_file
        if file_path.exists():
            changes = update_links_in_file(file_path)
            total_changes += changes
        else:
            print(f"File not found: {html_file}")
    
    print("=" * 50)
    print(f"Total updates: {total_changes} links changed")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Update article lists while preserving existing article HTML links
This replaces the functionality of UpdateArticles.py but maintains compatibility
with the new combined PDF+Text article system
"""

import os
import glob
import re
from datetime import datetime

def parse_filename(filename):
    """Parse a PDF filename into its components"""
    # Remove extension
    rawinfo = filename.rstrip(".pdf")
    try:
        pub, title, month, day, year = rawinfo.split("-")
        return {
            'publication': pub,
            'title': title.replace("_", " "),
            'month': int(month),
            'day': int(day),
            'year': int(year),
            'filename': filename
        }
    except ValueError:
        return None

def get_existing_articles(html_file):
    """Extract existing article links from an HTML file"""
    existing_articles = {}
    
    if not os.path.exists(html_file):
        return existing_articles
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all article links
    article_pattern = r'<a href="articles/([^"]+)\.html">([^<]+)</a>'
    for match in re.finditer(article_pattern, content):
        filename_base = match.group(1)
        link_text = match.group(2)
        # Map PDF name to article HTML
        pdf_name = filename_base + '.pdf'
        existing_articles[pdf_name] = {
            'html_file': filename_base + '.html',
            'link_text': link_text
        }
    
    return existing_articles

def update_publication_page(pub_file, articles):
    """Update a publication page with article links"""
    if not os.path.exists(pub_file):
        print(f"Warning: {pub_file} not found")
        return
    
    with open(pub_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get existing article mappings
    existing_articles = get_existing_articles(pub_file)
    
    # Find the list section
    pattern = r'(<!-- list:[^>]+>)(.*?)(<!-- /list -->)'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"Warning: No list section found in {pub_file}")
        return
    
    # Build new list content
    new_list = []
    for article in articles:
        pdf_name = article['filename']
        
        # Check if we have an HTML version
        if pdf_name in existing_articles:
            # Use the existing HTML link
            html_file = existing_articles[pdf_name]['html_file']
            link_text = existing_articles[pdf_name]['link_text']
            link = f'<a href="articles/{html_file}">{link_text}</a>'
        else:
            # Check if HTML file exists in articles directory
            html_name = pdf_name.replace('.pdf', '.html')
            if os.path.exists(f'articles/{html_name}'):
                # Link to the HTML version
                link_text = article['title']
                date_str = f"{article['month']}/{article['day']}/{article['year']}"
                link = f'<a href="articles/{html_name}">{link_text}</a> - {date_str}'
            else:
                # Fall back to PDF link
                link_text = article['title']
                date_str = f"{article['month']}/{article['day']}/{article['year']}"
                link = f'<a href="scans/{pdf_name}">{link_text}</a> - {date_str}'
        
        new_list.append(f'<br />\n{link}')
    
    # Replace the content
    new_content = match.group(1) + '\n' + '\n'.join(new_list) + '\n' + match.group(3)
    content = content[:match.start()] + new_content + content[match.end():]
    
    # Write back
    with open(pub_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {pub_file}: {len(articles)} articles")

def main():
    print("=" * 60)
    print("Update Article Lists (Preserving HTML Links)")
    print("=" * 60)
    
    # Get all PDFs
    pdf_files = glob.glob("scans/*.pdf")
    print(f"\nFound {len(pdf_files)} PDFs")
    
    # Parse and organize by publication
    publications = {}
    
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        article = parse_filename(filename)
        
        if article:
            pub = article['publication']
            if pub not in publications:
                publications[pub] = []
            publications[pub].append(article)
    
    # Sort articles by date (newest first)
    for pub in publications:
        publications[pub].sort(
            key=lambda x: (x['year'], x['month'], x['day']),
            reverse=True
        )
    
    # Update each publication page
    print(f"\nUpdating {len(publications)} publication pages...")
    
    for pub, articles in publications.items():
        pub_file = f"{pub}.htm"
        update_publication_page(pub_file, articles)
    
    print("\n✅ Update complete!")
    print("\nIMPORTANT: This script preserves existing article HTML links")
    print("while updating the article lists.")

if __name__ == "__main__":
    main()
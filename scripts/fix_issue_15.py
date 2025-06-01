#!/usr/bin/env python3
"""
Fix Issue #15: Display PDF directly without intermediate buttons
Updates all article pages to show PDF immediately when users click on article links
"""

import os
import glob
import re
from datetime import datetime

def parse_filename(filename):
    """Parse article filename to extract publication, title, and date"""
    # Remove .pdf or .html extension
    base = filename.replace('.pdf', '').replace('.html', '')
    
    try:
        parts = base.split('-')
        publication = parts[0]
        
        # Find date parts (should be last 3 parts)
        year = parts[-1]
        day = parts[-2]
        month = parts[-3]
        
        # Everything between publication and date is the title
        title_parts = parts[1:-3]
        title = ' '.join(title_parts).replace('_', ' ')
        
        # Convert month number to month name
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        try:
            month_name = month_names[int(month) - 1]
            formatted_date = f"{month_name} {int(day)}, {year}"
        except:
            formatted_date = f"{month}/{day}/{year}"
        
        return {
            'publication': publication,
            'title': title,
            'date': formatted_date,
            'month': month,
            'day': day,
            'year': year
        }
    except:
        return None

def create_new_article_template(pdf_filename, text_content):
    """Create the new article template according to Issue #15 requirements"""
    
    # Parse filename for metadata
    article_info = parse_filename(pdf_filename)
    if not article_info:
        print(f"Warning: Could not parse filename: {pdf_filename}")
        return None
    
    # Clean up the title for display
    display_title = article_info['title']
    
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{display_title} - {article_info['publication']} - Michael Giltz">
    <meta name="keywords" content="Michael Giltz, {article_info['publication']}, journalism, article">
    <meta name="author" content="Michael Giltz">
    <title>{display_title} - Michael Giltz</title>
    <link href="../giltz.css" rel="stylesheet" type="text/css" />
    <style>
        body {{
            font-family: 'Times New Roman', Times, serif;
            margin: 0;
            padding: 0;
            background: #fff;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        .site-banner {{
            text-align: center;
            padding: 20px 0;
            background: #f9f9f9;
        }}
        .site-banner img {{
            max-width: 100%;
            height: auto;
        }}
        .article-header {{
            text-align: center;
            padding: 30px 0 20px 0;
        }}
        .article-title {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 28px;
            font-weight: bold;
            margin: 0 0 10px 0;
            color: #333;
        }}
        .article-meta {{
            font-size: 14px;
            color: #666;
            margin: 0;
        }}
        .pdf-viewer {{
            width: 100%;
            height: 800px;
            margin: 20px 0;
            border: 1px solid #ddd;
        }}
        .home-button {{
            text-align: center;
            padding: 30px 0;
        }}
        .home-button a {{
            display: inline-block;
            padding: 12px 40px;
            background: #333;
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 16px;
            border-radius: 5px;
            text-transform: uppercase;
        }}
        .home-button a:hover {{
            background: #555;
        }}
        .text-section {{
            padding: 40px 0;
            border-top: 3px solid #333;
            margin-top: 40px;
        }}
        .text-section h2 {{
            font-size: 20px;
            color: #333;
            margin: 0 0 20px 0;
            text-transform: uppercase;
        }}
        .text-content {{
            line-height: 1.8;
            color: #333;
            font-size: 16px;
        }}
        .text-content p {{
            margin-bottom: 15px;
        }}
        @media (max-width: 768px) {{
            .pdf-viewer {{
                height: 500px;
            }}
            .article-title {{
                font-size: 22px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Site Banner -->
        <div class="site-banner">
            <a href="../index.htm"><img src="../giltz.jpg" width="800" height="146" alt="MichaelGiltz.com" /></a>
        </div>
        
        <!-- Article Header -->
        <div class="article-header">
            <h1 class="article-title">{display_title}</h1>
            <p class="article-meta">Publication: {article_info['publication']} &nbsp;&nbsp;|&nbsp;&nbsp; Date: {article_info['date']}</p>
        </div>
        
        <!-- PDF Viewer - Direct embed without buttons -->
        <iframe class="pdf-viewer" 
                src="../scans/{pdf_filename}#toolbar=0&navpanes=0" 
                type="application/pdf"
                frameborder="0">
            <p>Your browser does not support PDFs. 
               <a href="../scans/{pdf_filename}">Click here to view the PDF</a>.
            </p>
        </iframe>
        
        <!-- Home Button -->
        <div class="home-button">
            <a href="../index.htm">Home</a>
        </div>
        
        <!-- SEO Text Section -->
        <div class="text-section">
            <h2>SEO TEXT: Article Content for Search Engines</h2>
            <div class="text-content">
                {text_content}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return template

def update_article_file(filepath):
    """Update a single article file with the new template"""
    try:
        # Read the current file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the PDF filename
        pdf_match = re.search(r'href="../scans/([^"]+\.pdf)"', content)
        if not pdf_match:
            print(f"Warning: No PDF link found in {filepath}")
            return False
        
        pdf_filename = pdf_match.group(1)
        
        # Extract the SEO text content
        text_match = re.search(r'<div class="text-content">\s*(.*?)\s*</div>', content, re.DOTALL)
        if text_match:
            text_content = text_match.group(1).strip()
        else:
            text_content = '<p>Text extraction from this PDF is not available. Please view the PDF above.</p>'
        
        # Create new content
        new_content = create_new_article_template(pdf_filename, text_content)
        if not new_content:
            return False
        
        # Write the updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("Fixing Issue #15: Direct PDF Display")
    print("=" * 60)
    
    # Get all article files
    article_files = glob.glob("articles/*.html")
    total_files = len(article_files)
    
    print(f"\nFound {total_files} article files to update")
    
    updated = 0
    failed = 0
    
    # Update each file
    for i, filepath in enumerate(article_files, 1):
        if update_article_file(filepath):
            updated += 1
        else:
            failed += 1
        
        # Progress indicator
        if i % 100 == 0:
            print(f"Progress: {i}/{total_files} files processed...")
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully updated: {updated} files")
    if failed > 0:
        print(f"❌ Failed: {failed} files")
    
    print("\n📋 Changes made:")
    print("• Removed intermediate PDF access buttons")
    print("• PDF now displays directly in iframe")
    print("• Added proper article title and metadata")
    print("• Used Times New Roman font for title")
    print("• Added publication name and formatted date")
    print("• Removed PDF thumbnails/sidebar (#toolbar=0&navpanes=0)")
    print("• Kept home button and SEO text section")
    
    print("\n🚀 Next steps:")
    print("1. Test a few articles locally to verify changes")
    print("2. Upload all updated articles to the server")

if __name__ == "__main__":
    main()
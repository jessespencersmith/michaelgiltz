#!/usr/bin/env python3
"""
Create combined PDF + Text pages for michaelgiltz.com
Implements Issue #1: Combine PDF displays with text from PDFs
"""

import os
import re
from pathlib import Path
import PyPDF2
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def parse_filename(filename):
    """Extract publication, title, and date from filename"""
    # Remove .pdf extension
    name_without_ext = filename.replace('.pdf', '').replace('.PDF', '')
    
    # Split by hyphens
    parts = name_without_ext.split('-')
    
    if len(parts) >= 3:
        publication = parts[0]
        # Join middle parts as title
        title = '-'.join(parts[1:-1])
        # Last part should be date
        date_str = parts[-1]
        
        # Try to parse date
        try:
            # Try different date formats
            for fmt in ['%m_%d_%Y', '%m_%d_%y', '%m_%d_%Y', '%Y_%m_%d']:
                try:
                    date_obj = datetime.strptime(date_str.replace('-', '_'), fmt)
                    formatted_date = date_obj.strftime('%B %d, %Y')
                    break
                except:
                    continue
            else:
                formatted_date = date_str
        except:
            formatted_date = date_str
            
        # Clean up title
        title = title.replace('_', ' ').title()
        
        return publication, title, formatted_date
    else:
        # Fallback for files that don't match pattern
        return "Publication", name_without_ext, "Date Unknown"

def create_combined_page(pdf_filename, pdf_path, output_path):
    """Create a combined PDF + Text HTML page"""
    
    # Parse filename
    publication, title, date = parse_filename(pdf_filename)
    
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Clean up text for HTML
    if pdf_text:
        # Remove excessive whitespace
        pdf_text = re.sub(r'\s+', ' ', pdf_text)
        # Add paragraph breaks at likely spots
        pdf_text = re.sub(r'\.(\s+[A-Z])', '.</p><p>\\1', pdf_text)
        # Escape HTML characters
        pdf_text = pdf_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        pdf_text = f"<p>{pdf_text}</p>"
    else:
        pdf_text = "<p>Text extraction from this PDF is not available. Please view the PDF above.</p>"
    
    # Create HTML content with embedded PDF viewer
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} by Michael Giltz - {publication}">
    <meta name="keywords" content="{publication}, {title}, Michael Giltz, journalism, entertainment">
    <meta name="author" content="Michael Giltz">
    <title>{title} - {publication} - Michael Giltz</title>
    <link href="../giltz.css" rel="stylesheet" type="text/css" />
    <style>
        body {{ 
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background: #333;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header p {{
            margin: 5px 0;
            font-size: 14px;
        }}
        .pdf-viewer {{
            width: 100%;
            height: 600px;
            border: none;
            display: block;
        }}
        .home-button {{
            text-align: center;
            padding: 20px;
            background: #f0f0f0;
        }}
        .home-button a {{
            display: inline-block;
            padding: 10px 30px;
            background: #333;
            color: white;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
        }}
        .home-button a:hover {{
            background: #555;
        }}
        .text-section {{
            padding: 20px;
        }}
        .text-section h2 {{
            color: #333;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        .text-content {{
            line-height: 1.8;
            color: #333;
        }}
        .text-content p {{
            margin-bottom: 15px;
        }}
        .footer {{
            background: #f0f0f0;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }}
        @media (max-width: 768px) {{
            .pdf-viewer {{
                height: 400px;
            }}
        }}
    </style>
    <link rel="icon" type="image/x-icon" href="../favicon.ico">
    <link rel="icon" type="image/png" href="../favicon.png">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>Publication: {publication} | Date: {date} | by Michael Giltz</p>
        </div>
        
        <!-- PDF Viewer -->
        <iframe class="pdf-viewer" src="../scans/{pdf_filename}" title="PDF Article">
            <p>Your browser does not support embedded PDFs. <a href="../scans/{pdf_filename}">Download the PDF</a> to view.</p>
        </iframe>
        
        <!-- Home Button -->
        <div class="home-button">
            <a href="../index.htm">HOME</a>
        </div>
        
        <!-- Text Section -->
        <div class="text-section">
            <h2>SEO TEXT: Article Content for Search</h2>
            <div class="text-content">
                {pdf_text}
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>&copy; {datetime.now().year} Michael Giltz. All rights reserved.</p>
            <p>This article originally appeared in {publication} on {date}.</p>
        </div>
    </div>
</body>
</html>'''
    
    # Write the HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return True

def main():
    """Process all PDFs and create combined pages"""
    
    # Set up paths
    base_dir = Path(__file__).parent.parent
    scans_dir = base_dir / 'scans'
    output_dir = base_dir / 'articles'
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    print("Creating combined PDF + Text pages...")
    print("=" * 50)
    
    # Get all PDF files
    pdf_files = list(scans_dir.glob('*.pdf')) + list(scans_dir.glob('*.PDF'))
    
    print(f"Found {len(pdf_files)} PDFs to process")
    
    # Process each PDF
    success_count = 0
    for i, pdf_path in enumerate(pdf_files):
        if i % 100 == 0:
            print(f"Processing {i}/{len(pdf_files)}...")
        
        pdf_filename = pdf_path.name
        output_path = output_dir / f"{pdf_path.stem}.html"
        
        try:
            if create_combined_page(pdf_filename, pdf_path, output_path):
                success_count += 1
        except Exception as e:
            print(f"Error processing {pdf_filename}: {e}")
    
    print(f"\nCompleted! Created {success_count} combined pages in 'articles' folder")
    
    # Create an index page for the articles
    create_articles_index(output_dir, success_count)

def create_articles_index(articles_dir, count):
    """Create an index page listing all articles"""
    
    index_path = articles_dir.parent / 'articles_index.htm'
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>All Articles - Michael Giltz</title>
    <link href="giltz.css" rel="stylesheet" type="text/css" />
    <style>
        .articles-list { max-width: 800px; margin: 0 auto; padding: 20px; }
        .article-link { margin: 10px 0; }
    </style>
</head>
<body>
    <div class="articles-list">
        <h1>All Articles - Combined View</h1>
        <p>Total: ''' + str(count) + ''' articles with embedded PDFs and searchable text</p>
        <p><a href="index.htm">Back to Homepage</a></p>
        <hr>
        <p>Articles are accessible through the main navigation and search.</p>
    </div>
</body>
</html>'''
    
    with open(index_path, 'w') as f:
        f.write(html)
    
    print(f"Created articles index at: {index_path}")

if __name__ == "__main__":
    main()
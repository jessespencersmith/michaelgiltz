#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhanced PDF Processing Script for michaelgiltz.com
Extracts text from PDFs for SEO while maintaining existing workflow
Compatible with Python 2.7+ and Python 3.x
"""

import os
import sys
import glob
import time
import ftplib
import hashlib
import json
from datetime import datetime

# Handle Python 2/3 compatibility
if sys.version_info[0] >= 3:
    unicode = str

# Try to import PDF libraries
try:
    import PyPDF2
except ImportError:
    try:
        import pypdf2 as PyPDF2
    except ImportError:
        print("Warning: PyPDF2 not found. PDF text extraction will be disabled.")
        PyPDF2 = None

# HTML template for extracted content
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="Michael Giltz">
    <title>{title} - Michael Giltz</title>
    <link href="../giltz.css" rel="stylesheet" type="text/css" />
    <style>
        .pdf-content {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .pdf-header {{ border-bottom: 2px solid #333; margin-bottom: 20px; }}
        .pdf-link {{ background: #f0f0f0; padding: 10px; margin: 10px 0; }}
        .pdf-text {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="pdf-content">
        <div class="pdf-header">
            <h1>{title}</h1>
            <p>Published: {date} | Publication: {publication}</p>
            <div class="pdf-link">
                <strong>Original PDF:</strong> <a href="../scans/{pdf_filename}">Download PDF</a>
            </div>
        </div>
        <div class="pdf-text">
            {content}
        </div>
        <div style="margin-top: 40px; text-align: center;">
            <p><a href="../index.htm">Back to Michael Giltz Homepage</a></p>
        </div>
    </div>
</body>
</html>"""

class PDFProcessor:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.scan_dir = os.path.join(base_dir, "scans")
        self.extract_dir = os.path.join(base_dir, "extracted_content")
        self.log_dir = os.path.join(base_dir, "logs")
        self.state_file = os.path.join(self.log_dir, "processed_files.json")
        self.processed_files = self.load_state()
        
    def load_state(self):
        """Load previously processed files"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_state(self):
        """Save processed files state"""
        os.makedirs(self.log_dir, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.processed_files, f, indent=2)
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from PDF file"""
        if not PyPDF2:
            return None
            
        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text_content = []
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(text)
                
                return '\n\n'.join(text_content)
        except Exception as e:
            print("Error extracting text from {}: {}".format(pdf_path, str(e)))
            return None
    
    def parse_filename(self, filename):
        """Parse PDF filename to extract metadata"""
        # Format: publication-Title_of_Article-MM-DD-YYYY.pdf
        name = filename.replace('.pdf', '')
        try:
            parts = name.split('-')
            if len(parts) >= 5:
                publication = parts[0]
                title = parts[1].replace('_', ' ')
                month = int(parts[2])
                day = int(parts[3])
                year = int(parts[4])
                return {
                    'publication': publication,
                    'title': title,
                    'date': '{}/{}/{}'.format(month, day, year),
                    'year': year,
                    'month': month,
                    'day': day
                }
        except:
            pass
        return None
    
    def create_html_page(self, pdf_filename, text_content, metadata):
        """Create SEO-friendly HTML page from PDF content"""
        if not text_content:
            text_content = "PDF content could not be extracted. Please download the original PDF to view."
        
        # Clean and format text for HTML
        paragraphs = text_content.split('\n\n')
        formatted_content = '\n'.join(['<p>{}</p>'.format(p.strip()) for p in paragraphs if p.strip()])
        
        # Generate description (first 160 chars)
        description = text_content[:160].replace('\n', ' ').strip() + '...'
        
        # Generate keywords
        keywords = "{}, {}, Michael Giltz, journalism, entertainment, arts".format(
            metadata['publication'], metadata['title'].lower()
        )
        
        html_content = HTML_TEMPLATE.format(
            title=metadata['title'],
            description=description,
            keywords=keywords,
            date=metadata['date'],
            publication=metadata['publication'],
            pdf_filename=pdf_filename,
            content=formatted_content
        )
        
        # Save HTML file
        html_filename = pdf_filename.replace('.pdf', '.html')
        html_path = os.path.join(self.extract_dir, html_filename)
        
        os.makedirs(self.extract_dir, exist_ok=True)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_filename
    
    def process_single_pdf(self, pdf_filename):
        """Process a single PDF file"""
        pdf_path = os.path.join(self.scan_dir, pdf_filename)
        
        # Check if already processed
        file_hash = self.get_file_hash(pdf_path)
        if pdf_filename in self.processed_files and self.processed_files[pdf_filename] == file_hash:
            return None
        
        # Parse filename
        metadata = self.parse_filename(pdf_filename)
        if not metadata:
            print("Skipping {}: Invalid filename format".format(pdf_filename))
            return None
        
        # Extract text
        text_content = self.extract_text_from_pdf(pdf_path)
        
        # Create HTML page
        html_filename = self.create_html_page(pdf_filename, text_content, metadata)
        
        # Update state
        self.processed_files[pdf_filename] = file_hash
        
        return html_filename
    
    def get_file_hash(self, filepath):
        """Get MD5 hash of file for change detection"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    
    def process_all_pdfs(self, limit=None):
        """Process all PDFs in scan directory"""
        pdf_files = glob.glob(os.path.join(self.scan_dir, "*.pdf"))
        processed_count = 0
        
        print("Found {} PDF files to process".format(len(pdf_files)))
        
        for i, pdf_path in enumerate(pdf_files):
            if limit and processed_count >= limit:
                break
                
            pdf_filename = os.path.basename(pdf_path)
            print("Processing ({}/{}): {}".format(i+1, len(pdf_files), pdf_filename))
            
            result = self.process_single_pdf(pdf_filename)
            if result:
                processed_count += 1
                print("  Created: {}".format(result))
            else:
                print("  Skipped (already processed or invalid)")
        
        self.save_state()
        print("\nProcessed {} new/updated PDFs".format(processed_count))
        return processed_count

# Inherit from original UpdateArticles.py functionality
def NameFormatCheck(namelist):
    """Check filenames for proper formatting"""
    def good_date(year, month, day):
        tup1 = (year, month, day, 0,0,0,0,0,0)
        try:
            date = time.mktime(tup1)
            tup2 = time.localtime(date)
            if tup1[:2] != tup2[:2]:
                return False
            else:
                return True
        except OverflowError:
            return False

    goodnames = []
    badnames = []
    for filename in namelist:
        rawinfo = filename.rstrip(".pdf")
        try: 
            pub, title, month, day, year = rawinfo.split("-")
            if good_date(int(year), int(month), int(day)):
                goodnames.append(filename)
            else:
                badnames.append(filename)
        except ValueError:
            badnames.append(filename)
    return (goodnames, badnames)

def MakeArticleDict(include_html=True):
    """Read all files and create article links (enhanced version)"""
    os.chdir("scans")
    filelist = glob.glob("*.pdf")
    os.chdir("..")
    pubdatetitlelist = []
    
    for name in filelist:
        name = name.replace('.pdf','')
        try: 
            pub, title, month, day, year = name.split("-")
            info = pub, year, "%02i"%int(month), "%02i"%int(day), month, day, title
            pubdatetitlelist.append("-".join(info))
        except ValueError:
            print("ERROR! Bad format: " + name)
    
    pubdatetitlelist.sort()
    
    articles = {}
    prev = "" 
    for rawinfo in pubdatetitlelist:
        try: 
            pub, year, keymonth, keyday, month, day, title = rawinfo.split("-")
        except:
            print("Bad string: " + rawinfo)
            continue

        if pub != prev:
            prev = pub
            articles[pub] = []
            
        displayname = title.replace("_"," ")
        
        # Original PDF link
        pdf_link = 'scans/%(pub)s-%(title)s-%(month)s-%(day)s-%(year)s.pdf' % {
            'pub':pub, 'title':title, 'month':month, 'day':day, 'year':year
        }
        
        # HTML preview link (if extraction enabled)
        if include_html and PyPDF2:
            html_link = 'extracted_content/%(pub)s-%(title)s-%(month)s-%(day)s-%(year)s.html' % {
                'pub':pub, 'title':title, 'month':month, 'day':day, 'year':year
            }
            
            # Check if HTML file exists
            if os.path.exists(html_link):
                articlelink = '<a href="%(html)s">%(displayname)s, %(month)s-%(day)s-%(year)s</a> [<a href="%(pdf)s">PDF</a>]<br>' % {
                    'html': html_link, 'pdf': pdf_link, 'displayname': displayname,
                    'month': month, 'day': day, 'year': year
                }
            else:
                # Fallback to PDF-only link
                articlelink = '<a href="%(pdf)s">%(displayname)s, %(month)s-%(day)s-%(year)s</a><br>' % {
                    'pdf': pdf_link, 'displayname': displayname,
                    'month': month, 'day': day, 'year': year
                }
        else:
            # PDF-only link
            articlelink = '<a href="%(pdf)s">%(displayname)s, %(month)s-%(day)s-%(year)s</a><br>' % {
                'pdf': pdf_link, 'displayname': displayname,
                'month': month, 'day': day, 'year': year
            }
            
        articles[pub].append(articlelink)
    
    return articles

def UpdatePages(articles):
    """Update HTML pages with article links"""
    pages = glob.glob("*.htm")
    
    # Clear and populate backup directory
    if not os.path.exists("backup"):
        os.makedirs("backup")
        
    for filename in os.listdir("backup"):
        os.remove(os.path.join("backup", filename))
    
    for pagename in pages:
        os.rename(pagename, os.path.join('backup', pagename))
        htmlpage = open(os.path.join('backup', pagename), encoding='utf-8', errors='replace')
        newhtmlpage = open(pagename, 'w', encoding='utf-8')
        inlist = False
        
        for htmlline in htmlpage:
            if not inlist:
                newhtmlpage.write(htmlline)
                if '<!-- list:' in htmlline:
                    inlist = True
                    pub = htmlline.split(':')[1].replace(' -->','').strip()
                    print('Populating links for ' + pub)
                    newhtmlpage.write('<p>\n')
                    try:
                        for article in articles[pub]:
                            newhtmlpage.write(article + '\n')
                    except:
                        print('No articles for ' + pub)
                    newhtmlpage.write('</p>\n')
            if '<!-- /list -->' in htmlline:
                inlist = False
                newhtmlpage.write(htmlline)
                
        newhtmlpage.close()
        htmlpage.close()

def main():
    """Main function with enhanced features"""
    print("\nmichaelgiltz.com Enhanced Processing Script")
    print("=" * 50)
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Process PDFs and update website')
    parser.add_argument('--test', action='store_true', help='Run in test mode (process only 5 PDFs)')
    parser.add_argument('--no-extract', action='store_true', help='Skip PDF text extraction')
    parser.add_argument('--update-only', action='store_true', help='Only update HTML pages, skip PDF processing')
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    os.chdir(parent_dir)
    
    if not args.update_only:
        # Process PDFs for text extraction
        if not args.no_extract and PyPDF2:
            print("\nExtracting text from PDFs...")
            processor = PDFProcessor()
            limit = 5 if args.test else None
            processor.process_all_pdfs(limit=limit)
        else:
            print("\nSkipping PDF text extraction")
    
    # Update article lists
    print("\nUpdating article lists...")
    articles = MakeArticleDict(include_html=not args.no_extract)
    
    # Update HTML pages
    print("\nUpdating HTML pages...")
    UpdatePages(articles)
    
    print("\nProcessing complete!")
    
    # Log completion
    log_dir = os.path.join(parent_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "last_update.txt"), 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    main()
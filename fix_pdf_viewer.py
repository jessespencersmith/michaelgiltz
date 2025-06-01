#!/usr/bin/env python3
"""
Fix PDF viewer in combined pages to work better with modern browsers
"""

import os
import re
from pathlib import Path

def update_html_file(file_path):
    """Update a single HTML file with improved PDF viewer"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the PDF filename from the current iframe
        pdf_match = re.search(r'src="\.\.\/scans\/([^"]+)"', content)
        if not pdf_match:
            return False
        
        pdf_filename = pdf_match.group(1)
        
        # Create improved PDF viewer with multiple fallback methods
        new_pdf_viewer = f'''
        <!-- PDF Viewer with Multiple Fallbacks -->
        <div class="pdf-container">
            <!-- Method 1: PDF.js viewer (modern browsers) -->
            <iframe class="pdf-viewer" 
                    src="../scans/{pdf_filename}#toolbar=1&navpanes=0&scrollbar=1" 
                    title="PDF Article"
                    allowfullscreen>
                
                <!-- Method 2: Fallback with object embed -->
                <object data="../scans/{pdf_filename}" 
                        type="application/pdf" 
                        width="100%" 
                        height="600px">
                    
                    <!-- Method 3: Direct link fallback -->
                    <div class="pdf-fallback">
                        <p><strong>PDF Preview Not Available</strong></p>
                        <p>Your browser doesn't support embedded PDFs. Please use one of these options:</p>
                        <div class="pdf-options">
                            <a href="../scans/{pdf_filename}" target="_blank" class="pdf-button">📄 Open PDF in New Tab</a>
                            <a href="../scans/{pdf_filename}" download class="pdf-button">💾 Download PDF</a>
                        </div>
                    </div>
                </object>
            </iframe>
        </div>'''
        
        # Add improved CSS for the PDF viewer
        css_addition = '''
        .pdf-container {
            background: #f0f0f0;
            border: 1px solid #ddd;
            margin: 10px 0;
        }
        .pdf-fallback {
            text-align: center;
            padding: 40px 20px;
            background: #f9f9f9;
        }
        .pdf-options {
            margin-top: 20px;
        }
        .pdf-button {
            display: inline-block;
            margin: 0 10px;
            padding: 12px 24px;
            background: #333;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        .pdf-button:hover {
            background: #555;
        }'''
        
        # Replace the old iframe with the new viewer
        old_iframe_pattern = r'<iframe class="pdf-viewer"[^>]*>.*?</iframe>'
        content = re.sub(old_iframe_pattern, new_pdf_viewer, content, flags=re.DOTALL)
        
        # Add the CSS before the closing </style> tag
        content = content.replace('</style>', css_addition + '\n    </style>')
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Update all HTML files in the articles directory"""
    
    articles_dir = Path('articles')
    if not articles_dir.exists():
        print("❌ Articles directory not found")
        return
    
    html_files = list(articles_dir.glob('*.html'))
    total_files = len(html_files)
    
    if total_files == 0:
        print("❌ No HTML files found in articles directory")
        return
    
    print(f"Updating PDF viewers in {total_files} articles...")
    print("=" * 60)
    
    updated = 0
    failed = 0
    
    for i, html_file in enumerate(html_files):
        if i % 100 == 0:
            print(f"Progress: {i}/{total_files}")
        
        if update_html_file(html_file):
            updated += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"✅ Updated: {updated} files")
    if failed > 0:
        print(f"❌ Failed: {failed} files")
    
    print("\nNext steps:")
    print("1. Test a few articles locally")
    print("2. Upload updated articles to server")
    print("3. Verify PDFs display correctly")

if __name__ == "__main__":
    main()
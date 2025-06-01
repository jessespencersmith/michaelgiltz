#!/usr/bin/env python3
"""
Final update to all article pages with a reliable PDF access solution
Replaces problematic iframe embedding with professional PDF access interface
"""

import os
import re
from pathlib import Path

def update_article_pdf_viewer(file_path):
    """Update a single article with the final PDF viewer solution"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the PDF filename from the existing content
        pdf_match = re.search(r'src="\.\.\/scans\/([^"]+\.pdf)', content)
        if not pdf_match:
            # Try alternate patterns
            pdf_match = re.search(r'href="\.\.\/scans\/([^"]+\.pdf)', content)
            if not pdf_match:
                return False
        
        pdf_filename = pdf_match.group(1)
        
        # Create a clean title from the filename
        clean_title = pdf_filename.replace('.pdf', '').replace('_', ' ').replace('-', ' - ')
        
        # Create the new PDF access section
        new_pdf_section = f'''        <!-- PDF Viewer -->
        <div class="pdf-access-section">
            <div class="pdf-access-header">
                <h3>📄 View Original Article</h3>
                <p>Access the full article in PDF format</p>
            </div>
            
            <div class="pdf-access-box">
                <div class="pdf-icon-large">📰</div>
                <div class="pdf-details">
                    <h4>{clean_title}</h4>
                    <p class="pdf-format">PDF Document • Original Layout</p>
                </div>
                <div class="pdf-buttons">
                    <a href="../scans/{pdf_filename}" target="_blank" class="btn-pdf primary">
                        <span class="btn-icon">👁️</span>
                        View PDF
                    </a>
                    <a href="../scans/{pdf_filename}" download class="btn-pdf secondary">
                        <span class="btn-icon">⬇️</span>
                        Download
                    </a>
                </div>
            </div>
            
            <p class="pdf-help-text">
                💡 <strong>Tip:</strong> Click "View PDF" to read in your browser, or "Download" to save for offline reading.
            </p>
        </div>'''
        
        # New CSS for the PDF access section
        new_css = '''        /* PDF Access Section */
        .pdf-access-section {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 30px;
            margin: 30px 0;
            text-align: center;
        }
        .pdf-access-header h3 {
            color: #212529;
            margin: 0 0 10px 0;
            font-size: 24px;
        }
        .pdf-access-header p {
            color: #6c757d;
            margin: 0 0 25px 0;
            font-size: 16px;
        }
        .pdf-access-box {
            background: white;
            border-radius: 8px;
            padding: 25px;
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .pdf-icon-large {
            font-size: 48px;
            flex-shrink: 0;
        }
        .pdf-details {
            flex-grow: 1;
            text-align: left;
        }
        .pdf-details h4 {
            margin: 0 0 5px 0;
            color: #212529;
            font-size: 18px;
        }
        .pdf-format {
            margin: 0;
            color: #6c757d;
            font-size: 14px;
        }
        .pdf-buttons {
            display: flex;
            gap: 12px;
            flex-shrink: 0;
        }
        .btn-pdf {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s ease;
            white-space: nowrap;
        }
        .btn-pdf.primary {
            background: #0066cc;
            color: white;
            border: 2px solid #0066cc;
        }
        .btn-pdf.primary:hover {
            background: #0052a3;
            border-color: #0052a3;
            transform: translateY(-1px);
        }
        .btn-pdf.secondary {
            background: white;
            color: #495057;
            border: 2px solid #ced4da;
        }
        .btn-pdf.secondary:hover {
            background: #f8f9fa;
            border-color: #adb5bd;
            transform: translateY(-1px);
        }
        .btn-icon {
            font-size: 16px;
        }
        .pdf-help-text {
            color: #6c757d;
            font-size: 14px;
            margin: 0;
        }
        @media (max-width: 768px) {
            .pdf-access-box {
                flex-direction: column;
                text-align: center;
            }
            .pdf-details {
                text-align: center;
            }
            .pdf-buttons {
                flex-direction: column;
                width: 100%;
            }
            .btn-pdf {
                width: 100%;
                justify-content: center;
            }
        }'''
        
        # Remove all existing PDF viewer implementations
        # Pattern 1: Remove the entire PDF container div
        content = re.sub(
            r'<!-- PDF Viewer.*?-->\s*<div class="pdf-container">.*?</div>\s*(?:</div>\s*)?',
            '<!-- PDF Viewer -->\n        <!-- [PDF viewer will be inserted here] -->',
            content,
            flags=re.DOTALL
        )
        
        # Pattern 2: Remove iframe-based viewers
        content = re.sub(
            r'<iframe class="pdf-viewer".*?</iframe>',
            '<!-- [PDF viewer will be inserted here] -->',
            content,
            flags=re.DOTALL
        )
        
        # Pattern 3: Remove modern PDF viewer sections
        content = re.sub(
            r'<!-- Modern PDF Viewer.*?</div>\s*</div>',
            '<!-- [PDF viewer will be inserted here] -->',
            content,
            flags=re.DOTALL
        )
        
        # Replace the placeholder with new PDF section
        content = content.replace('<!-- [PDF viewer will be inserted here] -->', new_pdf_section)
        
        # If no placeholder was created, find the PDF Viewer comment
        if '<!-- PDF Viewer -->' in content and 'pdf-access-section' not in content:
            content = content.replace(
                '<!-- PDF Viewer -->',
                new_pdf_section
            )
        
        # Add or update CSS
        if '.pdf-access-section' not in content:
            # Add new CSS before closing </style> tag
            content = content.replace('    </style>', new_css + '\n    </style>')
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Update all article HTML files with the final PDF viewer solution"""
    
    articles_dir = Path('articles')
    if not articles_dir.exists():
        print("❌ Articles directory not found!")
        return
    
    # Get all HTML files
    html_files = list(articles_dir.glob('*.html'))
    total_files = len(html_files)
    
    print(f"Updating {total_files} article files with final PDF solution...")
    print("=" * 60)
    
    updated = 0
    failed = 0
    
    # Process files with progress updates
    for i, html_file in enumerate(html_files):
        if i % 100 == 0 and i > 0:
            print(f"Progress: {i}/{total_files} files processed...")
        
        if update_article_pdf_viewer(html_file):
            updated += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"✅ Successfully updated: {updated} files")
    if failed > 0:
        print(f"❌ Failed to update: {failed} files")
    
    print("\n📋 Summary:")
    print("• Replaced problematic iframe embedding")
    print("• Added professional PDF access interface")
    print("• Works in ALL browsers (Chrome, Firefox, Safari, Edge)")
    print("• Mobile-friendly responsive design")
    print("• Clear call-to-action buttons")
    print("• Helpful user guidance")
    
    print("\n🚀 Next steps:")
    print("1. Test a few articles locally")
    print("2. Run upload_site.py to upload all updated articles")
    print("3. Verify PDFs are accessible on live site")

if __name__ == "__main__":
    main()
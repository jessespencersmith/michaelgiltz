#!/usr/bin/env python3
"""
Create a modern PDF viewer using PDF.js CDN for better compatibility
"""

import os
import re
from pathlib import Path

def create_modern_viewer(file_path):
    """Update HTML file with modern PDF.js viewer"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract PDF filename
        pdf_match = re.search(r'src="\.\.\/scans\/([^"]+)"', content)
        if not pdf_match:
            return False
        
        pdf_filename = pdf_match.group(1)
        
        # Create modern PDF viewer using PDF.js CDN
        modern_viewer = f'''
        <!-- Modern PDF Viewer using PDF.js -->
        <div class="pdf-container">
            <div class="pdf-toolbar">
                <span class="pdf-title">📄 Article PDF</span>
                <div class="pdf-controls">
                    <a href="../scans/{pdf_filename}" target="_blank" class="pdf-btn">🔗 Open in New Tab</a>
                    <a href="../scans/{pdf_filename}" download class="pdf-btn">💾 Download</a>
                </div>
            </div>
            
            <!-- PDF.js Viewer -->
            <iframe 
                class="pdf-viewer"
                src="https://mozilla.github.io/pdf.js/web/viewer.html?file=https://michaelgiltz.com/scans/{pdf_filename}"
                title="PDF Article Viewer"
                allowfullscreen>
                
                <!-- Fallback for older browsers -->
                <div class="pdf-fallback">
                    <h3>📄 View Article PDF</h3>
                    <p>This article is available as a PDF document.</p>
                    <div class="pdf-buttons">
                        <a href="../scans/{pdf_filename}" target="_blank" class="pdf-button primary">
                            🔗 Open PDF in New Tab
                        </a>
                        <a href="../scans/{pdf_filename}" download class="pdf-button secondary">
                            💾 Download PDF
                        </a>
                    </div>
                    <p class="pdf-note">
                        <small>If the PDF doesn't load, your browser may not support embedded documents.</small>
                    </p>
                </div>
            </iframe>
        </div>'''
        
        # Enhanced CSS for modern viewer
        modern_css = '''
        .pdf-container {
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .pdf-toolbar {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .pdf-title {
            font-weight: bold;
            font-size: 14px;
        }
        .pdf-controls {
            display: flex;
            gap: 10px;
        }
        .pdf-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            border: 1px solid rgba(255,255,255,0.3);
            transition: all 0.3s ease;
        }
        .pdf-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-1px);
        }
        .pdf-viewer {
            width: 100%;
            height: 700px;
            border: none;
            display: block;
        }
        .pdf-fallback {
            text-align: center;
            padding: 60px 20px;
            background: #f8f9fa;
        }
        .pdf-fallback h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        .pdf-buttons {
            margin: 25px 0;
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .pdf-button {
            display: inline-block;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            transition: all 0.3s ease;
            min-width: 160px;
        }
        .pdf-button.primary {
            background: #3498db;
            color: white;
        }
        .pdf-button.primary:hover {
            background: #2980b9;
            transform: translateY(-2px);
        }
        .pdf-button.secondary {
            background: #95a5a6;
            color: white;
        }
        .pdf-button.secondary:hover {
            background: #7f8c8d;
            transform: translateY(-2px);
        }
        .pdf-note {
            color: #666;
            margin-top: 20px;
        }
        @media (max-width: 768px) {
            .pdf-viewer {
                height: 500px;
            }
            .pdf-toolbar {
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }
            .pdf-buttons {
                flex-direction: column;
                align-items: center;
            }
        }'''
        
        # Replace old viewer
        old_pattern = r'<div class="pdf-container">.*?</div>\s*</div>'
        content = re.sub(old_pattern, modern_viewer, content, flags=re.DOTALL)
        
        # Replace old CSS
        css_pattern = r'\.pdf-container \{.*?(?=\s*@media|\s*</style>)'
        content = re.sub(css_pattern, modern_css, content, flags=re.DOTALL)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Update a few sample articles for testing"""
    
    test_files = [
        'articles/Parade-13_New_Books_About_Royals_to_Read_If_You_Have_Royal_Fever-5-20-2021.html',
        'articles/AMERICAblog-Bush_Loses_Again-7-16-2004.html',
        'articles/Advocate-American_Idol_anti_gay_Carla_Hay-5-11-2004.html',
    ]
    
    print("Creating modern PDF viewer for sample articles...")
    print("=" * 60)
    
    updated = 0
    for file_path in test_files:
        if os.path.exists(file_path):
            if create_modern_viewer(file_path):
                print(f"✓ Updated: {file_path}")
                updated += 1
            else:
                print(f"✗ Failed: {file_path}")
        else:
            print(f"⚠ Not found: {file_path}")
    
    print("=" * 60)
    print(f"✅ Updated {updated} articles with modern PDF viewer")
    print("\nFeatures of the new viewer:")
    print("- Uses PDF.js CDN for better compatibility")
    print("- Modern toolbar with controls")
    print("- Responsive design")
    print("- Enhanced fallback options")
    print("- Better mobile experience")

if __name__ == "__main__":
    main()
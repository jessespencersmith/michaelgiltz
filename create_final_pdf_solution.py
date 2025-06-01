#!/usr/bin/env python3
"""
Create the final PDF solution that works reliably in all browsers
Instead of fighting browser restrictions, provide excellent user experience
"""

import os
import re
from pathlib import Path

def create_final_solution(file_path):
    """Create the final PDF viewer solution"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract PDF filename
        pdf_match = re.search(r'src="\.\.\/scans\/([^"]+)"', content)
        if not pdf_match:
            return False
        
        pdf_filename = pdf_match.group(1)
        
        # Create the final solution - clean and reliable
        final_viewer = f'''
        <!-- PDF Article Access -->
        <div class="pdf-article-section">
            <div class="pdf-header">
                <h3>📰 Read the Original Article</h3>
                <p>This article is available as a high-quality PDF document</p>
            </div>
            
            <div class="pdf-preview">
                <div class="pdf-thumbnail">
                    <div class="pdf-icon">📄</div>
                    <div class="pdf-info">
                        <strong>{pdf_filename.replace('_', ' ').replace('-', ' - ')}</strong>
                        <p>Original article in PDF format</p>
                    </div>
                </div>
                
                <div class="pdf-actions">
                    <a href="../scans/{pdf_filename}" target="_blank" class="pdf-action primary">
                        🔗 Open PDF
                    </a>
                    <a href="../scans/{pdf_filename}" download class="pdf-action secondary">
                        💾 Download
                    </a>
                </div>
            </div>
            
            <div class="pdf-note">
                <p><small>💡 Tip: The PDF will open in a new tab where you can read, zoom, and print the full article.</small></p>
            </div>
        </div>'''
        
        # Clean, modern CSS
        final_css = '''
        .pdf-article-section {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border: 2px solid #dee2e6;
            border-radius: 12px;
            margin: 30px 0;
            padding: 25px;
            text-align: center;
        }
        .pdf-header h3 {
            color: #2c3e50;
            margin: 0 0 10px 0;
            font-size: 22px;
        }
        .pdf-header p {
            color: #6c757d;
            margin: 0 0 25px 0;
        }
        .pdf-preview {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .pdf-thumbnail {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        .pdf-icon {
            font-size: 48px;
            opacity: 0.8;
        }
        .pdf-info {
            text-align: left;
        }
        .pdf-info strong {
            display: block;
            color: #2c3e50;
            font-size: 16px;
            margin-bottom: 5px;
        }
        .pdf-info p {
            color: #6c757d;
            margin: 0;
            font-size: 14px;
        }
        .pdf-actions {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .pdf-action {
            display: inline-block;
            padding: 14px 28px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            transition: all 0.3s ease;
            min-width: 140px;
            border: 2px solid transparent;
        }
        .pdf-action.primary {
            background: #3498db;
            color: white;
        }
        .pdf-action.primary:hover {
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }
        .pdf-action.secondary {
            background: white;
            color: #2c3e50;
            border-color: #dee2e6;
        }
        .pdf-action.secondary:hover {
            background: #f8f9fa;
            border-color: #adb5bd;
            transform: translateY(-2px);
        }
        .pdf-note {
            margin-top: 15px;
        }
        .pdf-note p {
            color: #6c757d;
            margin: 0;
        }
        @media (max-width: 768px) {
            .pdf-thumbnail {
                flex-direction: column;
                text-align: center;
            }
            .pdf-info {
                text-align: center;
            }
            .pdf-actions {
                flex-direction: column;
                align-items: center;
            }
            .pdf-action {
                width: 100%;
                max-width: 200px;
            }
        }'''
        
        # Replace all PDF viewer content
        old_patterns = [
            r'<div class="pdf-container">.*?</div>\s*</div>',
            r'<!-- PDF Viewer.*?</div>',
            r'<!-- Modern PDF Viewer.*?</div>',
        ]
        
        for pattern in old_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Find the PDF Viewer comment and replace
        viewer_pattern = r'<!-- PDF Viewer -->'
        content = re.sub(viewer_pattern, final_viewer, content)
        
        # Replace the CSS
        css_start = content.find('.pdf-container {')
        if css_start != -1:
            css_end = content.find('@media (max-width: 768px)', css_start)
            if css_end != -1:
                css_end = content.find('}', css_end) + 1
                css_end = content.find('}', css_end) + 1
                content = content[:css_start] + final_css + content[css_end:]
        else:
            # Add CSS before closing </style>
            content = content.replace('</style>', final_css + '\n    </style>')
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Update sample articles with the final solution"""
    
    test_files = [
        'articles/Parade-13_New_Books_About_Royals_to_Read_If_You_Have_Royal_Fever-5-20-2021.html',
        'articles/AMERICAblog-Bush_Loses_Again-7-16-2004.html',
        'articles/Advocate-American_Idol_anti_gay_Carla_Hay-5-11-2004.html',
    ]
    
    print("Creating final PDF solution...")
    print("=" * 60)
    
    updated = 0
    for file_path in test_files:
        if os.path.exists(file_path):
            if create_final_solution(file_path):
                print(f"✓ Updated: {file_path}")
                updated += 1
            else:
                print(f"✗ Failed: {file_path}")
        else:
            print(f"⚠ Not found: {file_path}")
    
    print("=" * 60)
    print(f"✅ Updated {updated} articles with final PDF solution")
    print("\n🎯 This solution provides:")
    print("• Clear, prominent PDF access")
    print("• Professional design")
    print("• Works in ALL browsers")
    print("• Mobile-friendly")
    print("• Fast loading")
    print("• No technical issues")

if __name__ == "__main__":
    main()
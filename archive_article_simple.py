#!/usr/bin/env python3
"""
Simple Article PDF Archiver
==========================

This tool converts articles to compressed PDFs with manual filename entry.

Requirements:
- macOS
- Ghostscript: brew install ghostscript
- Playwright: pip3 install playwright && playwright install chromium

Usage:
    python3 archive_article_simple.py
"""

import os
import sys
import re
import subprocess
from datetime import datetime
from pathlib import Path
import asyncio


def check_requirements():
    """Check if required tools are installed"""
    tools_ok = True
    
    # Check Ghostscript
    try:
        subprocess.run(['gs', '--version'], capture_output=True, check=True)
        print("✓ Ghostscript installed")
    except:
        print("✗ Ghostscript NOT installed")
        print("  Install with: brew install ghostscript")
        tools_ok = False
    
    # Check if Playwright is installed
    try:
        import playwright
        print("✓ Playwright installed")
    except ImportError:
        print("✗ Playwright NOT installed")
        print("  Install with: pip3 install playwright")
        print("  Then run: playwright install chromium")
        tools_ok = False
    
    if not tools_ok:
        print("\nPlease install missing tools before continuing.")
        sys.exit(1)
    
    print()


def get_filename_from_user():
    """Get filename from user with format reminder"""
    print("\n" + "="*60)
    print("FILENAME FORMAT:")
    print("Publication-Article_Title-MM-DD-YYYY.pdf")
    print("\nExamples:")
    print("  Variety-Oscar_Nominations_2024-01-23-2024.pdf")
    print("  HollywoodReporter-Box_Office_Report-02-15-2024.pdf")
    print("  NYTimes-Theater_Review_Hamlet-03-10-2024.pdf")
    print("="*60)
    
    while True:
        filename = input("\nEnter filename (without .pdf): ").strip()
        
        if not filename:
            print("Please enter a filename.")
            continue
        
        # Add .pdf if not present
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        # Basic validation
        if filename.count('-') < 3:
            print("\nFilename should follow format: Publication-Title-MM-DD-YYYY.pdf")
            print("Make sure to include hyphens between sections.")
            continue
        
        # Show what they entered
        print(f"\nFilename: {filename}")
        confirm = input("Is this correct? (Y/n): ").strip().lower()
        
        if confirm != 'n':
            return filename


async def create_pdf_with_playwright(url, output_path):
    """Create PDF using Playwright with better rendering"""
    print("\nGenerating PDF from webpage...")
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            # Create context with print-friendly settings
            context = await browser.new_context(
                viewport={'width': 1200, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            
            page = await context.new_page()
            
            # Add CSS to improve print layout
            await page.add_style_tag(content="""
                @media print {
                    * {
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }
                    body {
                        margin: 0 !important;
                        font-size: 12pt !important;
                        line-height: 1.5 !important;
                    }
                    img {
                        max-width: 100% !important;
                        height: auto !important;
                    }
                    .no-print, .ads, .sidebar, nav, header nav, footer {
                        display: none !important;
                    }
                    article, main, .content {
                        width: 100% !important;
                        margin: 0 !important;
                        padding: 0 !important;
                    }
                }
            """)
            
            # Navigate to page
            print("Loading webpage...")
            try:
                await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                # Wait for content
                await page.wait_for_timeout(5000)
            except Exception as e:
                print(f"Warning: {e}")
                # Continue anyway
            
            # Try to remove ads and popups
            try:
                await page.evaluate("""
                    // Remove common ad elements
                    document.querySelectorAll('[class*="ad-"], [id*="ad-"], .advertisement, .ads, .popup, .modal, .overlay').forEach(el => el.remove());
                    // Remove fixed position elements
                    document.querySelectorAll('*').forEach(el => {
                        const style = window.getComputedStyle(el);
                        if (style.position === 'fixed' || style.position === 'sticky') {
                            el.style.display = 'none';
                        }
                    });
                """)
            except:
                pass
            
            # Generate PDF with better settings
            print("Converting to PDF...")
            await page.pdf(
                path=output_path,
                format='Letter',  # US Letter size
                print_background=True,
                display_header_footer=False,
                margin={
                    'top': '0.75in',
                    'bottom': '0.75in',
                    'left': '0.75in',
                    'right': '0.75in'
                },
                prefer_css_page_size=False,
                scale=0.8  # Slightly smaller to fit better
            )
            
            await context.close()
            await browser.close()
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            size_mb = os.path.getsize(output_path) / 1024 / 1024
            print(f"✓ PDF created: {size_mb:.1f} MB")
            return True
        else:
            print("✗ Failed to create PDF")
            return False
            
    except Exception as e:
        print(f"✗ Error creating PDF: {e}")
        return False


def compress_pdf_with_ghostscript(input_path, output_path):
    """Compress PDF using Ghostscript with 72 DPI setting"""
    print("\nCompressing PDF...")
    print("Target: 72 DPI images for small file size")
    
    gs_command = [
        'gs',
        '-q',
        '-dNOPAUSE',
        '-dBATCH',
        '-dSAFER',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.5',
        '-dPDFSETTINGS=/screen',
        '-dDownsampleColorImages=true',
        '-dColorImageResolution=72',
        '-dDownsampleGrayImages=true',
        '-dGrayImageResolution=72',
        '-dDownsampleMonoImages=true',
        '-dMonoImageResolution=72',
        '-dCompressFonts=true',
        '-dSubsetFonts=true',
        '-dEmbedAllFonts=false',
        '-dAutoRotatePages=/None',
        '-dOptimize=true',
        f'-sOutputFile={output_path}',
        input_path
    ]
    
    try:
        # Get original size
        original_size = os.path.getsize(input_path)
        print(f"Original size: {original_size / 1024 / 1024:.1f} MB")
        
        # Run compression
        result = subprocess.run(gs_command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Ghostscript warning: {result.stderr}")
            # Continue anyway, often still works
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            compressed_size = os.path.getsize(output_path)
            reduction_pct = (1 - compressed_size / original_size) * 100
            
            print(f"✓ Compressed size: {compressed_size / 1024:.0f} KB")
            print(f"✓ Size reduction: {reduction_pct:.0f}%")
            return True
        else:
            print("✗ Compression failed")
            return False
            
    except Exception as e:
        print(f"✗ Compression error: {e}")
        return False


def main():
    """Main function"""
    print("\nSIMPLE ARTICLE PDF ARCHIVER")
    print("="*60)
    print("Saves articles as compressed PDFs to your Desktop")
    print("="*60)
    
    # Check requirements
    check_requirements()
    
    # Get URL
    url = input("Enter article URL: ").strip()
    
    if not url:
        print("No URL provided")
        return
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Get filename from user
    filename = get_filename_from_user()
    
    # Set up paths
    desktop = Path.home() / 'Desktop'
    temp_pdf = desktop / f"temp_{filename}"
    final_pdf = desktop / filename
    
    print(f"\nProcessing: {filename}")
    print("-" * 60)
    
    # Create PDF
    if not asyncio.run(create_pdf_with_playwright(url, str(temp_pdf))):
        print("\n✗ Failed to create PDF")
        return
    
    # Compress PDF
    if not compress_pdf_with_ghostscript(str(temp_pdf), str(final_pdf)):
        print("\n✗ Failed to compress PDF")
        # Keep uncompressed version
        if os.path.exists(temp_pdf):
            os.rename(temp_pdf, final_pdf)
            print("✓ Saved uncompressed PDF instead")
    else:
        # Clean up temp file
        if os.path.exists(temp_pdf):
            os.unlink(temp_pdf)
    
    # Success!
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print(f"✅ Saved to Desktop: {filename}")
    print(f"✅ Final size: {os.path.getsize(final_pdf) / 1024:.0f} KB")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
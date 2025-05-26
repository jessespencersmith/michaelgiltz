#!/usr/bin/env python3
"""
Entertainment Article PDF Archiver
==================================

This tool converts entertainment articles to space-efficient PDFs.
Designed specifically for archiving Michael Giltz's entertainment articles.

Features:
- Converts webpages to PDF
- Compresses PDFs using Ghostscript (9MB → 400KB)
- Images downsampled to 72 DPI
- Interactive filename creation
- Saves to Desktop

Requirements:
- macOS
- Ghostscript (REQUIRED): brew install ghostscript
- wkhtmltopdf: brew install --cask wkhtmltopdf

Usage:
    python3 archive_article_tool.py
"""

import os
import sys
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.parse


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
    
    # Check wkhtmltopdf
    try:
        subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, check=True)
        print("✓ wkhtmltopdf installed")
    except:
        print("✗ wkhtmltopdf NOT installed")
        print("  Install with: brew install --cask wkhtmltopdf")
        tools_ok = False
    
    if not tools_ok:
        print("\nPlease install missing tools before continuing.")
        sys.exit(1)
    
    print()


def clean_text_for_filename(text):
    """Clean text for safe filename use"""
    # Remove HTML entities and special characters
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    text = text.strip('_')
    return text


def get_suggested_publication(url):
    """Suggest publication name based on URL"""
    domain = urllib.parse.urlparse(url).netloc.lower()
    domain = domain.replace('www.', '')
    
    # Common entertainment sites
    suggestions = {
        'variety.com': 'Variety',
        'hollywoodreporter.com': 'HollywoodReporter',
        'deadline.com': 'Deadline',
        'indiewire.com': 'IndieWire',
        'ew.com': 'EntertainmentWeekly',
        'rollingstone.com': 'RollingStone',
        'billboard.com': 'Billboard',
        'vulture.com': 'Vulture',
        'avclub.com': 'AVClub',
        'thewrap.com': 'TheWrap',
        'nytimes.com': 'NYTimes',
        'latimes.com': 'LATimes',
        'theguardian.com': 'Guardian',
        'vanityfair.com': 'VanityFair',
        'newyorker.com': 'NewYorker',
        'slate.com': 'Slate',
        'salon.com': 'Salon',
        'huffpost.com': 'HuffPost',
        'thedailybeast.com': 'DailyBeast',
        'polygon.com': 'Polygon',
        'ign.com': 'IGN',
        'pitchfork.com': 'Pitchfork',
        'stereogum.com': 'Stereogum',
        'consequence.net': 'Consequence',
        'collider.com': 'Collider',
        'screenrant.com': 'ScreenRant',
        'denofgeek.com': 'DenOfGeek',
        'slashfilm.com': 'SlashFilm',
        'empireonline.com': 'Empire',
        'timeout.com': 'TimeOut',
        'vice.com': 'Vice',
        'buzzfeed.com': 'BuzzFeed',
        'vox.com': 'Vox',
        'wired.com': 'Wired',
        'gq.com': 'GQ',
        'esquire.com': 'Esquire'
    }
    
    if domain in suggestions:
        return suggestions[domain]
    
    # Clean up domain for suggestion
    name = domain.split('.')[0]
    return ''.join(word.capitalize() for word in name.split('-'))


def get_suggested_title(url):
    """Try to extract article title from webpage"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Try to find title
        import re
        
        # Try Open Graph title
        match = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', html, re.I)
        if match:
            return match.group(1)
        
        # Try regular title tag
        match = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
        if match:
            title = match.group(1).strip()
            # Remove site name
            title = re.split(r'\s*[\|–—-]\s*', title)[0].strip()
            return title
            
    except:
        pass
    
    return ""


def get_suggested_date(url):
    """Try to extract article date"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Try article:published_time
        match = re.search(r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([\d-]+)', html, re.I)
        if match:
            date_str = match.group(1)[:10]
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                return date_obj.strftime('%m-%d-%Y')
            except:
                pass
        
        # Try datePublished
        match = re.search(r'"datePublished"\s*:\s*"([\d-]+)', html)
        if match:
            date_str = match.group(1)[:10]
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                return date_obj.strftime('%m-%d-%Y')
            except:
                pass
                
    except:
        pass
    
    # Default to today
    return datetime.now().strftime('%m-%d-%Y')


def interactive_filename_creation(url):
    """Interactive process to create filename"""
    print("\n" + "="*60)
    print("FILENAME CREATION")
    print("="*60)
    print(f"URL: {url}")
    print("\nFormat: Publication-Title_of_Article-MM-DD-YYYY.pdf")
    print("="*60)
    
    # Get suggestions
    suggested_pub = get_suggested_publication(url)
    suggested_title = get_suggested_title(url)
    suggested_date = get_suggested_date(url)
    
    # Get publication
    print(f"\n1. PUBLICATION NAME")
    if suggested_pub:
        print(f"   Suggested: {suggested_pub}")
    publication = input("   Enter publication name (or press Enter to use suggestion): ").strip()
    if not publication and suggested_pub:
        publication = suggested_pub
    elif not publication:
        publication = input("   Please enter publication name: ").strip()
    
    # Clean publication name
    publication = clean_text_for_filename(publication)
    
    # Get title
    print(f"\n2. ARTICLE TITLE")
    if suggested_title:
        print(f"   Suggested: {suggested_title}")
    title = input("   Enter article title (or press Enter to use suggestion): ").strip()
    if not title and suggested_title:
        title = suggested_title
    elif not title:
        title = input("   Please enter article title: ").strip()
    
    # Clean title
    title = clean_text_for_filename(title)
    
    # Get date
    print(f"\n3. PUBLICATION DATE (MM-DD-YYYY)")
    print(f"   Suggested: {suggested_date}")
    date_input = input("   Enter date (or press Enter for suggestion): ").strip()
    
    if not date_input:
        date_str = suggested_date
    else:
        # Validate date format
        try:
            # Try different formats
            for fmt in ['%m-%d-%Y', '%m/%d/%Y', '%Y-%m-%d', '%m-%d-%y']:
                try:
                    date_obj = datetime.strptime(date_input, fmt)
                    date_str = date_obj.strftime('%m-%d-%Y')
                    break
                except:
                    continue
            else:
                print("   Invalid date format. Using today's date.")
                date_str = datetime.now().strftime('%m-%d-%Y')
        except:
            date_str = datetime.now().strftime('%m-%d-%Y')
    
    # Create filename
    filename = f"{publication}-{title}-{date_str}.pdf"
    
    print(f"\n4. FINAL FILENAME")
    print(f"   {filename}")
    confirm = input("   Is this correct? (Y/n): ").strip().lower()
    
    if confirm == 'n':
        return interactive_filename_creation(url)
    
    return filename


def create_pdf_from_url(url, output_path):
    """Create PDF from URL using wkhtmltopdf"""
    print("\nGenerating PDF from webpage...")
    
    cmd = [
        'wkhtmltopdf',
        '--print-media-type',
        '--no-stop-slow-scripts',
        '--javascript-delay', '3000',
        '--load-error-handling', 'ignore',
        '--load-media-error-handling', 'ignore',
        '--enable-local-file-access',
        url,
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and not os.path.exists(output_path):
            print(f"Error creating PDF: {result.stderr}")
            return False
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            size_mb = os.path.getsize(output_path) / 1024 / 1024
            print(f"✓ PDF created: {size_mb:.1f} MB")
            return True
        else:
            print("✗ Failed to create PDF")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def compress_pdf_with_ghostscript(input_path, output_path):
    """Compress PDF using exact Ghostscript settings from issue"""
    print("\nCompressing PDF with Ghostscript...")
    print("Target: Downsample images to 72 DPI")
    
    # Exact command from the issue with 72 DPI settings
    gs_command = [
        'gs',
        '-q',
        '-dNOPAUSE',
        '-dBATCH',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.5',
        '-dPDFSETTINGS=/screen',
        '-dDownsampleColorImages=true',
        '-dColorImageResolution=72',
        '-dColorImageDownsampleThreshold=1.0',
        '-dDownsampleGrayImages=true',
        '-dGrayImageResolution=72',
        '-dGrayImageDownsampleThreshold=1.0',
        '-dDownsampleMonoImages=true',
        '-dMonoImageResolution=72',
        '-dMonoImageDownsampleThreshold=1.0',
        '-dCompressFonts=true',
        '-dEmbedAllFonts=false',
        '-dSubsetFonts=true',
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
            print(f"Ghostscript error: {result.stderr}")
            return False
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            compressed_size = os.path.getsize(output_path)
            reduction_pct = (1 - compressed_size / original_size) * 100
            
            print(f"✓ Compressed size: {compressed_size / 1024:.0f} KB")
            print(f"✓ Size reduction: {reduction_pct:.0f}%")
            
            # Example from issue: 9MB → 400KB is 95.6% reduction
            if compressed_size < original_size:
                return True
            else:
                print("Warning: Compression did not reduce file size")
                return False
        else:
            print("✗ Compression failed - no output file")
            return False
            
    except Exception as e:
        print(f"✗ Compression error: {e}")
        return False


def main():
    """Main function"""
    print("\nENTERTAINMENT ARTICLE PDF ARCHIVER")
    print("="*60)
    print("Converts web articles to space-efficient PDFs")
    print("Images compressed to 72 DPI for minimal file size")
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
    
    # Interactive filename creation
    filename = interactive_filename_creation(url)
    
    # Set up paths
    desktop = Path.home() / 'Desktop'
    temp_pdf = desktop / f"temp_{filename}"
    final_pdf = desktop / filename
    
    print(f"\nProcessing: {filename}")
    print("-" * 60)
    
    # Step 1: Create PDF from webpage
    if not create_pdf_from_url(url, str(temp_pdf)):
        print("\n✗ Failed to create PDF from webpage")
        return
    
    # Step 2: Compress PDF (REQUIRED)
    if not compress_pdf_with_ghostscript(str(temp_pdf), str(final_pdf)):
        print("\n✗ Failed to compress PDF")
        # Clean up temp file
        if os.path.exists(temp_pdf):
            os.unlink(temp_pdf)
        return
    
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
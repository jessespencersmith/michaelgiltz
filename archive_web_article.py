#!/usr/bin/env python3
"""
Web Article PDF Archiver for Michael Giltz
==========================================

This tool archives web articles as compressed PDFs on your Desktop.
It's designed to be simple and reliable for archiving entertainment articles.

Features:
- Automatically extracts article title and publication date
- Creates consistent filenames: Publication-Title-MM-DD-YYYY.pdf
- Compresses PDFs to save space (requires Ghostscript)
- Works with major entertainment and news websites

Requirements:
- Python 3.6+
- Ghostscript (optional but recommended for compression)
  Install with: brew install ghostscript

Usage:
    python3 archive_web_article.py
    
Then enter the URL when prompted.

Example:
    URL: https://variety.com/2024/tv/news/some-tv-show-article
    Output: Variety-Some_TV_Show_Article-01-26-2024.pdf
"""

import os
import sys
import re
import subprocess
import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
import tempfile
import html


def clean_filename(text):
    """Clean text for use in filename"""
    # Decode HTML entities
    text = html.unescape(text)
    # Remove or replace problematic characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    text = text.strip('_')
    # Limit length
    if len(text) > 80:
        text = text[:80].rsplit('_', 1)[0]
    return text


def get_publication_name(url):
    """Extract publication name from URL"""
    domain = urllib.parse.urlparse(url).netloc.lower()
    
    # Remove www prefix
    domain = domain.replace('www.', '')
    
    # Common entertainment and news publications
    publications = {
        # Entertainment Trade Publications
        'variety.com': 'Variety',
        'hollywoodreporter.com': 'HollywoodReporter',
        'deadline.com': 'Deadline',
        'indiewire.com': 'IndieWire',
        'thewrap.com': 'TheWrap',
        
        # Entertainment Magazines
        'ew.com': 'EntertainmentWeekly',
        'rollingstone.com': 'RollingStone',
        'billboard.com': 'Billboard',
        'spin.com': 'Spin',
        'pitchfork.com': 'Pitchfork',
        'consequence.net': 'Consequence',
        'stereogum.com': 'Stereogum',
        'nme.com': 'NME',
        
        # Pop Culture Sites
        'vulture.com': 'Vulture',
        'avclub.com': 'AVClub',
        'gawker.com': 'Gawker',
        'jezebel.com': 'Jezebel',
        'io9.com': 'io9',
        'kotaku.com': 'Kotaku',
        'polygon.com': 'Polygon',
        'ign.com': 'IGN',
        
        # Film/TV Sites
        'collider.com': 'Collider',
        'screenrant.com': 'ScreenRant',
        'cinemablend.com': 'CinemaBlend',
        'slashfilm.com': 'SlashFilm',
        'denofgeek.com': 'DenOfGeek',
        'empireonline.com': 'Empire',
        'totalfilm.com': 'TotalFilm',
        
        # General News
        'nytimes.com': 'NYTimes',
        'washingtonpost.com': 'WashingtonPost',
        'latimes.com': 'LATimes',
        'usatoday.com': 'USAToday',
        'wsj.com': 'WSJ',
        'theguardian.com': 'Guardian',
        'guardian.co.uk': 'Guardian',
        'bbc.com': 'BBC',
        'bbc.co.uk': 'BBC',
        'cnn.com': 'CNN',
        'npr.org': 'NPR',
        
        # Magazines
        'newyorker.com': 'NewYorker',
        'vanityfair.com': 'VanityFair',
        'gq.com': 'GQ',
        'esquire.com': 'Esquire',
        'theatlantic.com': 'Atlantic',
        'harpersbazaar.com': 'HarpersBazaar',
        'wmagazine.com': 'W',
        'interviewmagazine.com': 'Interview',
        
        # Online Media
        'buzzfeed.com': 'BuzzFeed',
        'buzzfeednews.com': 'BuzzFeedNews',
        'vice.com': 'Vice',
        'vox.com': 'Vox',
        'slate.com': 'Slate',
        'salon.com': 'Salon',
        'thedailybeast.com': 'DailyBeast',
        'huffpost.com': 'HuffPost',
        'huffingtonpost.com': 'HuffPost',
        
        # Tech/Gaming
        'theverge.com': 'TheVerge',
        'wired.com': 'Wired',
        'arstechnica.com': 'ArsTechnica',
        'techcrunch.com': 'TechCrunch',
        'gamespot.com': 'GameSpot',
        
        # Politics
        'politico.com': 'Politico',
        'thehill.com': 'TheHill',
        'axios.com': 'Axios',
        
        # Books/Literary
        'lithub.com': 'LitHub',
        'bookforum.com': 'Bookforum',
        'nybooks.com': 'NYReviewBooks',
        'lrb.co.uk': 'LondonReviewBooks',
        
        # Local/Regional
        'timeout.com': 'TimeOut',
        'laweekly.com': 'LAWeekly',
        'villagevoice.com': 'VillageVoice',
        'chicagotribune.com': 'ChicagoTribune',
        'boston.com': 'Boston',
        'seattletimes.com': 'SeattleTimes',
        'sfgate.com': 'SFGate',
        
        # International
        'lemonde.fr': 'LeMonde',
        'spiegel.de': 'DerSpiegel',
        'elpais.com': 'ElPais',
        'smh.com.au': 'SydneyMorningHerald'
    }
    
    # Check if domain is in our mapping
    if domain in publications:
        return publications[domain]
    
    # Check partial matches (for subdomains)
    for pub_domain, pub_name in publications.items():
        if pub_domain in domain or domain.endswith('.' + pub_domain):
            return pub_name
    
    # Default: clean up domain name
    name = domain.split('.')[0]
    # Remove hyphens and capitalize
    name = ''.join(word.capitalize() for word in name.split('-'))
    return name


def fetch_article_metadata(url):
    """Fetch article title and date from URL"""
    print(f"Fetching article metadata from: {url}")
    
    try:
        # Create request with headers
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        
        # Fetch the page
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
        
        # Extract title
        title = "Untitled_Article"
        
        # Try Open Graph title
        match = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', html_content, re.I)
        if match:
            title = match.group(1)
        else:
            # Try regular title
            match = re.search(r'<title>(.*?)</title>', html_content, re.I | re.S)
            if match:
                title = match.group(1).strip()
                # Remove site name (usually after | or -)
                title = re.split(r'\s*[\|–—-]\s*', title)[0].strip()
        
        # Extract date
        date_obj = datetime.now()
        
        # Try article:published_time
        match = re.search(r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([\d-]+)', html_content, re.I)
        if match:
            try:
                date_obj = datetime.strptime(match.group(1)[:10], '%Y-%m-%d')
            except:
                pass
        else:
            # Try datePublished in JSON-LD
            match = re.search(r'"datePublished"\s*:\s*"([\d-]+)', html_content)
            if match:
                try:
                    date_obj = datetime.strptime(match.group(1)[:10], '%Y-%m-%d')
                except:
                    pass
        
        return title, date_obj
        
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return "Untitled_Article", datetime.now()


def download_pdf_printfriendly(url, output_path):
    """Download PDF using PrintFriendly service"""
    print("Generating PDF using PrintFriendly...")
    
    # PrintFriendly API URL
    pf_url = f"https://pdf-api.printfriendly.com/pdfs"
    
    # Prepare data
    data = urllib.parse.urlencode({
        'url': url,
        'format': 'pdf',
        'orientation': 'portrait'
    }).encode('utf-8')
    
    try:
        # Create request
        req = urllib.request.Request(pf_url, data=data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        # Download PDF
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        
        return True
        
    except Exception as e:
        print(f"PrintFriendly failed: {e}")
        return False


def download_pdf_web2pdf(url, output_path):
    """Download PDF using Web2PDF service"""
    print("Generating PDF using Web2PDF...")
    
    # Web2PDF URL
    pdf_url = f"https://api.web2pdfconvert.com/convert/web/pdf?url={urllib.parse.quote(url)}"
    
    try:
        # Download PDF
        req = urllib.request.Request(pdf_url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        
        return True
        
    except Exception as e:
        print(f"Web2PDF failed: {e}")
        return False


def create_pdf_with_weasyprint(url, output_path):
    """Create PDF using WeasyPrint if installed"""
    try:
        import weasyprint
        print("Generating PDF using WeasyPrint...")
        
        # Create PDF
        weasyprint.HTML(url=url).write_pdf(output_path)
        return True
        
    except ImportError:
        return False
    except Exception as e:
        print(f"WeasyPrint failed: {e}")
        return False


def compress_pdf(input_path, output_path):
    """Compress PDF using Ghostscript"""
    # Check if Ghostscript is installed
    try:
        result = subprocess.run(['which', 'gs'], capture_output=True, text=True)
        if not result.stdout.strip():
            print("\nNote: Ghostscript not installed. PDF will not be compressed.")
            print("To enable compression, install with: brew install ghostscript")
            # Just move the file
            if input_path != output_path:
                os.rename(input_path, output_path)
            return
    except:
        if input_path != output_path:
            os.rename(input_path, output_path)
        return
    
    print("Compressing PDF...")
    
    # Ghostscript command for compression
    gs_command = [
        'gs',
        '-q',
        '-dNOPAUSE',
        '-dBATCH',
        '-dSAFER',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/screen',
        '-dEmbedAllFonts=true',
        '-dSubsetFonts=true',
        '-dColorImageDownsampleType=/Bicubic',
        '-dColorImageResolution=150',
        '-dGrayImageDownsampleType=/Bicubic',
        '-dGrayImageResolution=150',
        '-dMonoImageDownsampleType=/Bicubic',
        '-dMonoImageResolution=150',
        '-dAutoRotatePages=/None',
        f'-sOutputFile={output_path}',
        input_path
    ]
    
    try:
        # Get original size
        original_size = os.path.getsize(input_path)
        
        # Run compression
        subprocess.run(gs_command, check=True, capture_output=True)
        
        # Get compressed size
        compressed_size = os.path.getsize(output_path)
        
        # Show results
        reduction = (1 - compressed_size / original_size) * 100
        print(f"Original: {original_size / 1024:.1f} KB")
        print(f"Compressed: {compressed_size / 1024:.1f} KB")
        print(f"Reduction: {reduction:.1f}%")
        
        # Remove uncompressed version
        if os.path.exists(input_path) and input_path != output_path:
            os.unlink(input_path)
            
    except subprocess.CalledProcessError:
        print("Compression failed, using original PDF")
        if input_path != output_path:
            os.rename(input_path, output_path)


def main():
    """Main function"""
    print("Web Article PDF Archiver")
    print("=" * 60)
    print("This tool saves web articles as PDFs on your Desktop")
    print("=" * 60)
    
    # Get URL
    url = input("\nEnter article URL: ").strip()
    
    if not url:
        print("No URL provided")
        return
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Get metadata
    title, date_obj = fetch_article_metadata(url)
    publication = get_publication_name(url)
    
    # Create filename
    clean_title = clean_filename(title)
    date_str = date_obj.strftime('%m-%d-%Y')
    filename = f"{publication}-{clean_title}-{date_str}.pdf"
    
    # Paths
    desktop = Path.home() / 'Desktop'
    temp_pdf = desktop / f"temp_{filename}"
    final_pdf = desktop / filename
    
    print(f"\nArticle: {title}")
    print(f"Publication: {publication}")
    print(f"Date: {date_str}")
    print(f"Filename: {filename}\n")
    
    # Try different methods to create PDF
    success = False
    
    # Method 1: Try WeasyPrint (best quality if installed)
    if not success:
        success = create_pdf_with_weasyprint(url, str(temp_pdf))
    
    # Method 2: Try PrintFriendly
    if not success:
        success = download_pdf_printfriendly(url, str(temp_pdf))
    
    # Method 3: Try Web2PDF
    if not success:
        success = download_pdf_web2pdf(url, str(temp_pdf))
    
    if success and os.path.exists(temp_pdf):
        # Compress the PDF
        compress_pdf(str(temp_pdf), str(final_pdf))
        
        print(f"\n✅ Success! PDF saved to your Desktop:")
        print(f"   {final_pdf}")
        print(f"\nFile size: {os.path.getsize(final_pdf) / 1024:.1f} KB")
    else:
        print("\n❌ Failed to create PDF")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the URL is correct") 
        print("3. Some sites may block automated access")
        print("\nFor best results, you can install WeasyPrint:")
        print("   pip3 install weasyprint")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease check the URL and try again")
#!/usr/bin/env python3
"""
Comprehensive validation of the entire GiltzWeb 2 site
Checks local files and live site for consistency and correctness
"""

import os
import glob
import re
import subprocess
from collections import defaultdict
from datetime import datetime

def check_local_files():
    """Validate all local files"""
    results = {
        'pdfs': {'count': 0, 'issues': []},
        'articles': {'count': 0, 'issues': []},
        'pages': {'count': 0, 'issues': []},
        'links': {'article_links': 0, 'pdf_links': 0, 'broken': []}
    }
    
    # Check PDFs in scans directory
    print("\n📁 Checking PDF files...")
    pdf_files = glob.glob("scans/*.pdf")
    results['pdfs']['count'] = len(pdf_files)
    
    # Check for naming convention
    for pdf in pdf_files:
        filename = os.path.basename(pdf)
        if not re.match(r'^[^-]+-[^-]+-\d{1,2}-\d{1,2}-\d{4}\.pdf$', filename):
            results['pdfs']['issues'].append(f"Bad naming: {filename}")
    
    # Check article HTML files
    print("📄 Checking article HTML files...")
    article_files = glob.glob("articles/*.html")
    results['articles']['count'] = len(article_files)
    
    # Check if each PDF has a corresponding article
    for pdf in pdf_files:
        pdf_name = os.path.basename(pdf)
        article_name = pdf_name.replace('.pdf', '.html')
        article_path = f"articles/{article_name}"
        if not os.path.exists(article_path):
            results['articles']['issues'].append(f"Missing article for: {pdf_name}")
    
    # Check publication pages
    print("📑 Checking publication pages...")
    pub_pages = glob.glob("*.htm")
    results['pages']['count'] = len(pub_pages)
    
    # Check links in each publication page
    for page in pub_pages:
        if page.startswith(('index.', 'template.')):
            continue
            
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count article vs PDF links
        article_links = len(re.findall(r'href="articles/[^"]+\.html"', content))
        pdf_links = len(re.findall(r'href="scans/[^"]+\.pdf"', content))
        
        results['links']['article_links'] += article_links
        results['links']['pdf_links'] += pdf_links
        
        if pdf_links > 0:
            results['pages']['issues'].append(f"{page}: Has {pdf_links} PDF links (should be 0)")
    
    return results

def check_live_site():
    """Check the live site"""
    print("\n🌐 Checking live site...")
    results = {
        'pages_checked': [],
        'issues': [],
        'pdf_interface': {'checked': 0, 'working': 0}
    }
    
    # Test key pages
    test_pages = [
        'Parade.htm',
        'HuffingtonPost.htm', 
        'AMERICAblog.htm',
        'BookFilter.htm',
        'Advocate.htm'
    ]
    
    for page in test_pages:
        url = f"https://www.michaelgiltz.com/{page}"
        print(f"   Checking {page}...")
        
        # Get page content
        try:
            result = subprocess.run(
                ['curl', '-s', url],
                capture_output=True,
                text=True,
                timeout=10
            )
            content = result.stdout
            
            # Count links
            article_links = len(re.findall(r'href="articles/[^"]+\.html"', content))
            pdf_links = len(re.findall(r'href="scans/[^"]+\.pdf"', content))
            
            results['pages_checked'].append({
                'page': page,
                'article_links': article_links,
                'pdf_links': pdf_links
            })
            
            if pdf_links > 0:
                results['issues'].append(f"{page}: Has {pdf_links} PDF links")
                
        except Exception as e:
            results['issues'].append(f"Failed to check {page}: {e}")
    
    # Test a few article pages for PDF interface
    test_articles = [
        'articles/Advocate-Aaron_Copland_bio_by_Howard_Pollack-5-11-1999.html',
        'articles/AMERICAblog-1776_The_Americablog_review-7-1-2005.html',
        'articles/BookFilter-Four_Futures_By_Peter_Frase-10-11-2016.html'
    ]
    
    for article in test_articles:
        url = f"https://www.michaelgiltz.com/{article}"
        try:
            result = subprocess.run(
                ['curl', '-s', url],
                capture_output=True,
                text=True,
                timeout=10
            )
            content = result.stdout
            
            results['pdf_interface']['checked'] += 1
            
            # Check for new PDF interface
            if 'pdf-access-section' in content and 'View PDF' in content:
                results['pdf_interface']['working'] += 1
                
        except Exception as e:
            results['issues'].append(f"Failed to check article: {e}")
    
    return results

def check_admin_panel():
    """Check admin panel configuration"""
    print("\n🔧 Checking admin panel...")
    results = {'status': 'Unknown', 'issues': []}
    
    # Check local admin files
    if os.path.exists('admin/index.php'):
        with open('admin/index.php', 'r') as f:
            content = f.read()
        
        if 'process_new_pdfs.py' in content:
            results['status'] = 'Correct (uses new system)'
        elif 'process_pdfs.py' in content:
            results['status'] = 'Partially correct'
        else:
            results['status'] = 'Incorrect'
            results['issues'].append('Admin panel not using correct update script')
    
    # Check if old update script is disabled
    if os.path.exists('UpdateArticles.py'):
        results['issues'].append('UpdateArticles.py still exists (should be disabled)')
    elif os.path.exists('UpdateArticles.py.disabled'):
        results['status'] += ' (old script disabled ✓)'
    
    return results

def generate_report(local_results, live_results, admin_results):
    """Generate validation report"""
    print("\n" + "=" * 60)
    print("GILTZWEB 2 VALIDATION REPORT")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Local files summary
    print("\n📊 LOCAL FILES SUMMARY")
    print(f"• PDFs in scans: {local_results['pdfs']['count']}")
    print(f"• Article HTML files: {local_results['articles']['count']}")
    print(f"• Publication pages: {local_results['pages']['count']}")
    print(f"• Total article links: {local_results['links']['article_links']}")
    print(f"• Total PDF links: {local_results['links']['pdf_links']}")
    
    # Issues
    if local_results['pdfs']['issues']:
        print(f"\n⚠️  PDF naming issues: {len(local_results['pdfs']['issues'])}")
        for issue in local_results['pdfs']['issues'][:5]:
            print(f"   - {issue}")
        if len(local_results['pdfs']['issues']) > 5:
            print(f"   ... and {len(local_results['pdfs']['issues']) - 5} more")
    
    if local_results['articles']['issues']:
        print(f"\n⚠️  Missing articles: {len(local_results['articles']['issues'])}")
        print("   Run: python3 scripts/create_combined_pages.py")
    
    if local_results['pages']['issues']:
        print(f"\n⚠️  Pages with PDF links: {len(local_results['pages']['issues'])}")
        for issue in local_results['pages']['issues']:
            print(f"   - {issue}")
    
    # Live site summary
    print("\n🌐 LIVE SITE SUMMARY")
    for page_info in live_results['pages_checked']:
        status = "✅" if page_info['pdf_links'] == 0 else "❌"
        print(f"{status} {page_info['page']}: {page_info['article_links']} article links, {page_info['pdf_links']} PDF links")
    
    pdf_status = live_results['pdf_interface']
    print(f"\nPDF Interface: {pdf_status['working']}/{pdf_status['checked']} working")
    
    if live_results['issues']:
        print("\n⚠️  Live site issues:")
        for issue in live_results['issues']:
            print(f"   - {issue}")
    
    # Admin panel
    print(f"\n🔧 ADMIN PANEL: {admin_results['status']}")
    if admin_results['issues']:
        for issue in admin_results['issues']:
            print(f"   - {issue}")
    
    # Overall status
    print("\n" + "=" * 60)
    total_issues = (
        len(local_results['pdfs']['issues']) +
        len(local_results['articles']['issues']) +
        len(local_results['pages']['issues']) +
        len(live_results['issues']) +
        len(admin_results['issues'])
    )
    
    if total_issues == 0:
        print("✅ VALIDATION PASSED - No issues found!")
    else:
        print(f"⚠️  VALIDATION FOUND {total_issues} ISSUES")
        print("\nRecommended actions:")
        if local_results['articles']['issues']:
            print("1. Run: python3 scripts/create_combined_pages.py")
        if local_results['pages']['issues'] or live_results['issues']:
            print("2. Run: python3 fix_missing_links.py")
        if pdf_status['working'] < pdf_status['checked']:
            print("3. Continue uploading article batches")
    
    print("=" * 60)

def main():
    print("Starting comprehensive site validation...")
    
    # Run all checks
    local_results = check_local_files()
    live_results = check_live_site()
    admin_results = check_admin_panel()
    
    # Generate report
    generate_report(local_results, live_results, admin_results)
    
    # Save detailed report
    with open('validation_report.txt', 'w') as f:
        f.write(f"GiltzWeb 2 Validation Report\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        f.write(f"Local Results:\n{local_results}\n\n")
        f.write(f"Live Results:\n{live_results}\n\n")
        f.write(f"Admin Results:\n{admin_results}\n")
    
    print("\n📋 Detailed report saved to: validation_report.txt")

if __name__ == "__main__":
    main()
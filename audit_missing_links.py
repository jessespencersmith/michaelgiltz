#!/usr/bin/env python3
"""
Comprehensive audit of missing links across all publication pages
"""

import os
import re
from pathlib import Path

def count_links_in_file(file_path):
    """Count different types of links in an HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count links to articles (correct format)
        article_links = len(re.findall(r'href="articles/[^"]+\.html"', content))
        
        # Count links to PDFs (incorrect format)
        pdf_links = len(re.findall(r'href="scans/[^"]+\.pdf"', content))
        
        # Count mixed old format links (extracted_content)
        old_links = len(re.findall(r'href="extracted_content/[^"]+\.html"', content))
        
        return {
            'article_links': article_links,
            'pdf_links': pdf_links,
            'old_links': old_links,
            'total_content_links': article_links + pdf_links + old_links
        }
    except Exception as e:
        return {'error': str(e)}

def count_pdfs_for_publication(pub_prefix):
    """Count PDFs in scans folder for a specific publication"""
    scans_dir = Path('scans')
    if not scans_dir.exists():
        return 0
    
    count = 0
    for pdf in scans_dir.glob(f"{pub_prefix}-*.pdf"):
        count += 1
    return count

def main():
    print("Comprehensive Link Audit")
    print("=" * 60)
    
    # Publication files to check
    publications = [
        ('Parade', 'Parade.htm'),
        ('HuffPo/HuffingtonPost', 'HuffingtonPost.htm'),
        ('AMERICAblog', 'AMERICAblog.htm'),
        ('NYPost', 'NYPost.htm'),
        ('Popsurfing', 'Popsurfing.htm'),
        ('Advocate', 'Advocate.htm'),
        ('BookFilter', 'BookFilter.htm'),
        ('Alligator', 'Alligator.htm'),
        ('NYDailyNews', 'NYDailyNews.htm'),
        ('NewYork', 'NewYork.htm'),
        ('LATimes', 'LATimes.htm'),
        ('EntertainmentWeekly', 'EntertainmentWeekly.htm'),
        ('Premiere', 'Premiere.htm'),
        ('BroadwayDirect', 'BroadwayDirect.htm'),
    ]
    
    total_issues = 0
    
    for pub_name, file_name in publications:
        if os.path.exists(file_name):
            # Get PDF count
            pdf_prefix = pub_name.split('/')[0]  # Handle "HuffPo/HuffingtonPost"
            pdf_count = count_pdfs_for_publication(pdf_prefix)
            
            # Get link count
            link_stats = count_links_in_file(file_name)
            
            if 'error' in link_stats:
                print(f"❌ {pub_name}: ERROR - {link_stats['error']}")
                continue
            
            # Calculate missing links
            expected_links = pdf_count
            actual_links = link_stats['total_content_links']
            missing = expected_links - actual_links
            
            # Status indicator
            if missing > 0:
                status = "❌ MISSING LINKS"
                total_issues += missing
            elif link_stats['pdf_links'] > 0 or link_stats['old_links'] > 0:
                status = "⚠️  WRONG FORMAT"
                total_issues += link_stats['pdf_links'] + link_stats['old_links']
            else:
                status = "✅ OK"
            
            print(f"{status} {pub_name}:")
            print(f"  PDFs in scans: {pdf_count}")
            print(f"  Article links: {link_stats['article_links']}")
            print(f"  PDF links: {link_stats['pdf_links']}")
            print(f"  Old links: {link_stats['old_links']}")
            if missing > 0:
                print(f"  MISSING: {missing} links")
            print()
        else:
            print(f"❌ {pub_name}: FILE NOT FOUND - {file_name}")
            print()
    
    print("=" * 60)
    if total_issues > 0:
        print(f"❌ TOTAL ISSUES FOUND: {total_issues}")
        print("\nRecommended fixes:")
        print("1. Re-run update_links_to_html.py")
        print("2. Re-run fix_remaining_links.py") 
        print("3. Re-upload affected HTML files")
        print("4. Verify uploads took effect")
    else:
        print("✅ ALL PUBLICATIONS LOOK GOOD!")
    
    # Create detailed report
    with open('link_audit_report.txt', 'w') as f:
        f.write("Link Audit Report\n")
        f.write("=" * 50 + "\n\n")
        for pub_name, file_name in publications:
            if os.path.exists(file_name):
                pdf_prefix = pub_name.split('/')[0]
                pdf_count = count_pdfs_for_publication(pdf_prefix)
                link_stats = count_links_in_file(file_name)
                
                f.write(f"{pub_name}:\n")
                f.write(f"  PDFs: {pdf_count}\n")
                f.write(f"  Links: {link_stats}\n")
                f.write("\n")
    
    print(f"\nDetailed report saved to: link_audit_report.txt")

if __name__ == "__main__":
    main()
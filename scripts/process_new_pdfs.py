#!/usr/bin/env python3
"""
Process new PDFs by creating combined HTML pages
This script is called by the admin panel to process newly uploaded PDFs
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import create_combined_pages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.create_combined_pages import process_pdf
except ImportError:
    # If running from scripts directory
    from create_combined_pages import process_pdf

def load_processed_state(state_file):
    """Load list of already processed PDFs"""
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_processed_state(state_file, processed_files):
    """Save list of processed PDFs"""
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, 'w') as f:
        json.dump(list(processed_files), f, indent=2)

def update_publication_page(pdf_filename, publication_pages_dir):
    """Update the publication HTML page with new article link"""
    # Parse filename to get publication
    parts = pdf_filename.split('-')
    if not parts:
        return
    
    publication = parts[0]
    
    # Map publication to HTML file
    publication_map = {
        'AMERICAblog': 'AMERICAblog.htm',
        'Advocate': 'Advocate.htm',
        'Alligator': 'Alligator.htm',
        'BBC': 'BBC_Portfolio.htm',
        'BookFilter': 'BookFilter.htm',
        'Bookandfilmglobe': 'Bookandfilmglobe.htm',
        'Books': 'Books.htm',
        'BroadwayDirect': 'BroadwayDirect.htm',
        'CDReview': 'CDReview.htm',
        'DVDs': 'DVDs.htm',
        'EntertainmentWeekly': 'EntertainmentWeekly.htm',
        'Flowers': 'Flowers_Portfolio.htm',
        'Fox': 'Fox_Portfolio.htm',
        'General': 'General.htm',
        'HuffPo': 'HuffingtonPost.htm',
        'HuffingtonPost': 'HuffingtonPost.htm',
        'IRA': 'IRAAwards.htm',
        'LATimes': 'LATimes.htm',
        'Lists': 'Lists.htm',
        'Misc': 'Misc.htm',
        'Movies': 'Movies.htm',
        'Music': 'Music.htm',
        'NYDailyNews': 'NYDailyNews.htm',
        'NYPost': 'NYPost.htm',
        'NewYork': 'NewYork.htm',
        'Parade': 'Parade.htm',
        'People': 'People.htm',
        'Politics': 'Politics.htm',
        'Popsurfing': 'Popsurfing.htm',
        'Premiere': 'Premiere.htm',
        'Sports': 'Sports.htm',
        'TV': 'TV.htm',
        'TheIRAs': 'TheIRAs.htm',
        'TheLists': 'TheLists.htm',
        'Theater': 'Theater.htm'
    }
    
    html_file = publication_map.get(publication)
    if not html_file:
        print(f"Warning: Unknown publication '{publication}' for {pdf_filename}")
        return
    
    html_path = os.path.join(publication_pages_dir, html_file)
    if not os.path.exists(html_path):
        print(f"Warning: Publication page {html_file} not found")
        return
    
    # Create link HTML
    html_filename = pdf_filename.replace('.pdf', '.html')
    
    # Parse article info
    try:
        parts = pdf_filename.replace('.pdf', '').split('-')
        title = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown Title'
        date = f"{parts[2]}-{parts[3]}-{parts[4]}" if len(parts) >= 5 else 'Unknown Date'
        
        new_link = f'<a href="articles/{html_filename}">{title}, {date}</a><br>\n'
        
        # Read the HTML file
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the appropriate place to insert (after the last article link)
        # Look for the pattern of article links
        insert_pos = content.rfind('</a><br>')
        if insert_pos != -1:
            insert_pos = content.find('\n', insert_pos) + 1
            # Insert the new link
            updated_content = content[:insert_pos] + new_link + content[insert_pos:]
            
            # Write back
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✓ Updated {html_file} with link to {html_filename}")
        else:
            print(f"Warning: Could not find insertion point in {html_file}")
            
    except Exception as e:
        print(f"Error updating {html_file}: {e}")

def main():
    """Process new PDFs and create combined HTML pages"""
    
    # Setup paths
    base_dir = Path(__file__).parent.parent  # GiltzWeb 2 directory
    scans_dir = base_dir / 'scans'
    articles_dir = base_dir / 'articles'
    state_file = base_dir / 'logs' / 'processed_pdfs.json'
    
    # Create directories if needed
    articles_dir.mkdir(exist_ok=True)
    
    # Load processed state
    processed_files = load_processed_state(state_file)
    
    # Find all PDFs
    pdf_files = list(scans_dir.glob('*.pdf'))
    new_pdfs = [f for f in pdf_files if f.name not in processed_files]
    
    if not new_pdfs:
        print("No new PDFs to process")
        return
    
    print(f"Found {len(new_pdfs)} new PDFs to process")
    
    # Process each new PDF
    success_count = 0
    for pdf_path in new_pdfs:
        print(f"\nProcessing: {pdf_path.name}")
        
        try:
            # Create combined HTML page
            output_path = articles_dir / pdf_path.name.replace('.pdf', '.html')
            
            # Use the process_pdf function from create_combined_pages
            if process_pdf(str(pdf_path), str(articles_dir)):
                print(f"✓ Created: {output_path.name}")
                
                # Update the publication page
                update_publication_page(pdf_path.name, str(base_dir))
                
                # Mark as processed
                processed_files.add(pdf_path.name)
                success_count += 1
            else:
                print(f"✗ Failed to process: {pdf_path.name}")
                
        except Exception as e:
            print(f"✗ Error processing {pdf_path.name}: {e}")
    
    # Save updated state
    save_processed_state(state_file, processed_files)
    
    # Update last update time
    last_update_file = base_dir / 'logs' / 'last_update.txt'
    last_update_file.parent.mkdir(exist_ok=True)
    with open(last_update_file, 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Successfully processed: {success_count}/{len(new_pdfs)} PDFs")
    
    # Test mode
    if '--test' in sys.argv and success_count > 0:
        print("\nTest mode - processed first PDF only")
        return
    
    return 0 if success_count == len(new_pdfs) else 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migration Script for Michael Giltz Website
Processes all existing PDFs to generate HTML versions
Can handle large volumes and resume if interrupted
"""

import os
import sys
import time
import json
import glob
from datetime import datetime

# Import the PDF processor from our main script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from process_pdfs import PDFProcessor, NameFormatCheck

class MigrationManager:
    def __init__(self):
        self.processor = PDFProcessor('..')
        self.migration_state_file = os.path.join(self.processor.log_dir, 'migration_state.json')
        self.batch_size = 100
        self.load_state()
        
    def load_state(self):
        """Load migration state"""
        if os.path.exists(self.migration_state_file):
            with open(self.migration_state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                'started': None,
                'completed': False,
                'total_files': 0,
                'processed_files': 0,
                'failed_files': [],
                'last_processed': None,
                'batches_completed': 0
            }
    
    def save_state(self):
        """Save migration state"""
        os.makedirs(self.processor.log_dir, exist_ok=True)
        with open(self.migration_state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_all_pdfs(self):
        """Get all PDFs sorted by date"""
        pdf_files = glob.glob(os.path.join(self.processor.scan_dir, "*.pdf"))
        
        # Sort by filename (which includes date)
        pdf_files.sort()
        
        return pdf_files
    
    def show_progress(self, current, total):
        """Display progress bar"""
        percent = (current / total) * 100 if total > 0 else 0
        bar_length = 50
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        sys.stdout.write('\r|%s| %.1f%% (%d/%d)' % (bar, percent, current, total))
        sys.stdout.flush()
    
    def calculate_size(self, pdf_files):
        """Calculate total size of PDFs"""
        total_size = 0
        for pdf in pdf_files:
            try:
                total_size += os.path.getsize(pdf)
            except:
                pass
        return total_size
    
    def format_size(self, size_bytes):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return "%.2f %s" % (size_bytes, unit)
            size_bytes /= 1024.0
        return "%.2f TB" % size_bytes
    
    def run_migration(self, resume=True):
        """Run the migration process"""
        print("\n" + "="*60)
        print("Michael Giltz Website Migration Tool")
        print("="*60)
        
        # Get all PDFs
        all_pdfs = self.get_all_pdfs()
        total_count = len(all_pdfs)
        total_size = self.calculate_size(all_pdfs)
        
        print("\nMigration Overview:")
        print(f"  Total PDFs found: {total_count:,}")
        print(f"  Total size: {self.format_size(total_size)}")
        print(f"  Batch size: {self.batch_size}")
        print(f"  Estimated batches: {(total_count // self.batch_size) + 1}")
        
        # Check for resumption
        if resume and self.state['started'] and not self.state['completed']:
            print(f"\nResuming from previous migration...")
            print(f"  Previously processed: {self.state['processed_files']:,}")
            start_index = self.state['processed_files']
        else:
            print("\nStarting fresh migration...")
            start_index = 0
            self.state['started'] = datetime.now().isoformat()
            self.state['total_files'] = total_count
            self.state['processed_files'] = 0
            self.state['failed_files'] = []
            self.state['batches_completed'] = 0
        
        # Confirmation
        print("\nPress Enter to continue or Ctrl+C to cancel...")
        try:
            input()
        except KeyboardInterrupt:
            print("\nMigration cancelled.")
            return
        
        print("\nStarting migration...\n")
        
        # Process in batches
        batch_num = start_index // self.batch_size
        
        for i in range(start_index, total_count):
            pdf_path = all_pdfs[i]
            pdf_filename = os.path.basename(pdf_path)
            
            # Check if new batch
            current_batch = i // self.batch_size
            if current_batch > batch_num:
                batch_num = current_batch
                self.state['batches_completed'] = batch_num
                print(f"\n\nStarting batch {batch_num + 1}...")
                time.sleep(1)  # Brief pause between batches
            
            try:
                # Show progress
                self.show_progress(i + 1, total_count)
                
                # Process PDF
                result = self.processor.process_single_pdf(pdf_filename)
                
                if result:
                    self.state['last_processed'] = pdf_filename
                
                self.state['processed_files'] = i + 1
                
                # Save state periodically
                if (i + 1) % 10 == 0:
                    self.save_state()
                    self.processor.save_state()
                    
            except KeyboardInterrupt:
                print("\n\nMigration interrupted by user.")
                self.save_state()
                self.processor.save_state()
                print(f"Progress saved. Processed {i}/{total_count} files.")
                print("Run the migration again to resume.")
                return
                
            except Exception as e:
                print(f"\nError processing {pdf_filename}: {str(e)}")
                self.state['failed_files'].append({
                    'filename': pdf_filename,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Migration complete
        self.state['completed'] = True
        self.state['completed_at'] = datetime.now().isoformat()
        self.save_state()
        self.processor.save_state()
        
        print("\n\n" + "="*60)
        print("Migration Complete!")
        print("="*60)
        print(f"  Total processed: {self.state['processed_files']:,}")
        print(f"  Failed files: {len(self.state['failed_files'])}")
        
        if self.state['failed_files']:
            print("\nFailed files:")
            for failed in self.state['failed_files'][:10]:
                print(f"  - {failed['filename']}: {failed['error']}")
            if len(self.state['failed_files']) > 10:
                print(f"  ... and {len(self.state['failed_files']) - 10} more")
        
        print("\nNext steps:")
        print("1. Run 'python scripts/process_pdfs.py' to update HTML pages")
        print("2. Test the website locally")
        print("3. Deploy to server")
        print()
    
    def show_status(self):
        """Show current migration status"""
        print("\nMigration Status:")
        print("-" * 40)
        
        if not self.state['started']:
            print("No migration has been started yet.")
            return
        
        print(f"Started: {self.state['started']}")
        print(f"Status: {'Completed' if self.state['completed'] else 'In Progress'}")
        print(f"Total files: {self.state['total_files']:,}")
        print(f"Processed: {self.state['processed_files']:,}")
        print(f"Remaining: {self.state['total_files'] - self.state['processed_files']:,}")
        print(f"Failed: {len(self.state['failed_files'])}")
        
        if self.state['completed']:
            print(f"Completed at: {self.state.get('completed_at', 'Unknown')}")
        else:
            percent = (self.state['processed_files'] / self.state['total_files'] * 100) if self.state['total_files'] > 0 else 0
            print(f"Progress: {percent:.1f}%")
            print(f"Last processed: {self.state.get('last_processed', 'None')}")
    
    def reset_migration(self):
        """Reset migration state"""
        print("\nAre you sure you want to reset the migration state?")
        print("This will NOT delete extracted HTML files, only reset the progress tracking.")
        print("\nType 'yes' to confirm: ", end='')
        
        confirm = input().strip().lower()
        if confirm == 'yes':
            self.state = {
                'started': None,
                'completed': False,
                'total_files': 0,
                'processed_files': 0,
                'failed_files': [],
                'last_processed': None,
                'batches_completed': 0
            }
            self.save_state()
            print("Migration state reset.")
        else:
            print("Reset cancelled.")

def main():
    """Main migration function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate existing PDFs to include HTML extraction')
    parser.add_argument('--status', action='store_true', help='Show migration status')
    parser.add_argument('--reset', action='store_true', help='Reset migration state')
    parser.add_argument('--no-resume', action='store_true', help='Start fresh, ignore previous progress')
    args = parser.parse_args()
    
    # Change to parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    os.chdir(parent_dir)
    
    # Create migration manager
    manager = MigrationManager()
    
    if args.status:
        manager.show_status()
    elif args.reset:
        manager.reset_migration()
    else:
        manager.run_migration(resume=not args.no_resume)

if __name__ == '__main__':
    main()
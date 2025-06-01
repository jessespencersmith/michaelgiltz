#!/usr/bin/env python3
"""
Upload updated article files in batches with progress tracking
"""

import ftplib
import os
import sys
from datetime import datetime

# FTP Configuration
FTP_HOST = "ftp.michaelgiltz.com"
FTP_USER = "webmanager@michaelgiltz.com"
FTP_PASS = "ebullient-frozen-paw-vine12"
FTP_DIR = "/"

# Batch configuration
BATCH_SIZE = 500  # Upload 500 files at a time
START_BATCH = 0   # Which batch to start from (0-based)

def upload_file(ftp, local_path, remote_path):
    """Upload a single file to FTP server"""
    with open(local_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_path}', file)

def main():
    if len(sys.argv) > 1:
        START_BATCH = int(sys.argv[1])
    else:
        START_BATCH = 0
        
    print("=" * 60)
    print("GiltzWeb 2 - Batch Upload Updated Articles")
    print("=" * 60)
    
    # Get all article files
    articles_dir = "articles"
    article_files = sorted([f for f in os.listdir(articles_dir) if f.endswith('.html')])
    total_files = len(article_files)
    total_batches = (total_files + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"\nTotal files: {total_files}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Total batches: {total_batches}")
    
    # Calculate batch range
    start_idx = START_BATCH * BATCH_SIZE
    end_idx = min(start_idx + BATCH_SIZE, total_files)
    batch_files = article_files[start_idx:end_idx]
    
    if not batch_files:
        print(f"\nNo files in batch {START_BATCH}. All uploads complete!")
        return
    
    print(f"\nUploading batch {START_BATCH + 1}/{total_batches}")
    print(f"Files {start_idx + 1} to {end_idx} of {total_files}")
    
    stats = {
        'uploaded': 0,
        'failed': 0,
        'start_time': datetime.now()
    }
    
    try:
        # Connect to FTP
        print(f"\nConnecting to {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_DIR)
        
        # Ensure articles directory exists
        try:
            ftp.mkd("articles")
        except:
            pass
        
        # Upload batch
        for i, filename in enumerate(batch_files, 1):
            try:
                local_path = os.path.join(articles_dir, filename)
                remote_path = f"articles/{filename}"
                
                upload_file(ftp, local_path, remote_path)
                stats['uploaded'] += 1
                
                # Progress update every 10 files
                if i % 10 == 0:
                    progress = (start_idx + i) / total_files * 100
                    print(f"Progress: {i}/{len(batch_files)} in batch | {progress:.1f}% overall")
                    
            except Exception as e:
                print(f"Failed: {filename} - {e}")
                stats['failed'] += 1
        
        ftp.quit()
        
    except Exception as e:
        print(f"\nError: {e}")
        return
    
    # Summary
    duration = datetime.now() - stats['start_time']
    print("\n" + "=" * 60)
    print(f"Batch {START_BATCH + 1} Complete!")
    print(f"✅ Uploaded: {stats['uploaded']} files")
    if stats['failed'] > 0:
        print(f"❌ Failed: {stats['failed']} files")
    print(f"⏱️  Duration: {duration}")
    
    # Next batch info
    if end_idx < total_files:
        print(f"\n📋 Next: Run 'python3 upload_articles_batch.py {START_BATCH + 1}'")
        print(f"   to upload batch {START_BATCH + 2} ({end_idx + 1}-{min(end_idx + BATCH_SIZE, total_files)})")
    else:
        print("\n✨ All articles uploaded!")
        print("🌐 Test on: https://www.michaelgiltz.com")

if __name__ == "__main__":
    main()
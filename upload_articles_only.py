#!/usr/bin/env python3
"""
Upload only the updated article files to the server
"""

import ftplib
import os
from datetime import datetime

# FTP Configuration
FTP_HOST = "ftp.michaelgiltz.com"
FTP_USER = "webmanager@michaelgiltz.com"
FTP_PASS = "ebullient-frozen-paw-vine12"
FTP_DIR = "/"

def upload_file(ftp, local_path, remote_path):
    """Upload a single file to FTP server"""
    with open(local_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_path}', file)

def main():
    print("=" * 60)
    print("GiltzWeb 2 - Upload Updated Articles Only")
    print("=" * 60)
    
    # Count article files
    articles_dir = "articles"
    article_files = [f for f in os.listdir(articles_dir) if f.endswith('.html')]
    total_files = len(article_files)
    
    print(f"\nFound {total_files} article files to upload")
    print("Starting upload...")
    
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
        
        # Change to root directory
        ftp.cwd(FTP_DIR)
        
        # Create articles directory if it doesn't exist
        try:
            ftp.mkd("articles")
        except:
            pass  # Directory already exists
        
        # Upload articles
        print(f"\nUploading {total_files} article files...")
        for i, filename in enumerate(article_files, 1):
            try:
                local_path = os.path.join(articles_dir, filename)
                remote_path = f"articles/{filename}"
                
                upload_file(ftp, local_path, remote_path)
                stats['uploaded'] += 1
                
                if i % 100 == 0:
                    print(f"Progress: {i}/{total_files} files uploaded...")
                    
            except Exception as e:
                print(f"Failed to upload {filename}: {e}")
                stats['failed'] += 1
        
        ftp.quit()
        
    except Exception as e:
        print(f"\nError: {e}")
        return
    
    # Summary
    duration = datetime.now() - stats['start_time']
    print("\n" + "=" * 60)
    print("Upload Complete!")
    print(f"✅ Successfully uploaded: {stats['uploaded']} files")
    if stats['failed'] > 0:
        print(f"❌ Failed: {stats['failed']} files")
    print(f"⏱️  Duration: {duration}")
    print("\n✨ All article pages now have the new PDF access interface!")
    print("🌐 Test on live site: https://www.michaelgiltz.com")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Fix missing links by re-uploading HTML pages that weren't properly updated
"""

import ftplib
import os
from pathlib import Path

# FTP Configuration
FTP_HOST = "ftp.michaelgiltz.com"
FTP_USER = "webmanager@michaelgiltz.com"
FTP_PASS = "ebullient-frozen-paw-vine12"

def upload_file(ftp, local_path, remote_path):
    """Upload a single file"""
    try:
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)
        print(f"✓ Uploaded: {remote_path}")
        return True
    except Exception as e:
        print(f"✗ Failed: {remote_path} - {e}")
        return False

def main():
    print("Fixing missing links by re-uploading HTML pages...")
    print("=" * 60)
    
    # Priority files that likely have missing links
    priority_files = [
        'Parade.htm',
        'HuffingtonPost.htm', 
        'AMERICAblog.htm',
        'NYPost.htm',
        'Popsurfing.htm',
        'Advocate.htm',
        'BookFilter.htm'
    ]
    
    try:
        # Connect to FTP
        print(f"Connecting to {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✓ Connected successfully!")
        
        uploaded = 0
        
        # Upload priority files
        for html_file in priority_files:
            if os.path.exists(html_file):
                if upload_file(ftp, html_file, html_file):
                    uploaded += 1
            else:
                print(f"⚠ Warning: {html_file} not found locally")
        
        # Close connection
        ftp.quit()
        
        print("=" * 60)
        print(f"✅ Upload complete! Updated {uploaded} files")
        print("\nNext steps:")
        print("1. Check http://michaelgiltz.com/Parade.htm")
        print("2. Verify article links are working")
        print("3. Test other publication pages if needed")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    main()
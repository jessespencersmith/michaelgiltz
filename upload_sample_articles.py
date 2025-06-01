#!/usr/bin/env python3
"""
Upload a sample of updated articles to test the new PDF viewer
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
    print("Uploading sample articles to test improved PDF viewer...")
    print("=" * 60)
    
    # Sample articles to test (one from each major publication)
    test_articles = [
        'Parade-13_New_Books_About_Royals_to_Read_If_You_Have_Royal_Fever-5-20-2021.html',
        'HuffPo-Theater_Review_Hamilton_Is_Worth_The_Wait-8-5-2015.html',
        'AMERICAblog-Bush_Loses_Again-7-16-2004.html',
        'NYPost-TV_Shows_On_DVD_Part_Two_feature-12-16-2001.html',
        'Advocate-American_Idol_anti_gay_Carla_Hay-5-11-2004.html',
    ]
    
    try:
        # Connect to FTP
        print(f"Connecting to {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✓ Connected successfully!")
        
        # Make sure articles directory exists
        try:
            ftp.mkd('articles')
        except:
            pass  # Directory probably exists
        
        uploaded = 0
        
        # Upload test articles
        for article in test_articles:
            local_path = f"articles/{article}"
            if os.path.exists(local_path):
                remote_path = f"articles/{article}"
                if upload_file(ftp, local_path, remote_path):
                    uploaded += 1
            else:
                print(f"⚠ Warning: {article} not found locally")
        
        # Close connection
        ftp.quit()
        
        print("=" * 60)
        print(f"✅ Upload complete! Updated {uploaded} test articles")
        print("\nTest these URLs:")
        for article in test_articles:
            if os.path.exists(f"articles/{article}"):
                print(f"http://michaelgiltz.com/articles/{article}")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    main()
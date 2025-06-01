#!/usr/bin/env python3
"""
Upload a single file to the server
"""

import ftplib
import os
import sys

# FTP Configuration
FTP_HOST = "ftp.michaelgiltz.com"
FTP_USER = "webmanager@michaelgiltz.com"
FTP_PASS = "ebullient-frozen-paw-vine12"
FTP_DIR = "/"

def upload_file(local_path):
    """Upload a single file to the server"""
    if not os.path.exists(local_path):
        print(f"Error: File not found: {local_path}")
        return False
    
    try:
        # Connect to FTP
        print(f"Connecting to {FTP_HOST}...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_DIR)
        
        # Determine remote path
        if local_path.startswith('admin/'):
            # Ensure admin directory exists
            try:
                ftp.mkd('admin')
            except:
                pass
            remote_path = local_path
        else:
            remote_path = os.path.basename(local_path)
        
        # Upload file
        print(f"Uploading {local_path} to {remote_path}...")
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)
        
        ftp.quit()
        print(f"✅ Successfully uploaded: {local_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 upload_single_file.py <file_path>")
        print("Example: python3 upload_single_file.py Parade.htm")
        print("Example: python3 upload_single_file.py admin/index.php")
        return
    
    file_path = sys.argv[1]
    upload_file(file_path)

if __name__ == "__main__":
    main()
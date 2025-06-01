#!/usr/bin/env python3
"""
Force upload just the Parade.htm file to fix the missing links
"""

import ftplib
import os
import time

# FTP Configuration
FTP_HOST = "ftp.michaelgiltz.com"
FTP_USER = "webmanager@michaelgiltz.com"
FTP_PASS = "ebullient-frozen-paw-vine12"

def main():
    print("Force uploading Parade.htm...")
    
    try:
        # Connect to FTP
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✓ Connected to FTP")
        
        # Check current file size on server
        try:
            size = ftp.size('Parade.htm')
            print(f"Current Parade.htm on server: {size} bytes")
        except:
            print("Could not get server file size")
        
        # Check local file size
        local_size = os.path.getsize('Parade.htm')
        print(f"Local Parade.htm: {local_size} bytes")
        
        # Upload with force overwrite
        with open('Parade.htm', 'rb') as f:
            ftp.storbinary('STOR Parade.htm', f)
        print("✓ Uploaded Parade.htm")
        
        # Verify new size
        try:
            new_size = ftp.size('Parade.htm')
            print(f"New Parade.htm on server: {new_size} bytes")
            if new_size == local_size:
                print("✅ File sizes match - upload successful")
            else:
                print("⚠ File sizes don't match")
        except:
            print("Could not verify new file size")
        
        ftp.quit()
        
        print("\n" + "="*50)
        print("Upload complete!")
        print("Wait 1-2 minutes for changes to take effect")
        print("Then check: http://michaelgiltz.com/Parade.htm")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
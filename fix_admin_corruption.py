#!/usr/bin/env python3
"""
Fix the admin panel corruption issue and restore article links
"""

import os
import shutil
from datetime import datetime

def main():
    print("=" * 60)
    print("Fixing Admin Panel Corruption Issue")
    print("=" * 60)
    
    # Step 1: Backup current admin panels
    print("\n1. Backing up admin panels...")
    backup_dir = f"admin_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    if os.path.exists("admin/index.php"):
        shutil.copy2("admin/index.php", f"{backup_dir}/index.php")
        print(f"   Backed up admin/index.php")
    
    if os.path.exists("admin/index_updated.php"):
        shutil.copy2("admin/index_updated.php", f"{backup_dir}/index_updated.php")
        print(f"   Backed up admin/index_updated.php")
    
    # Step 2: Make the updated admin panel the default
    print("\n2. Setting up correct admin panel...")
    if os.path.exists("admin/index_updated.php"):
        # Rename old index.php
        if os.path.exists("admin/index.php"):
            shutil.move("admin/index.php", "admin/index_old.php")
            print("   Moved admin/index.php to admin/index_old.php")
        
        # Copy updated to index
        shutil.copy2("admin/index_updated.php", "admin/index.php")
        print("   Copied admin/index_updated.php to admin/index.php")
    
    # Step 3: Disable the old UpdateArticles.py
    print("\n3. Disabling old UpdateArticles.py...")
    if os.path.exists("UpdateArticles.py"):
        shutil.move("UpdateArticles.py", "UpdateArticles.py.disabled")
        print("   Renamed UpdateArticles.py to UpdateArticles.py.disabled")
    
    # Step 4: Re-upload the fixed Parade.htm
    print("\n4. Preparing to fix Parade.htm...")
    print("   Run: python3 upload_single_file.py Parade.htm")
    
    print("\n✅ Admin panel corruption fix complete!")
    print("\nNEXT STEPS:")
    print("1. Upload the new admin panel: python3 upload_single_file.py admin/index.php")
    print("2. Upload fixed publication pages: python3 fix_missing_links.py")
    print("3. Test the admin panel at: https://www.michaelgiltz.com/admin/")
    print("\nIMPORTANT: The admin panel will now use the correct update script")
    print("that preserves article HTML links!")

if __name__ == "__main__":
    main()
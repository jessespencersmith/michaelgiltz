#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deployment script for Michael Giltz website
Handles FTP upload to BlueHost server
"""

import os
import sys
import ftplib
import json
import glob
from datetime import datetime

class DeploymentManager:
    def __init__(self, config_file='deployment_config.json'):
        self.config_file = config_file
        self.load_config()
        
    def load_config(self):
        """Load deployment configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            # Default configuration
            self.config = {
                'host': 'ftp.michaelgiltz.com',
                'username': 'webmanager@michaelgiltz.com',
                'password': '',  # Will prompt if not set
                'remote_dir': '/public_html',
                'exclude_patterns': [
                    '*.pyc',
                    '__pycache__',
                    '.git',
                    '.DS_Store',
                    'deployment_config.json',
                    'test_*'
                ]
            }
            self.save_config()
    
    def save_config(self):
        """Save deployment configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_password(self):
        """Get FTP password"""
        if self.config['password']:
            return self.config['password']
        else:
            import getpass
            return getpass.getpass("FTP Password: ")
    
    def connect_ftp(self):
        """Connect to FTP server"""
        print(f"Connecting to {self.config['host']}...")
        
        ftp = ftplib.FTP(self.config['host'])
        ftp.login(self.config['username'], self.get_password())
        
        print(f"Connected as {self.config['username']}")
        
        # Change to remote directory
        if self.config['remote_dir']:
            ftp.cwd(self.config['remote_dir'])
            print(f"Changed to directory: {self.config['remote_dir']}")
        
        return ftp
    
    def should_exclude(self, filename):
        """Check if file should be excluded"""
        for pattern in self.config['exclude_patterns']:
            if pattern.startswith('*'):
                if filename.endswith(pattern[1:]):
                    return True
            elif pattern in filename:
                return True
        return False
    
    def upload_file(self, ftp, local_path, remote_path):
        """Upload a single file"""
        try:
            with open(local_path, 'rb') as f:
                ftp.storbinary(f'STOR {remote_path}', f)
            return True
        except Exception as e:
            print(f"  Error: {str(e)}")
            return False
    
    def create_remote_dir(self, ftp, dirname):
        """Create directory on remote server if it doesn't exist"""
        try:
            ftp.mkd(dirname)
        except ftplib.error_perm:
            # Directory might already exist
            pass
    
    def deploy_scripts(self, ftp):
        """Deploy Python scripts"""
        print("\nDeploying scripts...")
        
        # Create scripts directory
        self.create_remote_dir(ftp, 'scripts')
        ftp.cwd('scripts')
        
        # Upload scripts
        script_files = [
            'process_pdfs.py',
            'migrate_existing.py'
        ]
        
        for script in script_files:
            local_path = os.path.join('scripts', script)
            if os.path.exists(local_path):
                print(f"  Uploading {script}...")
                if self.upload_file(ftp, local_path, script):
                    # Set executable permissions
                    try:
                        ftp.voidcmd(f'SITE CHMOD 755 {script}')
                    except:
                        pass
        
        ftp.cwd('..')
    
    def deploy_admin(self, ftp):
        """Deploy admin interface"""
        print("\nDeploying admin interface...")
        
        # Create admin directory
        self.create_remote_dir(ftp, 'admin')
        ftp.cwd('admin')
        
        # Upload admin files
        admin_files = [
            'index.php',
            '.htaccess'
        ]
        
        for filename in admin_files:
            local_path = os.path.join('admin', filename)
            if os.path.exists(local_path):
                print(f"  Uploading {filename}...")
                self.upload_file(ftp, local_path, filename)
        
        ftp.cwd('..')
    
    def deploy_php_files(self, ftp):
        """Deploy PHP files"""
        print("\nDeploying PHP files...")
        
        php_files = ['search.php']
        
        for filename in php_files:
            if os.path.exists(filename):
                print(f"  Uploading {filename}...")
                self.upload_file(ftp, filename, filename)
    
    def deploy_html_files(self, ftp):
        """Deploy all HTML files"""
        print("\nDeploying HTML files...")
        
        html_files = glob.glob('*.htm')
        
        for filename in html_files:
            print(f"  Uploading {filename}...")
            self.upload_file(ftp, filename, filename)
        
        print(f"  Uploaded {len(html_files)} HTML files")
    
    def deploy_extracted_content(self, ftp):
        """Deploy extracted content"""
        print("\nDeploying extracted content...")
        
        if os.path.exists('extracted_content'):
            ftp.cwd('extracted_content')
            
            html_files = glob.glob('extracted_content/*.html')
            
            for filepath in html_files:
                filename = os.path.basename(filepath)
                print(f"  Uploading {filename}...")
                self.upload_file(ftp, filepath, filename)
            
            print(f"  Uploaded {len(html_files)} extracted HTML files")
            ftp.cwd('..')
    
    def create_directories(self, ftp):
        """Create necessary directories"""
        print("\nCreating directories...")
        
        directories = ['extracted_content', 'logs', 'backup']
        
        for dirname in directories:
            print(f"  Creating {dirname}/...")
            self.create_remote_dir(ftp, dirname)
    
    def deploy_all(self):
        """Deploy everything"""
        print("\nMichael Giltz Website Deployment")
        print("=" * 50)
        
        try:
            # Connect to FTP
            ftp = self.connect_ftp()
            
            # Create directories
            self.create_directories(ftp)
            
            # Deploy components
            self.deploy_scripts(ftp)
            self.deploy_admin(ftp)
            self.deploy_php_files(ftp)
            self.deploy_html_files(ftp)
            self.deploy_extracted_content(ftp)
            
            # Create deployment log
            print("\nCreating deployment log...")
            log_content = f"Deployed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            log_file = 'deployment.log'
            
            with open(log_file, 'w') as f:
                f.write(log_content)
            
            ftp.cwd('logs')
            self.upload_file(ftp, log_file, 'deployment.log')
            os.remove(log_file)
            
            # Close connection
            ftp.quit()
            
            print("\n✓ Deployment completed successfully!")
            
        except Exception as e:
            print(f"\n✗ Deployment failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def deploy_updates_only(self):
        """Deploy only updated files"""
        print("\nDeploying updates only...")
        
        try:
            ftp = self.connect_ftp()
            
            # Upload any modified HTML pages
            print("\nChecking for updated HTML pages...")
            html_files = glob.glob('*.htm')
            
            for html_file in html_files:
                # Check if file was modified recently (within last hour)
                mtime = os.path.getmtime(html_file)
                if (datetime.now().timestamp() - mtime) < 3600:
                    print(f"  Uploading {html_file}...")
                    self.upload_file(ftp, html_file, html_file)
            
            # Upload extracted content
            print("\nUploading extracted content...")
            ftp.cwd('extracted_content')
            
            extracted_files = glob.glob('extracted_content/*.html')[:10]  # Limit for testing
            
            for html_file in extracted_files:
                filename = os.path.basename(html_file)
                print(f"  Uploading {filename}...")
                self.upload_file(ftp, html_file, filename)
            
            ftp.quit()
            
            print("\n✓ Update deployment completed!")
            
        except Exception as e:
            print(f"\n✗ Update deployment failed: {str(e)}")

def main():
    """Main deployment function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy Michael Giltz website updates')
    parser.add_argument('--full', action='store_true', help='Full deployment (all files)')
    parser.add_argument('--updates', action='store_true', help='Deploy updates only')
    parser.add_argument('--config', action='store_true', help='Edit deployment configuration')
    args = parser.parse_args()
    
    deployer = DeploymentManager()
    
    if args.config:
        print("Edit deployment_config.json to configure deployment settings")
        print(f"Config file: {os.path.abspath('deployment_config.json')}")
    elif args.full:
        deployer.deploy_all()
    elif args.updates:
        deployer.deploy_updates_only()
    else:
        print("Usage:")
        print("  python deploy.py --full     # Full deployment")
        print("  python deploy.py --updates  # Deploy updates only")
        print("  python deploy.py --config   # Show config file location")

if __name__ == '__main__':
    main()
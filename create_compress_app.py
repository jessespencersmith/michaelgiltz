#!/usr/bin/env python3
"""
Creates a macOS drag-and-drop app for PDF compression
Run this once to create the app on your Desktop
"""

import os
import sys
import shutil
from pathlib import Path

def create_app():
    """Create the PDF Compressor app"""
    
    desktop = Path.home() / 'Desktop'
    app_path = desktop / 'PDF Compressor 72DPI.app'
    
    # Remove old app if exists
    if app_path.exists():
        shutil.rmtree(app_path)
    
    # Create app structure
    contents = app_path / 'Contents'
    macos = contents / 'MacOS'
    resources = contents / 'Resources'
    
    macos.mkdir(parents=True, exist_ok=True)
    resources.mkdir(parents=True, exist_ok=True)
    
    # Create the main script
    script_content = '''#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

def compress_pdf(pdf_path):
    """Compress a PDF file"""
    
    input_file = Path(pdf_path)
    
    # Check if it's a PDF
    if input_file.suffix.lower() != '.pdf':
        messagebox.showerror("Error", f"Not a PDF file: {input_file.name}")
        return
    
    # Get file info
    original_size = input_file.stat().st_size
    
    # Create paths
    temp_path = input_file.parent / f"temp_{input_file.name}"
    original_backup = input_file.parent / f"{input_file.stem}_original{input_file.suffix}"
    
    # Ghostscript command
    gs_command = [
        'gs',
        '-q',
        '-dNOPAUSE',
        '-dBATCH',
        '-dSAFER',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.5',
        '-dPDFSETTINGS=/screen',
        '-dDownsampleColorImages=true',
        '-dColorImageResolution=72',
        '-dDownsampleGrayImages=true',
        '-dGrayImageResolution=72',
        '-dDownsampleMonoImages=true',
        '-dMonoImageResolution=72',
        '-dCompressFonts=true',
        '-dEmbedAllFonts=false',
        '-dSubsetFonts=true',
        '-dAutoRotatePages=/None',
        '-dOptimize=true',
        f'-sOutputFile={temp_path}',
        str(input_file)
    ]
    
    try:
        # Check if Ghostscript is installed
        try:
            subprocess.run(['gs', '--version'], capture_output=True, check=True)
        except:
            messagebox.showerror("Ghostscript Required", 
                "Ghostscript is not installed!\\n\\n"
                "To install:\\n"
                "1. Open Terminal\\n"
                "2. Run: brew install ghostscript")
            return
        
        # Run compression
        result = subprocess.run(gs_command, capture_output=True, text=True)
        
        if not temp_path.exists() or temp_path.stat().st_size == 0:
            messagebox.showerror("Error", "Compression failed")
            return
        
        # Get compressed size
        compressed_size = temp_path.stat().st_size
        reduction_pct = (1 - compressed_size / original_size) * 100
        
        # Rename original to backup
        input_file.rename(original_backup)
        
        # Move compressed to original name
        temp_path.rename(input_file)
        
        # Show success message
        message = f"Compression successful!\\n\\n"
        message += f"Original: {original_size / 1024 / 1024:.1f} MB\\n"
        message += f"Compressed: {compressed_size / 1024:.0f} KB\\n"
        message += f"Reduction: {reduction_pct:.0f}%\\n\\n"
        message += f"Files:\\n"
        message += f"• {input_file.name} (compressed)\\n"
        message += f"• {original_backup.name} (original backup)"
        
        messagebox.showinfo("PDF Compressed", message)
        
    except Exception as e:
        messagebox.showerror("Error", f"Compression failed: {str(e)}")
        # Clean up temp file if it exists
        if temp_path.exists():
            temp_path.unlink()

def main():
    """Main function"""
    # Hide the main window
    root = tk.Tk()
    root.withdraw()
    
    # Process dropped files
    if len(sys.argv) > 1:
        for pdf_file in sys.argv[1:]:
            if os.path.exists(pdf_file):
                compress_pdf(pdf_file)
    else:
        messagebox.showinfo("PDF Compressor", 
            "Drop PDF files onto this app to compress them to 72 DPI.\\n\\n"
            "Original files will be renamed with '_original' suffix.")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
'''
    
    script_path = macos / 'compress_pdf'
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod(script_path, 0o755)
    
    # Create Info.plist
    info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>compress_pdf</string>
    <key>CFBundleIdentifier</key>
    <string>com.michaelgiltz.pdfcompressor</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>PDF Compressor 72DPI</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.10</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>pdf</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>PDF Document</string>
            <key>CFBundleTypeRole</key>
            <string>Editor</string>
            <key>LSHandlerRank</key>
            <string>Alternate</string>
        </dict>
    </array>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>'''
    
    plist_path = contents / 'Info.plist'
    with open(plist_path, 'w') as f:
        f.write(info_plist)
    
    # Create a simple icon (you can replace this with a proper icon later)
    icon_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
    <rect width="512" height="512" fill="#FF6B6B" rx="80"/>
    <text x="256" y="200" font-family="Arial, sans-serif" font-size="120" font-weight="bold" text-anchor="middle" fill="white">PDF</text>
    <text x="256" y="320" font-family="Arial, sans-serif" font-size="80" text-anchor="middle" fill="white">72 DPI</text>
    <path d="M 150 380 L 360 380 L 330 420 L 180 420 Z" fill="white" opacity="0.8"/>
</svg>'''
    
    icon_path = resources / 'icon.svg'
    with open(icon_path, 'w') as f:
        f.write(icon_content)
    
    print(f"✅ Created app: {app_path}")
    print("\nHow to use:")
    print("1. Find 'PDF Compressor 72DPI' on your Desktop")
    print("2. Drag any PDF onto the app icon")
    print("3. The PDF will be compressed automatically")
    print("\nNote: Original files are preserved with '_original' suffix")

if __name__ == "__main__":
    create_app()
#!/usr/bin/env python3
"""
PDF Folder Compressor
====================

Put PDFs in a folder called "PDFs to Compress" on your Desktop.
Run this script to compress all PDFs in that folder.
"""

import os
import subprocess
from pathlib import Path
import time

def check_ghostscript():
    """Check if Ghostscript is installed"""
    try:
        subprocess.run(['gs', '--version'], capture_output=True, check=True)
        return True
    except:
        print("❌ Ghostscript is required but not installed!")
        print("Install with: brew install ghostscript")
        return False

def compress_pdf(input_path, output_path):
    """Compress a single PDF"""
    # Ghostscript command with better balance of size/quality
    gs_command = [
        'gs',
        '-q',
        '-dNOPAUSE',
        '-dBATCH',
        '-dSAFER',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.5',
        '-dPDFSETTINGS=/ebook',  # Better than /screen for rendering
        '-dDownsampleColorImages=true',
        '-dColorImageResolution=150',  # 150 DPI instead of 72
        '-dDownsampleGrayImages=true',
        '-dGrayImageResolution=150',
        '-dDownsampleMonoImages=true',
        '-dMonoImageResolution=300',  # Higher for text clarity
        '-dCompressFonts=true',
        '-dEmbedAllFonts=true',  # Embed fonts for better rendering
        '-dSubsetFonts=true',
        '-dAutoRotatePages=/None',
        '-dOptimize=true',
        '-dFastWebView=true',  # Optimize for web viewing
        f'-sOutputFile={output_path}',
        str(input_path)
    ]
    
    try:
        result = subprocess.run(gs_command, capture_output=True, text=True)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except:
        return False

def main():
    """Main function"""
    print("PDF FOLDER COMPRESSOR")
    print("=" * 50)
    
    # Check Ghostscript
    if not check_ghostscript():
        return
    
    # Set up folders
    desktop = Path.home() / 'Desktop'
    input_folder = desktop / 'PDFs to Compress'
    output_folder = desktop / 'Compressed PDFs'
    original_folder = desktop / 'Original PDFs'
    
    # Create input folder if it doesn't exist
    if not input_folder.exists():
        input_folder.mkdir()
        print(f"\n📁 Created folder: {input_folder}")
        print("\n📝 Instructions:")
        print("1. Put PDF files in 'PDFs to Compress' folder on Desktop")
        print("2. Run this script again")
        return
    
    # Find PDFs in input folder
    pdf_files = list(input_folder.glob('*.pdf')) + list(input_folder.glob('*.PDF'))
    
    if not pdf_files:
        print(f"\n❌ No PDF files found in: {input_folder}")
        print("\nPut PDF files in this folder and run again.")
        return
    
    print(f"\n📄 Found {len(pdf_files)} PDF(s) to compress")
    
    # Create output folders
    output_folder.mkdir(exist_ok=True)
    original_folder.mkdir(exist_ok=True)
    
    # Process each PDF
    success_count = 0
    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")
        
        # Get file size
        original_size = pdf_path.stat().st_size
        print(f"  Original size: {original_size / 1024 / 1024:.1f} MB")
        
        # Create output path
        output_path = output_folder / pdf_path.name
        
        # Compress
        if compress_pdf(pdf_path, output_path):
            compressed_size = output_path.stat().st_size
            reduction = (1 - compressed_size / original_size) * 100
            print(f"  ✅ Compressed: {compressed_size / 1024:.0f} KB ({reduction:.0f}% smaller)")
            print(f"  📁 Saved to: Compressed PDFs/{output_path.name}")
            
            # Move original to Original PDFs folder
            original_path = original_folder / pdf_path.name
            pdf_path.rename(original_path)
            print(f"  📁 Original moved to: Original PDFs/{pdf_path.name}")
            
            success_count += 1
        else:
            print(f"  ❌ Compression failed")
    
    print(f"\n{'='*50}")
    print(f"✅ Complete! Compressed {success_count} of {len(pdf_files)} PDFs")
    print(f"\n📁 Compressed files in: Compressed PDFs")
    print("📁 Original files in: Original PDFs")

if __name__ == "__main__":
    main()
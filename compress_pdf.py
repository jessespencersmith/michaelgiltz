#!/usr/bin/env python3
"""
PDF Compressor Tool
==================

Compresses existing PDFs by downsampling images to 72 DPI.
Saves compressed version with original name and renames original to filename_original.pdf

Requirements:
- Ghostscript: brew install ghostscript

Usage:
    python3 compress_pdf.py <pdf_file>
    
Example:
    python3 compress_pdf.py ~/Desktop/Variety-Oscar_News-01-26-2024.pdf
"""

import os
import sys
import subprocess
from pathlib import Path


def check_ghostscript():
    """Check if Ghostscript is installed"""
    try:
        subprocess.run(['gs', '--version'], capture_output=True, check=True)
        return True
    except:
        print("❌ Ghostscript is required but not installed!")
        print("Install with: brew install ghostscript")
        return False


def compress_pdf(input_path):
    """Compress PDF using Ghostscript with 72 DPI images"""
    
    input_file = Path(input_path)
    
    # Check if file exists
    if not input_file.exists():
        print(f"❌ File not found: {input_path}")
        return False
    
    # Check if it's a PDF
    if input_file.suffix.lower() != '.pdf':
        print(f"❌ Not a PDF file: {input_path}")
        return False
    
    # Get file info
    original_size = input_file.stat().st_size
    print(f"\nOriginal file: {input_file.name}")
    print(f"Original size: {original_size / 1024 / 1024:.1f} MB")
    
    # Create paths
    temp_path = input_file.parent / f"temp_{input_file.name}"
    original_backup = input_file.parent / f"{input_file.stem}_original{input_file.suffix}"
    
    print("\nCompressing PDF (72 DPI images)...")
    
    # Ghostscript command for 72 DPI compression
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
        '-dColorImageDownsampleThreshold=1.0',
        '-dDownsampleGrayImages=true',
        '-dGrayImageResolution=72',
        '-dGrayImageDownsampleThreshold=1.0',
        '-dDownsampleMonoImages=true',
        '-dMonoImageResolution=72',
        '-dMonoImageDownsampleThreshold=1.0',
        '-dCompressFonts=true',
        '-dEmbedAllFonts=false',
        '-dSubsetFonts=true',
        '-dAutoRotatePages=/None',
        '-dOptimize=true',
        '-dDetectDuplicateImages=true',
        f'-sOutputFile={temp_path}',
        str(input_file)
    ]
    
    try:
        # Run compression
        result = subprocess.run(gs_command, capture_output=True, text=True)
        
        if result.returncode != 0 and result.stderr:
            print(f"Warning: {result.stderr}")
        
        # Check if output was created
        if not temp_path.exists() or temp_path.stat().st_size == 0:
            print("❌ Compression failed - no output created")
            return False
        
        # Get compressed size
        compressed_size = temp_path.stat().st_size
        reduction_pct = (1 - compressed_size / original_size) * 100
        
        print(f"\n✅ Compression successful!")
        print(f"Compressed size: {compressed_size / 1024:.0f} KB")
        print(f"Size reduction: {reduction_pct:.0f}%")
        
        # Check if compression actually reduced size
        if compressed_size >= original_size:
            print("\n⚠️  Compressed file is not smaller than original")
            response = input("Keep compressed version anyway? (y/N): ").strip().lower()
            if response != 'y':
                temp_path.unlink()
                print("Compression cancelled - original file unchanged")
                return False
        
        # Rename original to backup
        print(f"\nRenaming original to: {original_backup.name}")
        input_file.rename(original_backup)
        
        # Move compressed to original name
        temp_path.rename(input_file)
        
        print(f"\n✅ Complete!")
        print(f"   Compressed: {input_file.name} ({compressed_size / 1024:.0f} KB)")
        print(f"   Original backup: {original_backup.name} ({original_size / 1024 / 1024:.1f} MB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during compression: {e}")
        # Clean up temp file if it exists
        if temp_path.exists():
            temp_path.unlink()
        return False


def main():
    """Main function"""
    print("PDF COMPRESSOR - 72 DPI")
    print("=" * 50)
    
    # Check requirements
    if not check_ghostscript():
        sys.exit(1)
    
    # Check arguments
    if len(sys.argv) != 2:
        print("\nUsage: python3 compress_pdf.py <pdf_file>")
        print("\nExample:")
        print("  python3 compress_pdf.py ~/Desktop/article.pdf")
        print("\nYou can also drag and drop a PDF file onto Terminal")
        sys.exit(1)
    
    # Get PDF path
    pdf_path = sys.argv[1].strip()
    
    # Handle paths with spaces (from drag and drop)
    if pdf_path.startswith("'") and pdf_path.endswith("'"):
        pdf_path = pdf_path[1:-1]
    
    # Compress the PDF
    compress_pdf(pdf_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
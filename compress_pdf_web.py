#!/usr/bin/env python3
"""
PDF Compressor specifically for fast web viewing
Uses qpdf for linearization after ghostscript compression
"""

import os
import subprocess
from pathlib import Path
import shutil

def compress_pdf_for_web(input_path, output_path):
    """Compress PDF with maximum web optimization"""
    
    # First, use Ghostscript for compression
    temp_path = output_path.parent / f"temp_{output_path.name}"
    
    gs_command = [
        'gs',
        '-q',
        '-dNOPAUSE',
        '-dBATCH',
        '-dSAFER',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/screen',
        '-dDownsampleColorImages=true',
        '-dColorImageResolution=72',
        '-dDownsampleGrayImages=true', 
        '-dGrayImageResolution=72',
        '-dDownsampleMonoImages=true',
        '-dMonoImageResolution=150',
        '-dCompressFonts=true',
        '-dEmbedAllFonts=false',
        '-dSubsetFonts=true',
        '-dAutoRotatePages=/None',
        '-dOptimize=true',
        '-dFastWebView=true',
        '-dConvertCMYKImagesToRGB=true',
        '-dCompressPages=true',
        '-dUseCIEColor=false',  # Faster color handling
        '-dProcessColorModel=/DeviceRGB',  # Force RGB
        '-dCompatibilityLevel=1.4',  # Better web compatibility
        f'-sOutputFile={temp_path}',
        str(input_path)
    ]
    
    try:
        # Run Ghostscript
        print("  Compressing with Ghostscript...")
        result = subprocess.run(gs_command, capture_output=True, text=True)
        
        if not temp_path.exists():
            print("  ❌ Ghostscript compression failed")
            return False
            
        # Try to linearize with qpdf if available
        try:
            print("  Linearizing for web...")
            qpdf_cmd = ['qpdf', '--linearize', str(temp_path), str(output_path)]
            subprocess.run(qpdf_cmd, capture_output=True, check=True)
            temp_path.unlink()  # Remove temp file
            print("  ✅ Linearized with qpdf")
            return True
        except:
            # qpdf not available, just use ghostscript output
            shutil.move(str(temp_path), str(output_path))
            print("  ⚠️  qpdf not found - using Ghostscript output only")
            print("     Install qpdf for better web optimization: brew install qpdf")
            return True
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        if temp_path.exists():
            temp_path.unlink()
        return False


def main():
    """Process all PDFs in the input folder"""
    
    desktop = Path.home() / 'Desktop'
    input_folder = desktop / 'PDFs to Compress'
    output_folder = desktop / 'Compressed PDFs'
    original_folder = desktop / 'Original PDFs'
    
    # Create folders
    output_folder.mkdir(exist_ok=True)
    original_folder.mkdir(exist_ok=True)
    
    # Find PDFs
    pdf_files = list(input_folder.glob('*.pdf')) + list(input_folder.glob('*.PDF'))
    
    if not pdf_files:
        print("No PDFs found in 'PDFs to Compress' folder")
        return
        
    print(f"Found {len(pdf_files)} PDFs to compress for web")
    print("=" * 50)
    
    success_count = 0
    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")
        
        original_size = pdf_path.stat().st_size
        print(f"  Original size: {original_size / 1024 / 1024:.1f} MB")
        
        output_path = output_folder / pdf_path.name
        
        if compress_pdf_for_web(pdf_path, output_path):
            compressed_size = output_path.stat().st_size
            reduction = (1 - compressed_size / original_size) * 100
            print(f"  ✅ Compressed: {compressed_size / 1024:.0f} KB ({reduction:.0f}% smaller)")
            
            # Move original
            original_path = original_folder / pdf_path.name
            pdf_path.rename(original_path)
            success_count += 1
        else:
            print(f"  ❌ Compression failed")
    
    print("\n" + "=" * 50)
    print(f"✅ Complete! Compressed {success_count} PDFs")
    print("\nTo install qpdf for better web optimization:")
    print("  brew install qpdf")


if __name__ == "__main__":
    main()
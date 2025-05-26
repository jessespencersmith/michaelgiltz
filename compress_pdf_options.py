#!/usr/bin/env python3
"""
PDF Compressor with Options
===========================

Choose between:
1. Maximum compression (72 DPI) - Smallest files
2. Balanced (100 DPI) - Good quality, fast rendering
3. High quality (150 DPI) - Best quality, larger files
"""

import os
import sys
import subprocess
from pathlib import Path


def compress_pdf(input_path, output_path, quality="balanced"):
    """Compress PDF with different quality options"""
    
    # Base command
    gs_command = [
        'gs',
        '-q',
        '-dNOPAUSE',
        '-dBATCH',
        '-dSAFER',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dAutoRotatePages=/None',
        '-dOptimize=true',
        '-dFastWebView=true',
    ]
    
    # Quality-specific settings
    if quality == "max":
        # Maximum compression - smallest files
        gs_command.extend([
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
        ])
    elif quality == "high":
        # High quality - larger files
        gs_command.extend([
            '-dPDFSETTINGS=/printer',
            '-dDownsampleColorImages=true',
            '-dColorImageResolution=150',
            '-dDownsampleGrayImages=true',
            '-dGrayImageResolution=150',
            '-dDownsampleMonoImages=true',
            '-dMonoImageResolution=300',
            '-dCompressFonts=true',
            '-dEmbedAllFonts=true',
            '-dSubsetFonts=true',
        ])
    else:  # balanced
        # Balanced - fast rendering
        gs_command.extend([
            '-dPDFSETTINGS=/ebook',
            '-dDownsampleColorImages=true',
            '-dColorImageResolution=100',
            '-dDownsampleGrayImages=true',
            '-dGrayImageResolution=100',
            '-dDownsampleMonoImages=true',
            '-dMonoImageResolution=200',
            '-dCompressFonts=true',
            '-dEmbedAllFonts=true',
            '-dSubsetFonts=true',
            '-dMaxInlineImageSize=4000',
            '-dConvertCMYKImagesToRGB=true',
            '-dDetectDuplicateImages=true',
        ])
    
    # Add output file
    gs_command.extend([
        f'-sOutputFile={output_path}',
        str(input_path)
    ])
    
    try:
        result = subprocess.run(gs_command, capture_output=True, text=True)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except:
        return False


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("PDF Compressor with Options")
        print("===========================")
        print("")
        print("Usage: python3 compress_pdf_options.py <pdf_file> [quality]")
        print("")
        print("Quality options:")
        print("  max      - Maximum compression (72 DPI)")
        print("  balanced - Balanced quality/size (100 DPI) [default]")
        print("  high     - High quality (150 DPI)")
        print("")
        print("Example:")
        print("  python3 compress_pdf_options.py document.pdf max")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    quality = sys.argv[2] if len(sys.argv) > 2 else "balanced"
    
    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        sys.exit(1)
    
    # Create output path
    output_path = pdf_path.parent / f"{pdf_path.stem}_compressed{pdf_path.suffix}"
    
    print(f"Compressing with {quality} quality...")
    print(f"Input: {pdf_path.name}")
    
    # Get original size
    original_size = pdf_path.stat().st_size
    
    # Compress
    if compress_pdf(pdf_path, output_path, quality):
        compressed_size = output_path.stat().st_size
        reduction = (1 - compressed_size / original_size) * 100
        
        print(f"\n✅ Success!")
        print(f"Original: {original_size / 1024 / 1024:.1f} MB")
        print(f"Compressed: {compressed_size / 1024:.0f} KB")
        print(f"Reduction: {reduction:.0f}%")
        print(f"Output: {output_path.name}")
    else:
        print("❌ Compression failed")


if __name__ == "__main__":
    main()
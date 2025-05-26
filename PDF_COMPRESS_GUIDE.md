# PDF Compression Tool

This tool compresses existing PDF files by downsampling images to 72 DPI, dramatically reducing file size.

## How It Works

- Takes any PDF file as input
- Compresses images to 72 DPI (same as the article archiver)
- Saves compressed version with the **original filename**
- Renames original to `filename_original.pdf` as backup

## Usage

### Method 1: Command Line
```bash
cd "/Users/spencejb/Documents/GiltzWeb 2"
python3 compress_pdf.py ~/Desktop/your-article.pdf
```

### Method 2: Drag and Drop
1. Open Terminal
2. Type: `cd "/Users/spencejb/Documents/GiltzWeb 2" && python3 compress_pdf.py `
3. Drag the PDF file from Finder into Terminal
4. Press Enter

## Example

```
PDF COMPRESSOR - 72 DPI
==================================================

Original file: Variety-Oscar_News-01-26-2024.pdf
Original size: 8.7 MB

Compressing PDF (72 DPI images)...

✅ Compression successful!
Compressed size: 412 KB
Size reduction: 95%

Renaming original to: Variety-Oscar_News-01-26-2024_original.pdf

✅ Complete!
   Compressed: Variety-Oscar_News-01-26-2024.pdf (412 KB)
   Original backup: Variety-Oscar_News-01-26-2024_original.pdf (8.7 MB)
```

## What You Get

After running:
- `Variety-Oscar_News-01-26-2024.pdf` - Compressed version (small)
- `Variety-Oscar_News-01-26-2024_original.pdf` - Original backup (large)

## Tips

- Works with any PDF, not just articles
- Typical compression: 90-95% size reduction
- Original is always preserved as backup
- If compression doesn't reduce size, it asks before replacing

## Requirements

Just Ghostscript:
```bash
brew install ghostscript
```
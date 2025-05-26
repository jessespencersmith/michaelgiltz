# PDF Compressor App

A drag-and-drop macOS app for compressing PDFs to 72 DPI.

## Installation

The app has been created on your Desktop as **"PDF Compressor 72DPI"**

If you need to recreate it:
```bash
cd "/Users/spencejb/Documents/GiltzWeb 2"
python3 create_compress_app.py
```

## How to Use

1. **Find the app** on your Desktop - red icon labeled "PDF Compressor 72DPI"

2. **Drag a PDF** file onto the app icon

3. **Wait for compression** - A dialog will show the results

4. **Check your files**:
   - `filename.pdf` - Now the compressed version
   - `filename_original.pdf` - Your original backup

## What It Does

- Compresses images to 72 DPI
- Typically reduces file size by 90-95%
- Preserves original as backup
- Shows compression statistics in a popup

## Example Results

Drag: `Variety-Article-01-26-2024.pdf` (8.7 MB)

Get:
- `Variety-Article-01-26-2024.pdf` (412 KB) - Compressed
- `Variety-Article-01-26-2024_original.pdf` (8.7 MB) - Original backup

## Multiple Files

You can drag multiple PDFs at once - each will be compressed with its own popup showing results.

## Troubleshooting

**"Ghostscript is not installed" error**
- Open Terminal
- Run: `brew install ghostscript`
- Try again

**App won't open (security warning)**
- Right-click the app
- Choose "Open"
- Click "Open" in the dialog

**Nothing happens when dragging**
- Make sure you're dragging PDF files
- Try opening the app first (double-click) for instructions

## Tips

- Works with any PDF, not just articles
- Original is always preserved
- Great for email attachments
- Can process batches of PDFs
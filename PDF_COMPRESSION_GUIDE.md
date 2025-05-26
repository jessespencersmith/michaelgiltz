# PDF Compression Guide

This tool compresses PDFs for fast web viewing with small file sizes.

## Setup (One Time)

The compression tool is already on your Desktop as **"Compress PDFs on Desktop.command"**

## How to Use

1. **Put PDFs** in the **"PDFs to Compress"** folder on your Desktop

2. **Double-click** the **"Compress PDFs on Desktop.command"** file

3. **Find your files**:
   - **Compressed PDFs** folder - Your compressed files (small, fast-loading)
   - **Original PDFs** folder - Your original files (backup)

## What It Does

- Compresses images to 72 DPI
- Reduces file size by ~90%
- Optimizes for fast web viewing
- Creates linearized PDFs (load page-by-page)
- Converts to RGB for faster browser rendering

## Example

Drop: `Article.pdf` (8 MB)

Get:
- `Compressed PDFs/Article.pdf` (400 KB) - Fast web version
- `Original PDFs/Article.pdf` (8 MB) - Original backup

## Folders on Desktop

- **PDFs to Compress** - Put files here
- **Compressed PDFs** - Get results here  
- **Original PDFs** - Originals moved here

## Requirements

- Ghostscript (already installed)
- qpdf (installs automatically if needed)
# Simple Article PDF Archiver - Instructions

This tool saves web articles as compressed PDFs on your Desktop.

## Setup (One Time Only)

1. **Install Ghostscript** (for compression):
   ```bash
   brew install ghostscript
   ```

2. **Install Playwright** (for PDF creation):
   ```bash
   pip3 install playwright
   playwright install chromium
   ```

## How to Use

1. **Open Terminal**

2. **Navigate to GiltzWeb folder**:
   ```bash
   cd "/Users/spencejb/Documents/GiltzWeb 2"
   ```

3. **Run the archiver**:
   ```bash
   python3 archive_article_simple.py
   ```

4. **Enter the article URL** when prompted

5. **Enter the filename** following this format:
   ```
   Publication-Article_Title-MM-DD-YYYY
   ```
   
   Examples:
   - `Variety-Oscar_Nominations_2024-01-23-2024`
   - `HollywoodReporter-Box_Office_Report-02-15-2024`
   - `NYTimes-Theater_Review_Hamlet-03-10-2024`

6. **Confirm the filename** when prompted

7. **Find your compressed PDF on the Desktop**

## Example Session

```
SIMPLE ARTICLE PDF ARCHIVER
============================================================

Enter article URL: https://variety.com/2024/tv/news/succession-wins-emmys

============================================================
FILENAME FORMAT:
Publication-Article_Title-MM-DD-YYYY.pdf

Examples:
  Variety-Oscar_Nominations_2024-01-23-2024.pdf
  HollywoodReporter-Box_Office_Report-02-15-2024.pdf
  NYTimes-Theater_Review_Hamlet-03-10-2024.pdf
============================================================

Enter filename (without .pdf): Variety-Succession_Wins_Emmys-01-15-2024

Filename: Variety-Succession_Wins_Emmys-01-15-2024.pdf
Is this correct? (Y/n): Y

Generating PDF from webpage...
✓ PDF created: 8.7 MB

Compressing PDF...
Original size: 8.7 MB
✓ Compressed size: 412 KB
✓ Size reduction: 95%

============================================================
✅ SUCCESS!
✅ Saved to Desktop: Variety-Succession_Wins_Emmys-01-15-2024.pdf
✅ Final size: 412 KB
============================================================
```

## Tips

- Use underscores (_) instead of spaces in the title
- Keep the date format as MM-DD-YYYY (with hyphens)
- The tool will add .pdf automatically
- Press Y or Enter to confirm the filename
- Type n to re-enter if you made a mistake

## Troubleshooting

**"Ghostscript NOT installed"**
```bash
brew install ghostscript
```

**"Playwright NOT installed"**
```bash
pip3 install playwright
playwright install chromium
```

**PDF looks bad or has ads**
- The tool tries to remove ads automatically
- Some sites may still have formatting issues
- The PDF will be readable but may not be perfect

**Compression didn't work**
- The tool will save an uncompressed version if compression fails
- Make sure Ghostscript is installed for compression
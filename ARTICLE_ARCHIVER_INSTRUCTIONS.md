# Entertainment Article PDF Archiver - Instructions

This tool converts entertainment articles into space-efficient PDFs on your Desktop.

## Installation (One Time Only)

1. **Install Ghostscript** (REQUIRED for compression):
   ```
   brew install ghostscript
   ```

2. **Install wkhtmltopdf** (REQUIRED for PDF creation):
   ```
   brew install --cask wkhtmltopdf
   ```

## How to Use

1. **Open Terminal**

2. **Navigate to GiltzWeb folder**:
   ```
   cd "/Users/spencejb/Documents/GiltzWeb 2"
   ```

3. **Run the archiver**:
   ```
   python3 archive_article_tool.py
   ```

4. **Enter the article URL** when prompted

5. **Create the filename interactively**:
   - Enter or confirm the PUBLICATION name
   - Enter or confirm the ARTICLE TITLE
   - Enter or confirm the DATE (MM-DD-YYYY format)

6. **The compressed PDF will be saved to your Desktop**

## Example Session

```
Enter article URL: https://variety.com/2024/tv/news/succession-wins-emmys

FILENAME CREATION
==================================
1. PUBLICATION NAME
   Suggested: Variety
   Enter publication name (or press Enter to use suggestion): [Enter]

2. ARTICLE TITLE  
   Suggested: Succession Wins Emmys
   Enter article title (or press Enter to use suggestion): [Enter]

3. PUBLICATION DATE (MM-DD-YYYY)
   Suggested: 01-15-2024
   Enter date (or press Enter for suggestion): [Enter]

4. FINAL FILENAME
   Variety-Succession_Wins_Emmys-01-15-2024.pdf
   Is this correct? (Y/n): Y

Generating PDF from webpage...
✓ PDF created: 8.7 MB

Compressing PDF with Ghostscript...
Target: Downsample images to 72 DPI
Original size: 8.7 MB
✓ Compressed size: 412 KB
✓ Size reduction: 95%

SUCCESS!
✅ Saved to Desktop: Variety-Succession_Wins_Emmys-01-15-2024.pdf
✅ Final size: 412 KB
```

## Key Features

- **Interactive naming**: You control the exact filename
- **Automatic compression**: Images reduced to 72 DPI
- **Space efficient**: Typically reduces file size by 90%+
- **Smart suggestions**: Extracts title and date when possible

## Filename Format

All files follow this pattern:
```
Publication-Title_of_Article-MM-DD-YYYY.pdf
```

Examples:
- `Variety-Oscar_Nominations_Announced-01-23-2024.pdf`
- `HollywoodReporter-Box_Office_Report-02-01-2024.pdf`
- `Deadline-TV_Pilot_Season_Update-03-15-2024.pdf`

## Troubleshooting

**"Ghostscript NOT installed"**
- Run: `brew install ghostscript`

**"wkhtmltopdf NOT installed"**
- Run: `brew install --cask wkhtmltopdf`

**PDF creation fails**
- Check the URL is correct
- Some sites may block automated access
- Try a different article from the same site

## Supported Sites

Works with all major entertainment sites including:
- Variety, Hollywood Reporter, Deadline
- Entertainment Weekly, Rolling Stone, Billboard
- Vulture, AV Club, IndieWire
- New York Times, LA Times, Guardian
- And many more...

## Tips

- The tool will suggest publication names for known sites
- It tries to extract the article title automatically
- Dates can be entered in multiple formats (MM-DD-YYYY, MM/DD/YYYY, etc.)
- Press Enter to accept suggestions during filename creation
- Type 'n' at the confirmation to start over if needed
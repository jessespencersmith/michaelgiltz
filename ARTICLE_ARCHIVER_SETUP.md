# Article PDF Archiver - Setup & Usage

## Quick Setup (Both Laptops)

Since wkhtmltopdf is discontinued, we're using Playwright instead.

### 1. Install Ghostscript (for compression)
```bash
brew install ghostscript
```

### 2. Install Playwright (for PDF creation)
```bash
pip3 install playwright
playwright install chromium
```

That's it! The tool is ready to use.

## How to Use

1. **Open Terminal**

2. **Go to the GiltzWeb folder**:
```bash
cd "/Users/spencejb/Documents/GiltzWeb 2"
```

3. **Run the archiver**:
```bash
python3 archive_article_tool_v2.py
```

4. **Follow the prompts**:
   - Enter the article URL
   - Confirm or edit the publication name
   - Confirm or edit the article title  
   - Confirm or edit the date
   - Confirm the final filename

5. **Find your PDF on the Desktop**

## Example

```
Enter article URL: https://variety.com/2024/tv/news/succession-wins-emmys

FILENAME CREATION
================
1. PUBLICATION NAME
   Suggested: Variety
   Enter publication name: [press Enter]

2. ARTICLE TITLE
   Suggested: Succession Wins Emmys
   Enter article title: [press Enter]

3. PUBLICATION DATE (MM-DD-YYYY)
   Suggested: 01-26-2024
   Enter date: [press Enter]

4. FINAL FILENAME
   Variety-Succession_Wins_Emmys-01-26-2024.pdf
   Is this correct? (Y/n): Y

Result: 8.7 MB PDF compressed to 412 KB (95% reduction)
```

## Troubleshooting

**"pip3: command not found"**
- Install Python 3: `brew install python3`

**"Playwright NOT installed"**
```bash
pip3 install playwright
playwright install chromium
```

**"Ghostscript NOT installed"**
```bash
brew install ghostscript
```

**PDF creation fails**
- Check internet connection
- Try a different article
- Make sure Playwright is installed correctly

## Tips

- The tool suggests publication names for major sites
- It tries to extract article titles automatically
- Press Enter to accept suggestions
- Type 'n' to redo the filename if needed
- PDFs are compressed to ~400KB typically
# Web Article PDF Archiver

This tool helps you save web articles as compressed PDFs on your Desktop.

## Quick Start

1. Open Terminal
2. Navigate to the GiltzWeb 2 folder:
   ```
   cd "/Users/spencejb/Documents/GiltzWeb 2"
   ```

3. Run the archiver:
   ```
   python3 archive_web_article.py
   ```

4. Paste the article URL when prompted

The PDF will be saved to your Desktop with a filename like:
`Variety-Article_Title_Here-01-26-2024.pdf`

## Features

- **Automatic naming**: Extracts publication name, article title, and date
- **Compression**: Reduces file size significantly (optional, requires Ghostscript)
- **Works with major sites**: Variety, Hollywood Reporter, Deadline, NYTimes, etc.
- **Simple to use**: Just paste the URL and press Enter

## Optional: Install Ghostscript for Better Compression

Ghostscript can reduce PDF file sizes by 50-90%. To install:

1. Open Terminal
2. Run: `brew install ghostscript`

Without Ghostscript, PDFs will still be created but won't be compressed.

## Examples

**Input:** https://variety.com/2024/tv/news/some-show-renewed-season-2
**Output:** Variety-Some_Show_Renewed_Season_2-01-26-2024.pdf

**Input:** https://www.hollywoodreporter.com/movies/movie-news/oscar-nominations-2024
**Output:** HollywoodReporter-Oscar_Nominations_2024-01-26-2024.pdf

## Troubleshooting

**"No module named 'weasyprint'" error:**
- This is fine - the tool will use alternative methods

**PDF not created:**
- Check your internet connection
- Make sure the URL is correct
- Some sites may block automated access

**File size too large:**
- Install Ghostscript: `brew install ghostscript`
- The tool will automatically compress PDFs when Ghostscript is available

## Supported Sites

The tool recognizes 100+ publications including:
- Entertainment: Variety, THR, Deadline, IndieWire, EW
- Music: Rolling Stone, Billboard, Pitchfork, NME
- Culture: Vulture, AV Club, Slate, Salon
- News: NYTimes, WashPost, Guardian, BBC
- And many more...

For sites not in the list, it will use the domain name as the publication.

## Technical Notes

- Uses PrintFriendly and Web2PDF services as fallbacks
- Compresses images to 150 DPI for balance of quality and size
- Handles special characters in titles automatically
- Date extraction works with most standard article formats
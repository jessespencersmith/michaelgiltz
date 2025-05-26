# New Workflow for michaelgiltz.com - Combined PDF+Text Pages

## Overview
The website has been upgraded to use combined HTML pages that include both an embedded PDF viewer and extracted text content. This provides better SEO, faster loading, and improved user experience.

## Key Changes

### 1. Article Display
- **Before**: Direct links to PDF files that required download
- **After**: HTML pages with embedded PDF viewer and searchable text

### 2. File Structure
```
GiltzWeb 2/
├── articles/          # NEW: Contains all combined HTML pages (4,213 files)
├── scans/            # Original PDFs (unchanged)
├── scripts/
│   ├── create_combined_pages.py    # Creates combined pages
│   └── process_new_pdfs.py        # NEW: Processes new PDFs
└── admin/
    └── index.php     # Updated admin panel
```

### 3. How Combined Pages Work
Each article now has an HTML page with:
- michaelgiltz.com banner at top
- Embedded PDF viewer (using iframe)
- HOME button for navigation
- Extracted text content for SEO
- Clean, consistent formatting

## Workflow for New Articles

### Option 1: Archive Web Articles
1. Use `archive_article_simple.py` to convert web articles to PDFs
2. Enter filename in format: `Publication-Title-MM-DD-YYYY.pdf`
3. Upload PDF to server's `scans/` folder
4. Run admin panel to process

### Option 2: Upload Existing PDFs
1. Ensure PDF follows naming format: `Publication-Title-MM-DD-YYYY.pdf`
2. Upload to `scans/` folder via FTP
3. Visit admin panel and click "Process New PDFs"

### Option 3: Local Processing (Advanced)
1. Place PDFs in local `scans/` folder
2. Run: `python3 scripts/create_combined_pages.py`
3. Upload generated HTML files from `articles/` folder
4. Update relevant publication page manually

## Admin Panel Updates

The admin panel (http://michaelgiltz.com/admin) now:
- Shows count of unprocessed PDFs
- Creates combined HTML pages automatically
- Updates publication pages with new links
- Provides processing status and logs

### To Process New PDFs:
1. Upload PDFs to `scans/` folder
2. Visit http://michaelgiltz.com/admin
3. Click "Process New PDFs"
4. System will:
   - Create HTML pages in `articles/`
   - Extract text for SEO
   - Update publication pages
   - Mark PDFs as processed

## FTP Details
- Host: `ftp.michaelgiltz.com`
- Username: `webmanager@michaelgiltz.com`
- Password: (stored in upload scripts)
- Main directory: `/public_html`

## Upload Scripts

### Full Site Upload
```bash
python3 upload_site.py
```
Uploads entire site including all 4,213 article pages

### Individual File Upload
For adding single new articles:
1. Upload PDF to `scans/`
2. Use admin panel to process
3. Article automatically appears on site

## File Naming Convention
**CRITICAL**: All PDFs must follow this format:
```
Publication-Article_Title_With_Underscores-MM-DD-YYYY.pdf
```

Examples:
- `HuffPo-Theater_Review_Hamilton-03-15-2016.pdf`
- `NYTimes-Movie_Review_Oppenheimer-07-21-2023.pdf`
- `Advocate-Pride_Parade_Coverage-06-25-2023.pdf`

## Search Functionality
The search feature now:
- Searches through actual article text (not just titles)
- Links to combined HTML pages
- Provides text excerpts with highlighted search terms
- Much more accurate and useful

## Benefits of New System
1. **Better SEO**: Search engines can index full article text
2. **Faster Loading**: Optimized PDFs with web viewing
3. **No Downloads**: Users can read articles directly in browser
4. **Mobile Friendly**: Responsive design works on all devices
5. **Consistent Look**: All articles have same professional appearance

## Troubleshooting

### PDF Not Processing
- Check filename format (must match exactly)
- Ensure PDF is in `scans/` folder
- Check admin panel logs for errors

### Article Not Appearing
- Verify PDF was processed (check admin panel)
- Check publication mapping in process_new_pdfs.py
- Ensure publication page was updated

### Text Extraction Issues
- Some older PDFs may not extract text properly
- Page will still display with PDF viewer
- Manual text entry possible if needed

## Future Enhancements
- Automatic category detection
- Bulk edit capabilities
- Enhanced search with filters
- Article tagging system

## Support
For issues or questions:
- Check processing logs in admin panel
- Review error messages carefully
- Ensure proper file naming
- Verify FTP upload completed
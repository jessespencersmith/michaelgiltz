# Upload Instructions for michaelgiltz.com - UPDATED January 2025

## IMPORTANT CHANGES
The website has been updated to use combined HTML pages instead of direct PDF links. Each article now has:
- An HTML page with embedded PDF viewer at the top
- Extracted text content below for better searchability
- All links throughout the site now point to these HTML pages

## What to Upload

### 1. NEW: Articles Folder (REQUIRED)
- **Folder**: `articles/`
- **Contains**: 4,213 HTML files (one for each PDF)
- **Purpose**: These are the new combined PDF+Text pages
- **Upload to**: `/articles/` on the server

### 2. NEW: Articles Index Page
- **File**: `articles_index.htm`
- **Purpose**: Index of all articles for browsing
- **Upload to**: Root directory on the server

### 3. Updated HTML Pages (REQUIRED)
All main HTML pages have been updated to link to the new article pages:
- index.htm
- AMERICAblog.htm
- About.htm
- Advocate.htm
- Alligator.htm
- BBC_Portfolio.htm
- BookFilter.htm
- Bookandfilmglobe.htm
- Books.htm
- BroadwayDirect.htm
- CDReview.htm
- Contact.htm
- DVDs.htm
- EntertainmentWeekly.htm
- Fired.htm
- Flowers_Portfolio.htm
- Fox_Portfolio.htm
- General.htm
- HuffingtonPost.htm
- IRAAwards.htm
- LATimes.htm
- Lists.htm
- Misc.htm
- Movies.htm
- Music.htm
- MyFavoriteThings.htm
- MyFirstTime.htm
- NYDailyNews.htm
- NYPost.htm
- NewYork.htm
- Parade.htm
- People.htm
- Politics.htm
- Popsurfing.htm
- Premiere.htm
- Sports.htm
- TV.htm
- TheIRAs.htm
- TheLists.htm
- Theater.htm

### 4. Updated Search File
- **File**: `search.php`
- **Changes**: Now searches through the new article HTML files

### 5. Existing Files (No Changes)
These remain the same:
- `scans/` folder (keep all PDFs - they're embedded in the HTML pages)
- `giltz.css`
- `giltz.jpg`
- All other images and assets

## Upload Steps

1. **Create articles folder on server**
   - Create a new folder called `articles` in the root directory

2. **Upload the articles folder contents**
   - Upload all 4,213 HTML files from your local `articles/` folder
   - This may take a while due to the number of files

3. **Upload updated HTML files**
   - Upload all the HTML files listed in section 3 above
   - These replace the existing files on the server

4. **Upload search.php**
   - Replace the existing search.php file

5. **Upload articles_index.htm**
   - Upload to the root directory

## Testing After Upload

1. **Test article links**: Click on any article link from the main pages - it should open the new HTML page with embedded PDF
2. **Test search**: Try searching for articles - results should link to the new HTML pages
3. **Test navigation**: Each article page should have a working HOME button
4. **Test PDF viewing**: The embedded PDFs should display properly at the top of each article page

## Benefits of This Update
- **Better SEO**: Search engines can now index the text content of all articles
- **Faster loading**: Compressed PDFs load quickly with web optimization
- **Better user experience**: Users can read articles without downloading PDFs
- **Improved search**: The site search now searches actual article content

## Notes
- The original PDFs are still stored in the `scans/` folder and are embedded in the HTML pages
- All article filenames remain the same, just with .html extension instead of .pdf
- The site structure and navigation remain unchanged - only the article links are updated

## Future Updates
When adding new articles:
1. Save the PDF in the `scans/` folder as usual
2. Run the `create_combined_pages.py` script to generate the HTML page
3. Update the relevant category page to link to the new HTML file
4. Upload both the PDF and the new HTML file
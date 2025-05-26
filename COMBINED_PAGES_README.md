# Combined PDF + Text Pages

This feature implements Issue #1: Combining PDF displays with extracted text for better searchability and user experience.

## What It Does

Creates web pages that display:
1. **Embedded PDF** at the top (viewable in browser)
2. **HOME button** for navigation
3. **Extracted text** below for search engines and accessibility
4. **Article metadata** (publication, date, author)

## How to Generate Combined Pages

### First Time Setup

1. **Generate all combined pages**:
   ```bash
   cd "/Users/spencejb/Documents/GiltzWeb 2/scripts"
   python3 create_combined_pages.py
   ```
   This creates an `articles` folder with 4000+ combined HTML pages.

2. **Update existing links** (optional):
   ```bash
   python3 update_article_links.py
   ```
   This updates existing pages to link to the new combined pages instead of direct PDFs.

### For New Articles

When you add a new PDF to the `scans` folder:
1. Run the admin panel update as usual
2. Run `create_combined_pages.py` to generate the combined page
3. The new article will automatically have both PDF and searchable text

## Page Features

Each combined page includes:
- **Header**: Article title, publication, date, author
- **PDF Viewer**: Embedded PDF (works in most modern browsers)
- **HOME Button**: Quick navigation back to main site
- **SEO Text**: Extracted text for search engines
- **Footer**: Copyright and source information

## Benefits

1. **Better SEO**: Search engines can index the full text
2. **Accessibility**: Screen readers can access content
3. **Faster Loading**: Users see content structure immediately
4. **Fallback**: If PDF viewer fails, text is still available
5. **Mobile Friendly**: Responsive design adapts to all screens

## Technical Notes

- PDFs are embedded using `<iframe>` tags
- Text extraction uses PyPDF2
- Pages follow the site's existing CSS styling
- All pages are static HTML for fast loading
- Original PDFs remain in the `scans` folder
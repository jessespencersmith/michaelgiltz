# MichaelGiltz.com - Journalism Portfolio Website

A comprehensive journalism portfolio website featuring 20+ years of entertainment journalism, reviews, and interviews. The site includes over 4,200 articles from publications like The New York Times, Los Angeles Times, Huffington Post, Entertainment Weekly, and many more.

## 🌟 Features

- **Extensive Article Archive**: 4,200+ PDFs organized by publication
- **Full-Text Search**: Search across all articles with extracted text content
- **Admin Panel**: One-click updates for new content
- **SEO Optimized**: Automatically generated HTML versions of all PDFs
- **Responsive Design**: Works on all devices
- **Social Integration**: BlueSky, Facebook, and Substack newsletter

## 🚀 Quick Start

### Updating with New Articles

Follow these steps to add new articles to your website:

1. **Save articles as PDFs**
   - For each article, save/download as PDF from the publication's website
   - Use this filename format: `Publication-Title-MM-DD-YYYY.pdf`
   - Example: `HuffPo-Theater_Review_Hamilton-03-15-2025.pdf`
   - Place all PDFs in the **"PDFs to Compress"** folder on your Desktop

2. **Compress all PDFs**
   - Double-click **"Compress PDFs on Desktop.command"**
   - Wait for "Processing complete!" message
   - All PDFs will be compressed at once

3. **Move compressed PDFs to scans**
   - Open the **"Compressed PDFs"** folder on your Desktop
   - Select ALL files in this folder
   - Move them to: `/Users/spencejb/Documents/GiltzWeb 2/scans/`
   - The "Compressed PDFs" folder should now be empty

4. **Upload to website**
   - Open your FTP client
   - Connect to `ftp.michaelgiltz.com`
   - Navigate to the `scans/` folder
   - Upload all the new PDFs you just moved

5. **Update the website**
   - Go to `http://michaelgiltz.com/admin`
   - Click the **"Process New PDFs"** button
   - The system will process all new articles at once
   - Wait for "Website updated successfully!" message

**Done!** All your new articles are now live with embedded PDFs and searchable text.

### Archive Web Articles as PDFs

To save online articles as compressed PDFs:

1. **Open Terminal**
2. **Navigate to project folder**: `cd "/Users/spencejb/Documents/GiltzWeb 2"`
3. **Run archiver**: `python3 archive_article_simple.py`
4. **Enter the article URL**
5. **Enter filename** in format: `Publication-Article_Title-MM-DD-YYYY`
6. **Find compressed PDF on your Desktop**

Example: `Variety-Oscar_Nominations_2024-01-23-2024.pdf`

### Compress Existing PDFs (Standalone Use)

If you need to compress PDFs separately:

1. Put PDFs in the **"PDFs to Compress"** folder on Desktop
2. Double-click **"Compress PDFs on Desktop.command"**
3. Find compressed PDFs in **"Compressed PDFs"** folder

Features:
- 72 DPI compression (~90% size reduction)
- Optimized for fast web viewing with linearization
- Originals automatically moved to "Original PDFs" folder
- Processes all PDFs in the folder at once

### For Developers

```bash
# Clone the repository
git clone https://github.com/jessespencersmith/michaelgiltz.git
cd michaelgiltz

# Install Python dependencies (if any)
pip install -r requirements.txt

# Run local test
python3 scripts/test_local.py
```

## 📁 Project Structure

```
.
├── articles/                 # Combined HTML pages (4,200+ files) - NEW!
├── scans/                    # PDF articles (4,200+ files)
├── admin/                    # Admin panel
│   └── index.php            # Admin interface (updated)
├── scripts/                  # Processing scripts
│   ├── create_combined_pages.py  # Creates HTML+PDF pages
│   ├── process_new_pdfs.py      # Processes new uploads
│   └── deploy.py                # Deployment script
├── *.htm                    # Main HTML pages (all updated)
├── search.php               # Search functionality (updated)
├── giltz.css               # Stylesheet
├── compress_pdf_web.py      # PDF compression tool
└── archive_article_simple.py # Web article archiver
```

## 🛠️ Technical Details

### PDF Processing System

The site now uses a combined HTML+PDF system:

1. **Filename Format**: `Publication-Title_of_Article-MM-DD-YYYY.pdf`
2. **Combined Pages**: Each PDF gets an HTML page with:
   - Embedded PDF viewer at the top
   - Extracted text content below for SEO
   - Site navigation and branding
3. **Automatic Updates**: Publication pages are updated with new article links
4. **Search Integration**: Full text search across all articles

### Admin Panel

Located at `/admin`, the admin panel provides:
- One-click processing of new PDFs
- Shows unprocessed PDF count
- Recent PDF listing with status
- Processing statistics
- Test mode for verification
- Automatic publication page updates

### Search Functionality

- Full-text search across all articles
- Searches extracted text content in HTML pages
- Returns excerpts with highlighted search terms
- Links directly to combined HTML pages
- Much faster and more accurate than before

## 🔧 Configuration

### FTP Settings (scripts/deploy.py)
```python
host = "ftp.michaelgiltz.com"
username = "webmanager@michaelgiltz.com"
remote_dir = "/"
```

### Admin Password
The admin panel is protected with HTTP Basic Authentication. To set up:
1. Use an online htpasswd generator
2. Create `.htpasswd` file in `/admin`
3. Update `.htaccess` with correct path

## 📝 Content Guidelines

### PDF Naming Convention
- Format: `Publication-Title_of_Article-MM-DD-YYYY.pdf`
- Publication: No spaces (use HuffPo, not Huffington Post)
- Title: Use underscores for spaces
- Date: MM-DD-YYYY format

### Supported Publications
- HuffPo (Huffington Post)
- BookFilter
- Popsurfing
- NYPost (New York Post)
- LATimes (Los Angeles Times)
- And 30+ more...

## 🚀 Deployment

### Full Site Upload (NEW)
```bash
python3 upload_site.py
```
This uploads:
- All HTML pages with updated links
- 4,213 combined article pages
- Updated search functionality
- Admin panel updates

### Process New PDFs Locally
```bash
python3 scripts/create_combined_pages.py
```

### Quick HTML Updates
```bash
python3 deploy_html.py
```

## 🔒 Security

- Admin panel password protected
- Sensitive files excluded from repository
- FTP credentials stored locally only
- `.htaccess` protects sensitive directories

## 🐛 Troubleshooting

### PDFs Not Processing
- Check filename format matches convention
- Ensure no special characters in filename
- Verify PDF is valid and not corrupted

### Admin Panel Access Issues
- Verify `.htpasswd` exists in admin directory
- Check `.htaccess` path is correct
- Ensure password was generated with Apache MD5

### Search Not Working
- Verify `extracted_content/` directory exists
- Check PHP is enabled on server
- Run full update to regenerate HTML files

## 📈 Recent Updates (January 2025)

- [x] Combined HTML+PDF pages for all articles
- [x] Improved search with full text indexing
- [x] PDF compression workflow
- [x] Web article archiving tool
- [x] Automatic publication page updates
- [x] Enhanced admin panel

## 🎯 Future Enhancements

- [ ] Automatic social media posting
- [ ] Analytics integration
- [ ] Comment system
- [ ] Related articles feature
- [ ] Mobile app
- [ ] RSS feed generation

## 👨‍💻 Development

### Local Testing
```bash
python3 scripts/test_local.py
```

### Adding New Features
1. Create feature branch
2. Test locally
3. Update documentation
4. Submit pull request

## 📄 License

© 2025 Michael J. Giltz. All rights reserved.

Articles and content are the sole property of Michael Giltz and the original publishers. Code and infrastructure may be used with attribution.

## 🤝 Contributing

While this is primarily a personal portfolio site, bug reports and feature suggestions are welcome:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

Michael Giltz
- Email: mgiltz@pipeline.com
- BlueSky: [@mgiltz.bsky.social](https://bsky.app/profile/mgiltz.bsky.social)
- Facebook: [michael.giltz](https://facebook.com/michael.giltz)
- Newsletter: [Subscribe on Substack](https://michaelgiltz390212.substack.com)

## 🙏 Acknowledgments

- Built with Python, PHP, and classic web technologies
- Hosted on BlueHost
- PDF processing powered by PyPDF2
- Over 20 years of journalism archived and searchable

---

**Note**: This repository contains the website infrastructure. The actual article PDFs are not included due to size and copyright considerations.
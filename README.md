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

### For Content Updates (Non-Technical Users)

1. Create your article PDF as usual
2. Upload to the `scans/` folder via FTP
3. Visit `http://michaelgiltz.com/admin`
4. Click "Update Website Now"
5. Done! Your article is now live and searchable

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
├── scans/                    # PDF articles (4,200+ files)
├── extracted_content/        # SEO-friendly HTML versions
├── admin/                    # Admin panel
│   └── index.php            # Admin interface
├── scripts/                  # Processing scripts
│   ├── process_pdfs.py      # Main processing script
│   ├── deploy.py            # Deployment script
│   └── migrate_existing.py  # One-time migration
├── *.htm                    # Main HTML pages
├── search.php               # Search functionality
└── giltz.css               # Stylesheet
```

## 🛠️ Technical Details

### PDF Processing System

The site uses an automated system to process PDFs:

1. **Filename Format**: `Publication-Title_of_Article-MM-DD-YYYY.pdf`
2. **Text Extraction**: PyPDF2 extracts text for search functionality
3. **HTML Generation**: Creates SEO-friendly pages for each article
4. **Link Updates**: Automatically updates publication pages with new articles

### Admin Panel

Located at `/admin`, the admin panel provides:
- One-click website updates
- Recent PDF listing
- Processing statistics
- Test mode for verification

### Search Functionality

- Full-text search across all articles
- Searches both PDF content and metadata
- Returns excerpts with highlighted search terms
- Links to both HTML and PDF versions

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

### Full Deployment
```bash
python3 scripts/deploy.py --full
```

### Update HTML Files Only
```bash
python3 deploy_html.py
```

### Process New PDFs
```bash
python3 scripts/process_pdfs.py
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

## 📈 Future Enhancements

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
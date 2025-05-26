# Troubleshooting Guide for michaelgiltz.com

## Common Issues and Solutions

### PDF Compression Not Working

#### Symptom: "Command not found: gs"
**Solution:**
```bash
brew install ghostscript
```

#### Symptom: "No PDFs found in 'PDFs to Compress' folder"
**Solution:**
- Make sure PDFs are directly in the folder, not in subfolders
- Check that files end with .pdf (not .PDF)
- Make sure "PDFs to Compress" folder is on Desktop

#### Symptom: Double-clicking command does nothing
**Solution:**
1. Right-click the command file
2. Choose "Open"
3. Click "Open" in security dialog
4. Try double-clicking again

### Archive Tool Issues

#### Symptom: "playwright not found"
**Solution:**
```bash
pip3 install playwright
playwright install chromium
```

#### Symptom: "Permission denied"
**Solution:**
```bash
cd ~/Documents/GiltzWeb\ 2
chmod +x archive_article_simple.py
```

### FTP Upload Issues

#### Symptom: Can't connect to FTP
**Check:**
- Host: ftp.michaelgiltz.com
- Username: webmanager@michaelgiltz.com
- Password: (your password)
- Port: 21 (if asked)

#### Symptom: "Permission denied" when uploading
**Solution:**
- Make sure you're in the /scans/ folder on the server
- Check that filename has no special characters

### Git/GitHub Issues

#### Symptom: "Repository not found"
**Solution:**
```bash
cd ~/Documents
rm -rf "GiltzWeb 2"
git clone https://github.com/jessespencersmith/michaelgiltz.git "GiltzWeb 2"
```

#### Symptom: "Please tell me who you are"
**Solution:**
```bash
git config --global user.name "Michael Giltz"
git config --global user.email "mgiltz@pipeline.com"
```

### Admin Panel Issues

#### Symptom: "Process New PDFs" does nothing
**Check:**
- PDFs are in correct format: Publication-Title-MM-DD-YYYY.pdf
- No spaces in publication name
- Use underscores in title, not spaces

#### Symptom: Can't access admin panel
**Solution:**
- URL must be exactly: http://michaelgiltz.com/admin
- Username and password are for admin panel, not FTP

### Python Issues

#### Symptom: "pip3: command not found"
**Solution:**
```bash
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
```

#### Symptom: "No module named pypdf2"
**Solution:**
```bash
python3 -m pip install pypdf2
```

### File Naming Issues

#### Symptom: PDFs not processing on website
**Check filename format:**
- ✓ HuffPo-Theater_Review-03-15-2024.pdf
- ✗ HuffPo Theater Review 03-15-2024.pdf (spaces)
- ✗ HuffPo-Theater Review-March 15 2024.pdf (wrong date)
- ✗ Huffington Post-Theater_Review-03-15-2024.pdf (use HuffPo)

### Performance Issues

#### Symptom: Compression very slow
**Normal times:**
- 1-10 PDFs: 1-2 minutes
- 10-50 PDFs: 5-10 minutes
- 50+ PDFs: Consider smaller batches

#### Symptom: Website slow after upload
**Solution:**
- Process PDFs in batches of 20-30
- Wait for "Success" message before adding more

## Emergency Fixes

### Reset Everything
If nothing works, start fresh:

```bash
# Backup your work
cp -r ~/Documents/GiltzWeb\ 2/scans ~/Desktop/scans_backup

# Remove and reinstall
rm -rf ~/Documents/GiltzWeb\ 2
cd ~/Documents
git clone https://github.com/jessespencersmith/michaelgiltz.git "GiltzWeb 2"

# Restore your work
cp ~/Desktop/scans_backup/* ~/Documents/GiltzWeb\ 2/scans/
```

### Check Everything Is Installed
Run this diagnostic:

```bash
echo "Checking installations..."
which brew && echo "✓ Homebrew OK" || echo "✗ Homebrew MISSING"
which gs && echo "✓ Ghostscript OK" || echo "✗ Ghostscript MISSING"
which qpdf && echo "✓ qpdf OK" || echo "✗ qpdf MISSING"
which git && echo "✓ Git OK" || echo "✗ Git MISSING"
python3 -c "import pypdf2" && echo "✓ PyPDF2 OK" || echo "✗ PyPDF2 MISSING"
python3 -c "import playwright" && echo "✓ Playwright OK" || echo "✗ Playwright MISSING"
```

## Getting Help

Before asking for help:
1. Take a screenshot of the error
2. Note which step you were on
3. Try the relevant fix above
4. Check the filename format

Still stuck? 
- Email the screenshot and description
- Include the PDF filename if relevant
- Mention which guide you're following
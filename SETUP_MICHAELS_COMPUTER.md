# Complete Setup Guide for Michael's Computer

This guide will walk you through setting up everything you need to manage michaelgiltz.com on your Mac.

## Prerequisites
- Mac computer (you have this ✓)
- Python 3 (you have this ✓)
- Internet connection
- About 30 minutes

## Step 1: Install Homebrew (Package Manager)

Homebrew helps install software on your Mac. Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the prompts. When done, you may need to run these commands (it will tell you):

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## Step 2: Install Required Software

In Terminal, run these commands one at a time:

### Install Ghostscript (for PDF compression)
```bash
brew install ghostscript
```

### Install qpdf (for PDF optimization)
```bash
brew install qpdf
```

### Install Git (for version control)
```bash
brew install git
```

### Install Python packages
```bash
pip3 install pypdf2 playwright
```

### Install Playwright browsers (for web archiving)
```bash
playwright install chromium
```

## Step 3: Get the GiltzWeb 2 Project

### Option A: If you don't have it yet
```bash
cd ~/Documents
git clone https://github.com/jessespencersmith/michaelgiltz.git "GiltzWeb 2"
cd "GiltzWeb 2"
```

### Option B: If you already have it
```bash
cd ~/Documents/GiltzWeb\ 2
git pull origin main
```

## Step 4: Create Desktop Folders

Run this command to create the PDF compression folders:

```bash
mkdir -p ~/Desktop/"PDFs to Compress"
mkdir -p ~/Desktop/"Compressed PDFs"
mkdir -p ~/Desktop/"Original PDFs"
```

## Step 5: Set Up the Compression Tool

Make the compression command executable:

```bash
cd ~/Documents/GiltzWeb\ 2
chmod +x compress_pdf_web.py
```

Create the Desktop command file:

```bash
cat > ~/Desktop/"Compress PDFs on Desktop.command" << 'EOF'
#!/bin/bash
cd ~/Desktop

# Create folders if they don't exist
mkdir -p "PDFs to Compress"
mkdir -p "Compressed PDFs"
mkdir -p "Original PDFs"

echo "=========================================="
echo "PDF Compression Tool"
echo "=========================================="

# Check if qpdf is installed
if ! command -v qpdf &> /dev/null; then
    echo "Installing qpdf for better web optimization..."
    brew install qpdf
fi

# Run the compression script
cd ~/Documents/GiltzWeb\ 2
python3 compress_pdf_web.py

echo ""
echo "Processing complete!"
echo "Check the 'Compressed PDFs' folder on your Desktop"
echo ""
echo "Press Enter to close..."
read
EOF

chmod +x ~/Desktop/"Compress PDFs on Desktop.command"
```

## Step 6: Set Up FTP Credentials

Create your FTP configuration file:

```bash
cd ~/Documents/GiltzWeb\ 2
cat > ftp_config.txt << 'EOF'
Host: ftp.michaelgiltz.com
Username: webmanager@michaelgiltz.com
Password: [YOUR_PASSWORD_HERE]
EOF
```

**IMPORTANT**: Replace `[YOUR_PASSWORD_HERE]` with your actual FTP password.

## Step 7: Test Everything

### Test PDF Compression
1. Put a PDF in the "PDFs to Compress" folder on your Desktop
2. Double-click "Compress PDFs on Desktop.command"
3. Check the "Compressed PDFs" folder for the result

### Test Web Article Archiving
```bash
cd ~/Documents/GiltzWeb\ 2
python3 archive_article_simple.py
```

### Test Git Access
```bash
cd ~/Documents/GiltzWeb\ 2
git status
```

## Step 8: Install an FTP Client (if needed)

If you don't have an FTP client, download one of these free options:
- **FileZilla**: https://filezilla-project.org/download.php?platform=osx
- **Cyberduck**: https://cyberduck.io/download/

## Daily Workflow Checklist

Now you're ready to use the workflow:

1. **Save articles as PDFs** → "PDFs to Compress" folder
2. **Compress PDFs** → Double-click "Compress PDFs on Desktop.command"
3. **Move compressed PDFs** → From "Compressed PDFs" to GiltzWeb 2/scans/
4. **Upload via FTP** → Connect and upload to scans/ folder
5. **Update website** → Visit michaelgiltz.com/admin and click "Process New PDFs"

## Troubleshooting

### "Command not found" errors
Make sure you've installed Homebrew and run:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile
```

### Python package errors
Try installing with:
```bash
python3 -m pip install --upgrade pip
python3 -m pip install pypdf2 playwright
```

### Compression tool not working
Check that Ghostscript is installed:
```bash
which gs
```
If nothing appears, reinstall:
```bash
brew reinstall ghostscript
```

### Git issues
Set up your Git identity:
```bash
git config --global user.name "Michael Giltz"
git config --global user.email "mgiltz@pipeline.com"
```

## Quick Reference Card

Save this for daily use:

```
COMPRESS PDFs:
1. PDFs → "PDFs to Compress" folder
2. Double-click "Compress PDFs on Desktop.command"
3. Get files from "Compressed PDFs" folder

ARCHIVE WEB ARTICLES:
1. Terminal: cd ~/Documents/GiltzWeb\ 2
2. Terminal: python3 archive_article_simple.py
3. Enter URL and filename

UPLOAD TO SITE:
1. FTP to ftp.michaelgiltz.com
2. Upload PDFs to scans/ folder
3. Visit michaelgiltz.com/admin
4. Click "Process New PDFs"

UPDATE FROM GITHUB:
Terminal: cd ~/Documents/GiltzWeb\ 2 && git pull
```

## Support

If you run into issues:
1. Take a screenshot of the error
2. Note what step you were on
3. Contact Jesse for help

---

Setup complete! You now have everything needed to manage michaelgiltz.com.
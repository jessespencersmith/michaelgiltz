# Quick Setup Steps for Michael's Mac

Follow these steps in order. Copy and paste each command into Terminal.

## Step 1: Open Terminal
- Press `Command + Space`
- Type "Terminal"
- Press Enter

## Step 2: Install Homebrew
Copy and paste this entire line:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- Press Enter
- Enter your Mac password when asked
- Wait for "Installation successful!"

## Step 3: Set Up Homebrew
If Terminal shows commands starting with "echo", copy and run them.
Otherwise, run these:
```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## Step 4: Install Required Tools
Run each line separately:
```
brew install ghostscript
```
```
brew install qpdf
```
```
brew install git
```

## Step 5: Install Python Tools
```
pip3 install pypdf2 playwright
```
```
playwright install chromium
```

## Step 6: Get the Website Code
```
cd ~/Documents
```
```
git clone https://github.com/jessespencersmith/michaelgiltz.git "GiltzWeb 2"
```

## Step 7: Create Desktop Folders
```
mkdir -p ~/Desktop/"PDFs to Compress" ~/Desktop/"Compressed PDFs" ~/Desktop/"Original PDFs"
```

## Step 8: Create the PDF Compression Tool
Run this big command (copy the whole thing):
```
cat > ~/Desktop/"Compress PDFs on Desktop.command" << 'EOF'
#!/bin/bash
cd ~/Desktop
mkdir -p "PDFs to Compress" "Compressed PDFs" "Original PDFs"
echo "=========================================="
echo "PDF Compression Tool"
echo "=========================================="
if ! command -v qpdf &> /dev/null; then
    echo "Installing qpdf..."
    brew install qpdf
fi
cd ~/Documents/GiltzWeb\ 2
python3 compress_pdf_web.py
echo ""
echo "Processing complete!"
echo "Check the 'Compressed PDFs' folder"
echo "Press Enter to close..."
read
EOF
```

Then make it executable:
```
chmod +x ~/Desktop/"Compress PDFs on Desktop.command"
```

## Step 9: Test It!
1. Look at your Desktop - you should see:
   - "PDFs to Compress" folder
   - "Compressed PDFs" folder
   - "Original PDFs" folder
   - "Compress PDFs on Desktop.command" file

2. Put a PDF in "PDFs to Compress"
3. Double-click "Compress PDFs on Desktop.command"
4. Check "Compressed PDFs" folder for result

## You're Done! 

### Daily Use:
1. Save PDFs to "PDFs to Compress"
2. Double-click "Compress PDFs on Desktop.command"
3. Move files from "Compressed PDFs" to GiltzWeb 2/scans
4. Upload to website
5. Update via admin panel

### To Update Code Later:
```
cd ~/Documents/GiltzWeb\ 2 && git pull
```
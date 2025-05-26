#!/bin/bash

# Push repository to GitHub using Personal Access Token
# Run this after creating a new repository on GitHub

echo "========================================="
echo "GitHub Push Script for michaelgiltz"
echo "========================================="
echo ""
echo "⚠️  IMPORTANT: GitHub requires a Personal Access Token (PAT)"
echo "   Not your regular GitHub password!"
echo ""
echo "📋 To create a token:"
echo "   1. Go to https://github.com/settings/tokens"
echo "   2. Click 'Generate new token' → 'Generate new token (classic)'"
echo "   3. Check 'repo' scope"
echo "   4. Generate and copy the token"
echo ""
echo "========================================="
echo ""

# Check if remote already exists
if git remote | grep -q origin; then
    echo "Remote 'origin' already exists. Removing it first..."
    git remote remove origin
fi

# Add remote origin
echo "Adding GitHub remote..."
git remote add origin https://github.com/jessespencersmith/michaelgiltz.git

# Set up credential helper for macOS
echo "Setting up credential helper..."
git config --global credential.helper osxkeychain

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
echo "When prompted:"
echo "  Username: jessespencersmith"
echo "  Password: [Paste your Personal Access Token]"
echo ""
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Your repository is now on GitHub!"
    echo "🔗 View it at: https://github.com/jessespencersmith/michaelgiltz"
else
    echo ""
    echo "❌ Push failed. Please check your token and try again."
    echo "📖 See github_setup_instructions.md for help"
fi
#!/bin/bash

# Push repository to GitHub
# Run this after creating a new repository on GitHub

echo "Setting up GitHub remote for michaelgiltz project..."

# Check if remote already exists
if git remote | grep -q origin; then
    echo "Remote 'origin' already exists. Removing it first..."
    git remote remove origin
fi

# Add remote origin
echo "Adding GitHub remote..."
git remote add origin https://github.com/jessespencersmith/michaelgiltz.git

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo "✅ Done! Your repository is now on GitHub at https://github.com/jessespencersmith/michaelgiltz"
echo ""
echo "You can view it at: https://github.com/jessespencersmith/michaelgiltz"
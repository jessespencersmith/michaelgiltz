# GitHub Authentication Setup

GitHub requires Personal Access Tokens (PAT) instead of passwords. Here's how to set it up:

## Step 1: Create a Personal Access Token (Recommended: Fine-grained)

### Option A: Fine-grained Personal Access Token (More Secure - Recommended)
1. Go to https://github.com/settings/tokens?type=beta
2. Click "Generate new token"
3. Token name: "GiltzWeb Push Access"
4. Expiration: 90 days (or custom)
5. Repository access: Select "Selected repositories"
   - Add: `jessespencersmith/michaelgiltz`
6. Repository permissions:
   - Contents: Read and Write
   - Metadata: Read (automatically selected)
   - Pull requests: Read and Write (if you plan to use PRs)
   - Actions: Read (if you plan to use GitHub Actions)
7. Click "Generate token"
8. **COPY THE TOKEN NOW** - you won't see it again!

### Option B: Classic Token (Simpler but less secure)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Note: "GiltzWeb Push Access"
4. Expiration: 90 days
5. Select scope: ✅ repo
6. Click "Generate token"
7. **COPY THE TOKEN NOW** - you won't see it again!

## Step 2: Use the Token

When prompted:
- Username: `jessespencersmith`
- Password: **Paste your Personal Access Token** (not your GitHub password)

## Step 3: Push to GitHub

Run the push script again:
```bash
cd "/Users/spencejb/Documents/GiltzWeb 2"
./push_to_github.sh
```

## Optional: Save Credentials

To avoid entering credentials every time:
```bash
git config --global credential.helper osxkeychain
```

This will save your credentials in macOS Keychain after the first successful push.

## Alternative: Use SSH

If you prefer SSH (more secure):
1. Set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
2. Change the remote URL:
   ```bash
   git remote set-url origin git@github.com:jessespencersmith/michaelgiltz.git
   ```
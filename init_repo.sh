#!/bin/bash

echo "=========================================="
echo "Git Repository Initialization"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed!"
    echo "Please install Git first"
    exit 1
fi

echo "✅ Git found: $(git --version)"
echo ""

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already initialized"
fi

echo ""

# Set up git config (optional)
echo "Current Git configuration:"
git config user.name
git config user.email
echo ""

read -p "Configure Git user settings? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    
    git config user.name "$git_name"
    git config user.email "$git_email"
    
    echo "✅ Git user configured"
fi

echo ""

# Create initial commit
read -p "Create initial commit? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add .
    git commit -m "Initial commit: Deshrupantor news scraper"
    echo "✅ Initial commit created"
fi

echo ""
echo "=========================================="
echo "Next Steps"
echo "=========================================="
echo ""
echo "1. Create a new repository on GitHub"
echo "2. Add the remote:"
echo "   git remote add origin https://github.com/yourusername/deshrupantor-scraper.git"
echo ""
echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Enable GitHub Actions in repository settings"
echo ""
echo "The scraper will then run automatically every 5 minutes!"
echo ""

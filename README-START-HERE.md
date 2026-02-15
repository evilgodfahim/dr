# Deshrupantor News Scraper - Complete GitHub Repository

## 📦 What You Have

A **complete, ready-to-deploy GitHub repository** for scraping Deshrupantor.com news articles with **FlareSolverr**, **automatic button clicking**, and a **beautiful web interface**.

## 📂 Files Provided

1. **deshrupantor-scraper/** (folder) - Complete repository with all files
2. **deshrupantor-scraper.tar.gz** (archive) - Compressed version

Both contain the exact same content - use whichever is more convenient!

## ⚡ Quick Deploy to GitHub

### Method 1: Web Upload (Easiest)

1. Go to GitHub.com and create a new repository named `deshrupantor-scraper`
2. Click "uploading an existing file"
3. Drag and drop ALL files from the `deshrupantor-scraper` folder
4. Click "Commit changes"
5. Go to Settings → Actions → Enable workflows
6. Go to Settings → Pages → Enable (select main branch)
7. Done! It will scrape daily at 6 AM Bangladesh Time

### Method 2: Command Line

```bash
# Extract the archive (if using .tar.gz)
tar -xzf deshrupantor-scraper.tar.gz
cd deshrupantor-scraper

# Initialize Git
git init
git add .
git commit -m "Initial commit"

# Connect to GitHub (create repo first on GitHub.com)
git remote add origin https://github.com/YOUR_USERNAME/deshrupantor-scraper.git
git branch -M main
git push -u origin main

# Enable GitHub Actions in repository settings
```

## ✨ Features

✅ **Daily scraping** at 6:00 AM Bangladesh Time  
✅ **FlareSolverr integration** - Bypasses Cloudflare protection  
✅ **Automatic button clicking** - Clicks "আরও দেখুন" (Load More) button  
✅ **Web interface** (index.html) - Beautiful UI to browse articles  
✅ Stores articles in XML format  
✅ Maximum 500 articles (auto-maintains)  
✅ Automatic deduplication  
✅ Complete documentation  
✅ Docker support for local development  
✅ Error handling & logging  

## 🎯 New in This Version

🆕 **FlareSolverr**: Automatically bypasses Cloudflare challenges  
🆕 **Button Clicking**: Loads more content by clicking "আরও দেখুন"  
🆕 **Daily Schedule**: Runs at 6 AM BD time (not every 5 minutes)  
🆕 **Web Viewer**: Beautiful interface with search and filters  
🆕 **Docker Compose**: Easy FlareSolverr setup for local testing  

## 📋 Repository Contents (24 files)

```
deshrupantor-scraper/
├── 🎯 Core Application
│   ├── scraper.py              # Main scraper with FlareSolverr
│   ├── config.py               # Configuration
│   ├── articles.xml            # XML storage
│   └── index.html              # Beautiful web interface
│
├── 🐳 Docker
│   └── docker-compose.yml      # FlareSolverr setup
│
├── 🤖 GitHub Actions
│   ├── .github/workflows/scraper.yml
│   └── .github/ISSUE_TEMPLATE/
│
├── 📚 Documentation
│   ├── README.md               # Main docs
│   ├── OVERVIEW.md             # This overview
│   ├── QUICKSTART.md           # Quick setup
│   ├── SETUP_GUIDE.md          # Complete setup
│   ├── USAGE.md                # Usage examples
│   ├── CONTRIBUTING.md         # How to contribute
│   ├── PROJECT_STRUCTURE.md    # File structure
│   └── CHANGELOG.md            # Version history
│
├── 🔧 Setup & Testing
│   ├── requirements.txt        # Dependencies
│   ├── setup.sh               # Setup script
│   ├── init_repo.sh           # Git init script
│   └── test_scraper.py        # Tests
│
└── 📄 Other
    ├── LICENSE                 # MIT License
    └── .gitignore             # Git ignore
```

## 🎯 How It Works

```
Daily at 6:00 AM Bangladesh Time
    ↓
GitHub Actions starts FlareSolverr (Docker)
    ↓
Run scraper.py
    ↓
FlareSolverr bypasses Cloudflare
    ↓
Click "আরও দেখুন" button → Wait 5 seconds
    ↓
Extract articles using CSS selector
    ↓
Save to articles.xml (max 500)
    ↓
Commit & push to GitHub
    ↓
View at GitHub Pages or download index.html
    ↓
Repeat tomorrow at 6 AM
```

## 🎨 Customization

All settings in `config.py`:
- Update frequency: Edit `.github/workflows/scraper.yml`
- Max articles: `MAX_ARTICLES = 500`
- CSS selector: `CSS_SELECTOR = ".each .title .link_overlay"`
- Timeout, user agent, and more

## 📊 Output Format (XML)

```xml
<articles last_updated="..." total_count="...">
  <article>
    <id>unique-hash</id>
    <title>Article Title in Bengali</title>
    <url>https://www.deshrupantor.com/...</url>
    <scraped_at>2026-02-15T10:30:00</scraped_at>
  </article>
</articles>
```

## 🧪 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper
python scraper.py

# Run tests
python test_scraper.py

# View results
cat articles.xml
```

## 📈 GitHub Actions Info

- **Schedule**: Daily at 6:00 AM Bangladesh Time (`0 0 * * *` UTC)
- **Runtime**: ~2-3 minutes per run
- **Services**: FlareSolverr (Docker container)
- **Triggers**: Schedule, manual, push to main
- **Permissions**: Needs write access (auto-configured)

✅ **Free Tier Friendly**: Uses ~60-90 minutes/month (well within 2,000 minutes limit)

## 🎓 Documentation Files

1. **OVERVIEW.md** - You are here! Overall summary
2. **README.md** - Main documentation with all details
3. **QUICKSTART.md** - Get started in 5 minutes
4. **USAGE.md** - Code examples and integrations
5. **PROJECT_STRUCTURE.md** - Detailed file explanations
6. **CONTRIBUTING.md** - How to contribute

## 🔧 Common Tasks

**View articles in web browser:**
- Enable GitHub Pages in Settings
- Visit: `https://yourusername.github.io/deshrupantor-scraper/`
- Or download `index.html` and `articles.xml` and open locally

**Change schedule:**
```yaml
# Edit .github/workflows/scraper.yml
schedule:
  - cron: '0 12 * * *'  # 6 PM BD Time (12:00 UTC)
```

**Disable FlareSolverr:**
```python
# Edit config.py
USE_FLARESOLVERR = False
```

**Disable button clicking:**
```python
# Edit config.py
CLICK_LOAD_MORE = False
```

**Change max articles:**
```python
# Edit config.py
MAX_ARTICLES = 1000
```

## ✅ Checklist for Deployment

- [ ] Create GitHub repository
- [ ] Upload all files OR clone with git
- [ ] Enable GitHub Actions in settings
- [ ] Wait 5 minutes for first run
- [ ] Check Actions tab for status
- [ ] Verify articles.xml is updated
- [ ] Customize config.py as needed

## 🆘 Troubleshooting

**No articles scraped:**
- Test locally: `python scraper.py`
- Check website is accessible
- Verify CSS selector still works

**GitHub Actions not running:**
- Enable Actions in repository settings
- Check workflow file syntax
- View logs in Actions tab

**Permission errors:**
- Make scripts executable: `chmod +x *.sh`

## 🎯 Next Steps

1. ✅ Deploy to GitHub
2. ✅ Enable Actions
3. ✅ Enable GitHub Pages
4. ✅ Wait for first run (6 AM BD or manual trigger)
5. ✅ View articles at your GitHub Pages URL
6. ✅ Customize as needed (config.py)
7. ✅ Test locally with Docker (optional)

## 📧 Support

- Read the documentation files (especially SETUP_GUIDE.md)
- Test locally first with FlareSolverr
- Check GitHub Actions logs for errors
- Open issues on GitHub for help

## 🎉 Ready to Go!

Everything you need is in this folder. Just upload to GitHub, enable Actions and Pages, and you're done!

**Files**: 24 total  
**Size**: ~20KB compressed  
**Status**: Production ready ✅  
**FlareSolverr**: Included ✅  
**Web Interface**: Included ✅  
**License**: MIT  

Happy scraping! 🚀

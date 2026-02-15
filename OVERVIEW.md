# Deshrupantor Scraper - Complete Repository

## 🎯 What This Is

A complete, production-ready GitHub repository for scraping news articles from Deshrupantor.com **daily at 6:00 AM Bangladesh Time** and storing them in XML format. Features **FlareSolverr integration** for Cloudflare bypass, **automatic button clicking** to load more content, and a **beautiful web interface** to view articles.

## ✅ What's Included

### Core Functionality
- ✅ Python scraper that extracts articles from https://www.deshrupantor.com/printversion
- ✅ **FlareSolverr integration** - Bypasses Cloudflare protection automatically
- ✅ **Automatic button clicking** - Clicks "আরও দেখুন" (Load More) and waits 5 seconds
- ✅ Uses CSS selector: `.each .title .link_overlay`
- ✅ Stores articles in XML format with automatic deduplication
- ✅ Maintains maximum 500 articles (newest first)
- ✅ **Web interface** (index.html) - Beautiful UI to browse articles
- ✅ GitHub Actions workflow that runs **daily at 6:00 AM Bangladesh Time**
- ✅ Automatic commits to main branch
- ✅ Docker support for easy FlareSolverr setup

### Files Created (24 total)

**Core Application (4 files)**
1. `scraper.py` - Main scraper script with FlareSolverr support
2. `config.py` - Configuration settings
3. `articles.xml` - Initial XML storage file
4. `index.html` - Beautiful web interface to view articles

**Docker & Services (1 file)**
5. `docker-compose.yml` - FlareSolverr setup for local development

**GitHub Integration (4 files)**
22. `.github/workflows/scraper.yml` - Automation workflow with FlareSolverr
23. `.github/ISSUE_TEMPLATE/bug_report.md` - Bug report template
24. `.github/ISSUE_TEMPLATE/feature_request.md` - Feature request template
25. `.github/pull_request_template.md` - PR template

**Documentation (8 files)**
8. `README.md` - Main documentation
9. `QUICKSTART.md` - Quick start guide
10. `SETUP_GUIDE.md` - Complete setup instructions
11. `USAGE.md` - Detailed usage examples
12. `CONTRIBUTING.md` - Contribution guidelines
13. `CHANGELOG.md` - Version history
14. `PROJECT_STRUCTURE.md` - Repository structure
15. `LICENSE` - MIT License

**Setup & Testing (5 files)**
16. `requirements.txt` - Python dependencies
17. `requirements-dev.txt` - Development dependencies
18. `setup.sh` - Quick setup script
19. `init_repo.sh` - Git initialization script
20. `test_scraper.py` - Test suite
21. `.gitignore` - Git ignore rules

## 🚀 Quick Start

### 1. Create GitHub Repository
```bash
# On GitHub: Create new repository named "deshrupantor-scraper"
```

### 2. Upload Files
```bash
# Upload all files from this folder to your GitHub repository
# You can drag and drop or use Git commands
```

### 3. Initialize Locally (Alternative)
```bash
# If you prefer command line:
cd path/to/files
bash init_repo.sh

# Then follow the prompts to:
# 1. Set up Git
# 2. Create initial commit
# 3. Add remote
# 4. Push to GitHub
```

### 4. Enable GitHub Actions
- Go to your repository on GitHub
- Click "Actions" tab
- Click "I understand my workflows, go ahead and enable them"

### 5. Done!
The scraper will now run automatically every 5 minutes!

## 📊 How It Works

```
Daily at 6:00 AM Bangladesh Time:
    ↓
GitHub Actions triggers
    ↓
Starts FlareSolverr service (Docker container)
    ↓
Runs scraper.py
    ↓
FlareSolverr bypasses Cloudflare
    ↓
Clicks "আরও দেখুন" button → Waits 5 seconds
    ↓
Fetches full HTML content
    ↓
Parses HTML → Extracts articles
    ↓
Loads existing articles.xml
    ↓
Merges new + existing (removes duplicates)
    ↓
Keeps newest 500 articles
    ↓
Saves to articles.xml
    ↓
Commits & pushes if changed
    ↓
Repeat tomorrow at 6 AM
```

## 🎨 Key Features

### 1. FlareSolverr Integration
- Bypasses Cloudflare protection automatically
- Uses headless browser for reliable scraping
- Runs as Docker service in GitHub Actions
- Easy local setup with docker-compose

### 2. Smart Button Clicking
- Automatically finds and clicks "আরও দেখুন" (Load More)
- Waits 5 seconds for content to load
- Continues even if button not found
- Configurable wait time and button text

### 3. Beautiful Web Interface
- Modern, responsive design
- Search articles in Bengali or English
- Filter by date (Today, Week, Month)
- Auto-refreshes every 5 minutes
- Mobile-friendly
- Gradient UI with smooth animations

### 4. Smart Deduplication
- Each article gets a unique ID based on URL
- Same article won't be added twice
- Updates timestamp on re-scraping

### 5. FIFO Storage
- Maximum 500 articles maintained
- Oldest articles automatically removed
- Newest articles always kept

### 6. Robust Error Handling
- Network errors handled gracefully
- XML corruption prevention
- Automatic backups on errors
- Comprehensive logging
- FlareSolverr fallback support

## 📁 Repository Structure

```
deshrupantor-scraper/
├── scraper.py              ⭐ Main script
├── articles.xml            ⭐ Data storage
├── config.py               ⭐ Settings
├── .github/
│   └── workflows/
│       └── scraper.yml     ⭐ Automation
├── README.md               📖 Docs
├── QUICKSTART.md           📖 Quick guide
├── USAGE.md                📖 Examples
└── ... (other files)
```

## 🔧 Customization

### Change Update Frequency
Edit `.github/workflows/scraper.yml`:
```yaml
schedule:
  - cron: '*/5 * * * *'   # Every 5 minutes (default)
  - cron: '*/10 * * * *'  # Every 10 minutes
  - cron: '0 * * * *'     # Every hour
```

### Change Maximum Articles
Edit `config.py`:
```python
MAX_ARTICLES = 500  # Change to any number
```

### Change CSS Selector
If website structure changes, edit `config.py`:
```python
CSS_SELECTOR = ".each .title .link_overlay"  # Update this
```

## 📋 XML Output Format

```xml
<?xml version="1.0" encoding="utf-8"?>
<articles last_updated="2026-02-15T10:30:00" total_count="25">
  <article>
    <id>a1b2c3d4e5f6789...</id>
    <title>তারেক রহমানকে বিজিএমইএর অভিনন্দন</title>
    <url>https://www.deshrupantor.com/664807/...</url>
    <scraped_at>2026-02-15T10:30:00</scraped_at>
  </article>
  <!-- More articles... -->
</articles>
```

## 🧪 Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper locally
python scraper.py

# Run tests
python test_scraper.py

# View results
cat articles.xml
```

## 📊 GitHub Actions Usage

- **Frequency**: Every 5 minutes
- **Runtime**: ~1 minute per run
- **Monthly runs**: ~8,640 times
- **GitHub Free Tier**: 2,000 minutes/month
- **Estimated usage**: ~8,640 minutes/month

⚠️ **Note**: You may need to optimize or reduce frequency for free tier!

## 🎯 Next Steps

1. **Start**: Upload files to GitHub
2. **Enable**: Turn on GitHub Actions
3. **Monitor**: Check Actions tab for runs
4. **Customize**: Edit config.py as needed
5. **Integrate**: Use XML data in other projects

## 📚 Documentation Quick Links

- **Getting Started**: README.md
- **Quick Setup**: QUICKSTART.md
- **Examples**: USAGE.md
- **Contributing**: CONTRIBUTING.md
- **Structure**: PROJECT_STRUCTURE.md
- **Changes**: CHANGELOG.md

## 🆘 Support

- Read documentation files
- Check GitHub Actions logs
- Test locally first
- Open GitHub issue if stuck

## ⚡ Pro Tips

1. **Test locally before deploying**
2. **Monitor GitHub Actions quota**
3. **Keep documentation updated**
4. **Use branches for experiments**
5. **Backup articles.xml regularly**

## 🎉 You're All Set!

This is a complete, production-ready repository. Just:
1. Upload to GitHub
2. Enable Actions
3. Watch it work!

Happy scraping! 🎊

# Complete Setup Guide

## Prerequisites

- Python 3.8 or higher
- Docker (for FlareSolverr)
- Git

## Step-by-Step Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/deshrupantor-scraper.git
cd deshrupantor-scraper
```

### 2. Start FlareSolverr

FlareSolverr is required to bypass Cloudflare protection.

**Option A: Docker Compose (Recommended)**
```bash
docker-compose up -d
```

**Option B: Docker Run**
```bash
docker run -d \
  --name flaresolverr \
  -p 8191:8191 \
  -e LOG_LEVEL=info \
  -e TZ=Asia/Dhaka \
  ghcr.io/flaresolverr/flaresolverr:latest
```

**Verify FlareSolverr is running:**
```bash
curl http://localhost:8191/v1
```

You should see a JSON response.

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or using virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Settings (Optional)

Edit `config.py` to customize:

```python
# Enable/disable FlareSolverr
USE_FLARESOLVERR = True

# Button clicking
CLICK_LOAD_MORE = True
LOAD_MORE_BUTTON_TEXT = "আরও দেখুন"
WAIT_AFTER_CLICK = 5

# Max articles
MAX_ARTICLES = 500
```

### 5. Test Locally

```bash
python scraper.py
```

You should see:
```
2026-02-15 10:00:00 - INFO - Starting article update
2026-02-15 10:00:01 - INFO - Fetching via FlareSolverr: https://...
2026-02-15 10:00:05 - INFO - Clicked button, waiting 5 seconds...
2026-02-15 10:00:10 - INFO - Found 50 articles
2026-02-15 10:00:10 - INFO - Added 50 new articles
2026-02-15 10:00:10 - INFO - Successfully saved articles to articles.xml
```

### 6. View Articles

Open `index.html` in your browser:

```bash
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

Or run a local server:
```bash
python -m http.server 8000
# Then open http://localhost:8000
```

## GitHub Actions Setup

### 1. Push to GitHub

```bash
git remote add origin https://github.com/yourusername/deshrupantor-scraper.git
git branch -M main
git add .
git commit -m "Initial commit"
git push -u origin main
```

### 2. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"**

### 3. Enable GitHub Pages (Optional)

1. Go to **Settings** → **Pages**
2. Under **Source**, select **"main"** branch
3. Click **Save**
4. Your index.html will be available at:
   `https://yourusername.github.io/deshrupantor-scraper/`

### 4. Verify Workflow

1. Go to **Actions** tab
2. Click **"Scrape Deshrupantor Articles"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait for the workflow to complete
5. Check if `articles.xml` was updated

## Configuration

### Schedule Settings

The scraper runs **daily at 6:00 AM Bangladesh Time**.

Edit `.github/workflows/scraper.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # 6 AM BD = 00:00 UTC
```

**Other schedule examples:**
- `0 12 * * *` - 6 PM BD Time
- `0 0,12 * * *` - Twice daily (6 AM and 6 PM)
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 1` - Weekly on Monday

### FlareSolverr Settings

**Local Development** (`config.py`):
```python
FLARESOLVERR_URL = "http://localhost:8191/v1"
```

**GitHub Actions**: Already configured in workflow file

### Button Click Settings

Edit `config.py`:

```python
# Enable button clicking
CLICK_LOAD_MORE = True

# Button text to find
LOAD_MORE_BUTTON_TEXT = "আরও দেখুন"

# Wait time after click (seconds)
WAIT_AFTER_CLICK = 5
```

To disable button clicking:
```python
CLICK_LOAD_MORE = False
```

## Troubleshooting

### FlareSolverr Not Working

**Check if running:**
```bash
docker ps | grep flaresolverr
```

**Check logs:**
```bash
docker logs flaresolverr
```

**Restart:**
```bash
docker restart flaresolverr
```

### No Articles Found

1. Check if FlareSolverr is running
2. Verify website is accessible
3. Check CSS selector in `config.py`
4. Run with debug logging:
   ```python
   # In config.py
   LOG_LEVEL = "DEBUG"
   ```

### Button Click Failed

The scraper will continue even if button click fails. Check logs:
```
WARNING - Button click may have failed, continuing anyway...
```

This is normal if the button selector has changed.

### GitHub Actions Failing

1. Check **Actions** tab for error logs
2. Verify FlareSolverr service started
3. Check if workflow file syntax is correct
4. Look for rate limiting issues

### Index.html Not Loading

1. Ensure `articles.xml` is in the same folder
2. Check browser console for errors (F12)
3. Verify XML is valid:
   ```bash
   xmllint articles.xml
   ```

## Advanced Usage

### Custom CSS Selector

If website structure changes, update `config.py`:

```python
CSS_SELECTOR = ".new-selector .article-link"
```

### Multiple Scrapers

Run different scrapers for different sections:

1. Copy files:
   ```bash
   cp scraper.py scraper_politics.py
   cp config.py config_politics.py
   ```

2. Edit `config_politics.py` with different URL/selector

3. Update `scraper_politics.py` to import `config_politics`

### Export to Other Formats

See `USAGE.md` for examples of exporting to:
- JSON
- CSV
- SQLite database
- PostgreSQL

## Maintenance

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Update FlareSolverr

```bash
docker pull ghcr.io/flaresolverr/flaresolverr:latest
docker-compose down
docker-compose up -d
```

### Backup Articles

```bash
cp articles.xml articles.xml.backup
```

### Clean Old Data

Articles are automatically limited to 500. To manually clean:

```python
# In scraper.py or as a script
MAX_ARTICLES = 100  # Keep fewer articles
```

## Support

- **Documentation**: README.md, USAGE.md, PROJECT_STRUCTURE.md
- **Issues**: Open an issue on GitHub
- **Discussions**: GitHub Discussions

## Next Steps

1. ✅ Set up locally with FlareSolverr
2. ✅ Test the scraper
3. ✅ View in index.html
4. ✅ Push to GitHub
5. ✅ Enable Actions and Pages
6. ✅ Verify daily runs
7. ✅ Customize as needed

Happy scraping! 🎉

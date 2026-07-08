# Quick Start Guide

Get up and running with the Deshrupantor scraper in 5 minutes!

## 🚀 Quick Setup

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/deshrupantor-scraper.git
cd deshrupantor-scraper

# Start FlareSolverr
docker-compose up -d

# Install Python dependencies
pip install -r requirements.txt

# Run the scraper
python scraper.py

# Open the web viewer
open index.html  # macOS
# or
xdg-open index.html  # Linux
# or
start index.html  # Windows
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/deshrupantor-scraper.git
cd deshrupantor-scraper

# Start FlareSolverr manually
docker run -d \
  --name byparr \
  -p 8191:8191 \
  ghcr.io/thephaseless/byparr:latest

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scraper.py
```

## 📊 View Results

### Web Interface (Recommended)

Open `index.html` in your browser for a beautiful interface:

```bash
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

Features:
- Search articles in Bengali or English
- Filter by date (Today, This Week, This Month)
- Responsive design for all devices
- Auto-refreshes every 5 minutes

### View Raw XML

```bash
# View the XML file
cat articles.xml

# Or use a text editor
nano articles.xml

# Or open in browser
open articles.xml  # macOS
xdg-open articles.xml  # Linux
start articles.xml  # Windows
```

## 🤖 GitHub Actions Setup

To run automatically on GitHub (daily at 6 AM Bangladesh Time):

1. **Create GitHub Repository**
   ```bash
   # Go to github.com and create a new repository
   ```

2. **Push Your Code**
   ```bash
   git remote add origin https://github.com/yourusername/deshrupantor-scraper.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable Actions**
   - Go to your repository on GitHub
   - Click on "Actions" tab
   - Click "I understand my workflows, go ahead and enable them"

4. **Enable GitHub Pages (Optional)**
   - Go to Settings → Pages
   - Set source to "main branch"
   - Your index.html will be available at: `https://yourusername.github.io/deshrupantor-scraper/`

5. **Done!** 
   - The scraper will run daily at 6:00 AM Bangladesh Time
   - Check the "Actions" tab to see runs
   - New articles will be committed to `articles.xml`
   - View them at your GitHub Pages URL or download index.html

## 🔧 Common Tasks

### Change Update Frequency

Edit `.github/workflows/scraper.yml`:

```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
  # - cron: '*/10 * * * *'  # Every 10 minutes
  # - cron: '0 * * * *'  # Every hour
```

### Change Maximum Articles

Edit `scraper.py`:

```python
MAX_ARTICLES = 500  # Change this number
```

### Manual Trigger on GitHub

1. Go to "Actions" tab
2. Click "Scrape Deshrupantor Articles"
3. Click "Run workflow"
4. Click green "Run workflow" button

## 🧪 Testing

Run the test suite:

```bash
python test_scraper.py
```

## 📝 Example Output

```xml
<?xml version="1.0" ?>
<articles last_updated="2026-02-15T10:30:00" total_count="25">
  <article>
    <id>a1b2c3d4e5f6...</id>
    <title>আপডেট নিউজ শিরোনাম</title>
    <url>https://www.deshrupantor.com/664807/...</url>
    <scraped_at>2026-02-15T10:30:00</scraped_at>
  </article>
  <!-- More articles... -->
</articles>
```

## ❓ Troubleshooting

### "No articles found"
- Check your internet connection
- Verify the website is accessible
- The website structure may have changed

### "Permission denied" on scripts
```bash
chmod +x setup.sh init_repo.sh
```

### GitHub Actions not running
- Check if Actions are enabled
- Verify the workflow file syntax
- Check repository permissions

## 📚 Next Steps

- Read the full [README.md](README.md)
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Customize the scraper for your needs

## 💡 Tips

- Run locally first to test
- Check GitHub Actions logs for errors
- The scraper respects the website's structure
- Keep the repository public for free GitHub Actions

## 🆘 Need Help?

Open an issue on GitHub with:
- What you tried
- What happened
- Error messages (if any)

# Deshrupantor News Scraper

A Python-based web scraper that monitors [Deshrupantor](https://www.deshrupantor.com/printversion) and automatically saves articles to an XML file. The scraper runs daily at 6:00 AM Bangladesh time and maintains a maximum of 500 articles. Features **FlareSolverr** integration for Cloudflare bypass and automatic "আরও দেখুন" button clicking.

## Features

- 🔄 Auto-updates daily at 6:00 AM Bangladesh Time
- 🛡️ **FlareSolverr integration** for Cloudflare bypass
- 🖱️ **Automatic button clicking** - clicks "আরও দেখুন" (Load More) before scraping
- 📰 Scrapes news articles from Deshrupantor print version
- 💾 Saves articles in XML format
- 📊 Maintains maximum 500 articles (FIFO)
- 🌐 **Beautiful web interface** (index.html) to view articles
- 🚀 GitHub Actions workflow for continuous operation
- 🛡️ Error handling and logging

## What's New

✨ **FlareSolverr Support**: Bypasses Cloudflare protection automatically  
✨ **Button Clicking**: Clicks "আরও দেখুন" button and waits 5 seconds before scraping  
✨ **Daily Schedule**: Runs at 6:00 AM Bangladesh Time instead of every 5 minutes  
✨ **Web Viewer**: Beautiful index.html to browse scraped articles  
✨ **Docker Support**: Easy local development with docker-compose

## Project Structure

```
deshrupantor-scraper/
├── .github/
│   └── workflows/
│       └── scraper.yml       # GitHub Actions workflow (daily 6 AM BD)
├── scraper.py                # Main scraper script
├── config.py                 # Configuration (FlareSolverr, button click, etc.)
├── articles.xml              # XML storage for articles
├── index.html                # Web interface to view articles
├── docker-compose.yml        # FlareSolverr setup for local dev
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/deshrupantor-scraper.git
cd deshrupantor-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start FlareSolverr (required):

**Option A: Using Docker (Recommended)**
```bash
docker-compose up -d
```

**Option B: Using Docker directly**
```bash
docker run -d \
  --name byparr \
  -p 8191:8191 \
  -e LOG_LEVEL=info \
  ghcr.io/thephaseless/byparr:latest
```

4. Run the scraper:
```bash
python scraper.py
```

5. View articles:
```bash
# Open index.html in your browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

### GitHub Actions Setup

The scraper runs automatically on GitHub Actions daily at 6:00 AM Bangladesh Time:

1. Fork/clone this repository
2. Enable GitHub Actions in your repository settings
3. The workflow will run automatically at 6 AM BD time
4. Articles are committed to `articles.xml` in the main branch
5. View articles by opening `index.html` via GitHub Pages or downloading it

## Configuration

### Schedule

The scraper runs **daily at 6:00 AM Bangladesh Time** (00:00 UTC).

To change the schedule, edit `.github/workflows/scraper.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # 6:00 AM BD Time (UTC+6)
```

Cron syntax examples:
- `0 0 * * *` - Daily at 6:00 AM BD (00:00 UTC)
- `0 12 * * *` - Daily at 6:00 PM BD (12:00 UTC)
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 1` - Weekly on Monday at 6:00 AM BD

### FlareSolverr Settings

Edit `config.py`:

```python
# Enable/disable FlareSolverr
USE_FLARESOLVERR = True
FLARESOLVERR_URL = "http://localhost:8191/v1"

# Button clicking
CLICK_LOAD_MORE = True
LOAD_MORE_BUTTON_TEXT = "আরও দেখুন"
WAIT_AFTER_CLICK = 5  # seconds
```

### Maximum Articles

To change the maximum number of articles stored, edit `config.py`:

```python
MAX_ARTICLES = 500  # Change this value
```

## XML Format

Articles are stored in the following XML structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<articles>
  <article>
    <id>unique-id</id>
    <title>Article Title</title>
    <url>https://www.deshrupantor.com/...</url>
    <scraped_at>2026-02-15T10:30:00</scraped_at>
  </article>
  <!-- More articles... -->
</articles>
```

## How It Works

1. **FlareSolverr**: Bypasses Cloudflare protection using a headless browser
2. **Button Clicking**: Automatically clicks "আরও দেখুন" (Load More) button
3. **Waiting**: Waits 5 seconds for content to load after clicking
4. **Scraping**: Extracts article titles and URLs using CSS selectors
5. **Storage**: Saves articles to `articles.xml` with timestamps
6. **Maintenance**: Keeps only the latest 500 articles
7. **Automation**: GitHub Actions runs the script daily at 6 AM BD time
8. **Viewing**: Use `index.html` to browse articles in a beautiful web interface

## Web Interface

The project includes a beautiful web interface (`index.html`) to view scraped articles:

### Features:
- 📊 Statistics: Total articles, last update time, displayed count
- 🔍 Search: Search articles by title (supports Bengali and English)
- 📅 Filters: All, Today, This Week, This Month
- 📱 Responsive: Works on desktop, tablet, and mobile
- 🎨 Modern UI: Gradient design with smooth animations
- 🔄 Auto-refresh: Updates every 5 minutes automatically

### Usage:

**Option 1: Open Locally**
```bash
# Download articles.xml and index.html
# Open index.html in your browser
```

**Option 2: GitHub Pages**
```bash
# Enable GitHub Pages in repository settings
# Set source to main branch
# Access at: https://yourusername.github.io/deshrupantor-scraper/
```

**Option 3: Local Server**
```bash
# Python 3
python -m http.server 8000
# Open http://localhost:8000

# Node.js
npx serve
```

## Dependencies

- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - XML processing

### Additional Requirements

- **FlareSolverr** (Docker container) - For Cloudflare bypass
  - Runs as a GitHub Actions service
  - Or locally via Docker: `docker-compose up -d`

## Troubleshooting

### Scraper not running on GitHub Actions

1. Check if Actions are enabled in repository settings
2. Verify the workflow file syntax
3. Check the Actions tab for error logs

### No articles being saved

1. Check if the website structure has changed
2. Verify CSS selectors in `scraper.py`
3. Check network connectivity

### XML file corruption

The scraper includes error handling to prevent XML corruption. If it occurs:
1. Delete `articles.xml`
2. Run the scraper again to create a fresh file

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

MIT License - feel free to use and modify as needed.

## Disclaimer

This scraper is for educational purposes. Please respect the website's robots.txt and terms of service. Consider implementing rate limiting and proper user agents for production use.

## Author

Created for monitoring Bangladeshi news content.

## Support

For issues and questions, please open an issue on GitHub.

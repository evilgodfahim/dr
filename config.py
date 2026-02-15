"""
Configuration file for Deshrupantor scraper
Modify these settings to customize the scraper behavior
"""

# Website Configuration
URL = "https://www.deshrupantor.com/printversion"
CSS_SELECTOR = ".each .title .link_overlay"

# FlareSolverr Configuration
USE_FLARESOLVERR = True
FLARESOLVERR_URL = "http://localhost:8191/v1"

# Button Clicking Configuration
CLICK_LOAD_MORE = True
LOAD_MORE_BUTTON_TEXT = "আরও দেখুন"
WAIT_AFTER_CLICK = 2  # seconds to wait after clicking each button

# Storage Configuration
XML_FILE = "articles.xml"
MAX_ARTICLES = 500

# Request Configuration
REQUEST_TIMEOUT = 60  # seconds (increased for FlareSolverr)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# GitHub Actions Configuration
# Runs daily at 6:00 AM Bangladesh Time (UTC+6 = 00:00 UTC)
# Edit .github/workflows/scraper.yml to change schedule

# Advanced Settings
ENCODING = 'utf-8'
PRETTY_PRINT = True
BACKUP_ON_ERROR = True

# Article ID Generation
# Options: 'url', 'title_url', 'timestamp'
ID_METHOD = 'url'

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# XML Settings
XML_INDENT = "  "  # Two spaces for indentation

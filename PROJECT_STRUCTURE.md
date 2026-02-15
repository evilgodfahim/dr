# Project Structure

Complete overview of the repository structure and file purposes.

```
deshrupantor-scraper/
│
├── .github/                          # GitHub-specific files
│   ├── workflows/
│   │   └── scraper.yml              # GitHub Actions workflow (runs every 5 min)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md            # Bug report template
│   │   └── feature_request.md       # Feature request template
│   └── pull_request_template.md     # PR template
│
├── scraper.py                        # Main scraper script ⭐
├── config.py                         # Configuration settings
├── test_scraper.py                   # Test suite
├── articles.xml                      # Scraped articles storage ⭐
│
├── requirements.txt                  # Python dependencies
├── requirements-dev.txt              # Development dependencies
│
├── setup.sh                          # Quick setup script
├── init_repo.sh                      # Git initialization script
│
├── README.md                         # Main documentation ⭐
├── QUICKSTART.md                     # Quick start guide
├── USAGE.md                          # Detailed usage examples
├── CONTRIBUTING.md                   # Contribution guidelines
├── CHANGELOG.md                      # Version history
├── PROJECT_STRUCTURE.md              # This file
│
├── LICENSE                           # MIT License
└── .gitignore                        # Git ignore rules
```

## Core Files (⭐)

### scraper.py
**Purpose**: Main application script  
**What it does**:
- Fetches articles from Deshrupantor website
- Parses HTML using BeautifulSoup
- Extracts article titles and URLs
- Generates unique IDs for articles
- Saves to XML with timestamps
- Maintains maximum 500 articles
- Handles errors gracefully

**Key Functions**:
- `fetch_articles()` - Scrapes website
- `load_existing_articles()` - Reads XML
- `save_articles_to_xml()` - Writes XML
- `update_articles()` - Main orchestration

### articles.xml
**Purpose**: Data storage  
**Structure**:
```xml
<articles last_updated="..." total_count="...">
  <article>
    <id>unique-hash</id>
    <title>Article Title</title>
    <url>https://...</url>
    <scraped_at>ISO-8601-timestamp</scraped_at>
  </article>
</articles>
```

### .github/workflows/scraper.yml
**Purpose**: Automation workflow  
**What it does**:
- Runs every 5 minutes (cron: `*/5 * * * *`)
- Sets up Python environment
- Installs dependencies
- Runs scraper
- Commits changes to Git
- Pushes to main branch

**Triggers**:
- Schedule (every 5 min)
- Manual (workflow_dispatch)
- Push to main (for testing)

## Configuration Files

### config.py
Centralized configuration:
- Website URL and CSS selector
- File paths and limits
- Request settings
- Logging configuration
- Retry and timeout settings

### requirements.txt
Python dependencies:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `lxml` - XML processing

### .gitignore
Excludes from Git:
- Python cache files
- Virtual environments
- IDE settings
- Log files
- Backup files

## Documentation Files

### README.md
Main project documentation:
- Overview and features
- Installation instructions
- Configuration guide
- XML format specification
- Dependencies
- Contributing guidelines
- License information

### QUICKSTART.md
Fast onboarding:
- 5-minute setup
- Common tasks
- Troubleshooting
- Quick examples

### USAGE.md
Detailed examples:
- Integration code
- Export scripts (JSON, CSV)
- Database storage
- Email notifications
- Search functionality
- API examples

### CONTRIBUTING.md
Development guide:
- How to report bugs
- Feature requests
- Pull request process
- Development setup
- Code style

### CHANGELOG.md
Version history:
- Release notes
- Feature additions
- Bug fixes
- Breaking changes

## Utility Scripts

### setup.sh
Quick environment setup:
- Checks Python installation
- Optionally creates venv
- Installs dependencies
- Provides next steps

### init_repo.sh
Git initialization:
- Checks Git installation
- Initializes repository
- Configures user
- Creates initial commit
- Provides GitHub instructions

### test_scraper.py
Validation suite:
- Tests article fetching
- Tests XML operations
- Validates XML structure
- Provides test summary

## GitHub Templates

### .github/ISSUE_TEMPLATE/bug_report.md
Structured bug reports:
- Description
- Reproduction steps
- Environment details
- Logs/screenshots

### .github/ISSUE_TEMPLATE/feature_request.md
Feature suggestions:
- Description
- Use case
- Proposed solution
- Alternatives

### .github/pull_request_template.md
PR standardization:
- Change description
- Type of change
- Testing checklist
- Review checklist

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ GitHub Actions (Every 5 minutes)                            │
│  ├── Checkout code                                          │
│  ├── Setup Python                                           │
│  ├── Install dependencies                                   │
│  └── Run scraper.py                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ scraper.py                                                  │
│  ├── Read config.py                                         │
│  ├── Fetch website HTML                                     │
│  ├── Parse with BeautifulSoup                               │
│  ├── Extract articles                                       │
│  ├── Load existing articles.xml                             │
│  ├── Merge and deduplicate                                  │
│  ├── Limit to MAX_ARTICLES (500)                            │
│  └── Save to articles.xml                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ articles.xml (Updated)                                      │
│  └── Pretty-printed XML with latest articles                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ GitHub Actions (Continued)                                  │
│  ├── Git add articles.xml                                   │
│  ├── Git commit (if changed)                                │
│  └── Git push to main                                       │
└─────────────────────────────────────────────────────────────┘
```

## Extending the Project

### Adding New Features

1. **Modify config.py** for new settings
2. **Update scraper.py** with new logic
3. **Add tests** to test_scraper.py
4. **Update docs** in relevant .md files
5. **Test locally** before pushing

### Adding New Scrapers

1. Copy scraper.py to scraper_[name].py
2. Create config_[name].py
3. Update workflow to run both
4. Use separate XML files

### Custom Integrations

See USAGE.md for examples:
- Export to different formats
- Database storage
- Email/webhook notifications
- Custom processing

## File Sizes (Approximate)

- `scraper.py`: ~6 KB
- `config.py`: ~1 KB
- `articles.xml`: ~50-500 KB (depending on count)
- `README.md`: ~5 KB
- Total repository: ~1-2 MB

## Maintenance

### Regular Tasks
- Monitor GitHub Actions quota
- Check for website structure changes
- Update dependencies periodically
- Review and close old issues

### Backups
- XML is backed up on errors
- Git history provides version control
- Export to other formats for safety

---

For questions about any file or component, please open an issue!

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-15

### Added
- Initial release of Deshrupantor news scraper
- Automatic scraping every 5 minutes via GitHub Actions
- XML storage with maximum 500 articles
- Article deduplication using unique IDs
- Comprehensive error handling and logging
- Configuration file for easy customization
- Test suite for validation
- Setup and initialization scripts
- Complete documentation (README, QUICKSTART, CONTRIBUTING)
- MIT License

### Features
- Scrapes articles from deshrupantor.com/printversion
- Saves article title, URL, ID, and timestamp
- Maintains chronological order (newest first)
- Automatic Git commits on changes
- Pretty-printed XML output
- Backup creation on XML errors

### Technical
- Python 3.8+ support
- Dependencies: requests, beautifulsoup4, lxml
- GitHub Actions workflow with scheduled runs
- Cross-platform compatibility (Linux, macOS, Windows)

## [Unreleased]

### Planned
- Support for multiple news sources
- Email notifications for new articles
- Web dashboard for viewing articles
- Database storage option (SQLite/PostgreSQL)
- RSS feed generation
- Article content extraction (full text)
- Category/topic classification
- Search functionality
- Export to JSON/CSV formats
- Docker support

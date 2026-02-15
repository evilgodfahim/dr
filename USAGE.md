# Usage Guide

Detailed examples and use cases for the Deshrupantor scraper.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Advanced Configuration](#advanced-configuration)
3. [Integration Examples](#integration-examples)
4. [Common Workflows](#common-workflows)
5. [API & Parsing](#api--parsing)

---

## Basic Usage

### Running Locally

```bash
# Simple run
python scraper.py

# With verbose output
python scraper.py --verbose  # (if implemented)
```

### Viewing Results

```bash
# Pretty print XML
xmllint --format articles.xml

# Count articles
grep -c "<article>" articles.xml

# View latest articles
head -n 50 articles.xml
```

### Testing

```bash
# Run all tests
python test_scraper.py

# Test specific functionality
python -c "from scraper import fetch_articles; print(len(fetch_articles()))"
```

---

## Advanced Configuration

### Custom CSS Selector

If the website structure changes, update `config.py`:

```python
# Original
CSS_SELECTOR = ".each .title .link_overlay"

# Custom selector
CSS_SELECTOR = "article h2 a"  # Example
```

### Change Storage Limit

```python
# In config.py
MAX_ARTICLES = 1000  # Store more articles
MAX_ARTICLES = 100   # Store fewer articles
```

### Multiple Instances

Run multiple scrapers for different sections:

```bash
# Create separate configs
cp scraper.py scraper_politics.py
cp config.py config_politics.py

# Edit config_politics.py with different URL/selector
# Edit scraper_politics.py to import config_politics
```

---

## Integration Examples

### Python Integration

```python
from scraper import fetch_articles, load_existing_articles

# Get latest articles
articles = fetch_articles()

# Process each article
for article in articles:
    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"ID: {article['id']}")
    print()

# Load from XML
existing = load_existing_articles()
print(f"Total stored: {len(existing)}")
```

### Parse XML with Python

```python
import xml.etree.ElementTree as ET

tree = ET.parse('articles.xml')
root = tree.getroot()

# Get all articles
for article in root.findall('article'):
    title = article.find('title').text
    url = article.find('url').text
    scraped_at = article.find('scraped_at').text
    
    print(f"{title} - {scraped_at}")
```

### Export to JSON

```python
import xml.etree.ElementTree as ET
import json

tree = ET.parse('articles.xml')
root = tree.getroot()

articles = []
for article in root.findall('article'):
    articles.append({
        'id': article.find('id').text,
        'title': article.find('title').text,
        'url': article.find('url').text,
        'scraped_at': article.find('scraped_at').text
    })

with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
```

### Export to CSV

```python
import xml.etree.ElementTree as ET
import csv

tree = ET.parse('articles.xml')
root = tree.getroot()

with open('articles.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Title', 'URL', 'Scraped At'])
    
    for article in root.findall('article'):
        writer.writerow([
            article.find('id').text,
            article.find('title').text,
            article.find('url').text,
            article.find('scraped_at').text
        ])
```

---

## Common Workflows

### Daily Digest Email

```python
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

# Get articles from last 24 hours
tree = ET.parse('articles.xml')
root = tree.getroot()

yesterday = datetime.now() - timedelta(days=1)
recent = []

for article in root.findall('article'):
    scraped = datetime.fromisoformat(article.find('scraped_at').text)
    if scraped > yesterday:
        recent.append({
            'title': article.find('title').text,
            'url': article.find('url').text
        })

# Send email (configure SMTP settings)
if recent:
    body = "Today's Articles:\n\n"
    for a in recent:
        body += f"- {a['title']}\n  {a['url']}\n\n"
    
    # Send email code here...
```

### Webhook Notification

```python
import requests
import xml.etree.ElementTree as ET

def notify_new_articles(webhook_url):
    tree = ET.parse('articles.xml')
    root = tree.getroot()
    
    # Get latest article
    article = root.find('article')
    if article:
        payload = {
            'title': article.find('title').text,
            'url': article.find('url').text,
            'text': f"New article: {article.find('title').text}"
        }
        requests.post(webhook_url, json=payload)

# Usage
notify_new_articles('https://hooks.slack.com/services/YOUR/WEBHOOK/URL')
```

### Database Storage

```python
import sqlite3
import xml.etree.ElementTree as ET

# Create database
conn = sqlite3.connect('articles.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id TEXT PRIMARY KEY,
        title TEXT,
        url TEXT,
        scraped_at TEXT
    )
''')

# Import from XML
tree = ET.parse('articles.xml')
root = tree.getroot()

for article in root.findall('article'):
    c.execute('''
        INSERT OR REPLACE INTO articles VALUES (?, ?, ?, ?)
    ''', (
        article.find('id').text,
        article.find('title').text,
        article.find('url').text,
        article.find('scraped_at').text
    ))

conn.commit()
conn.close()
```

---

## API & Parsing

### Read XML in JavaScript

```javascript
// In Node.js
const fs = require('fs');
const xml2js = require('xml2js');

fs.readFile('articles.xml', (err, data) => {
    xml2js.parseString(data, (err, result) => {
        const articles = result.articles.article;
        articles.forEach(article => {
            console.log(article.title[0]);
            console.log(article.url[0]);
        });
    });
});
```

### Parse XML in PHP

```php
<?php
$xml = simplexml_load_file('articles.xml');

foreach ($xml->article as $article) {
    echo $article->title . "\n";
    echo $article->url . "\n";
    echo "---\n";
}
?>
```

### Search Articles

```python
import xml.etree.ElementTree as ET

def search_articles(keyword):
    tree = ET.parse('articles.xml')
    root = tree.getroot()
    
    results = []
    for article in root.findall('article'):
        title = article.find('title').text.lower()
        if keyword.lower() in title:
            results.append({
                'title': article.find('title').text,
                'url': article.find('url').text
            })
    
    return results

# Usage
matches = search_articles('রাজনীতি')
for match in matches:
    print(match['title'])
```

---

## Tips & Best Practices

1. **Always backup before major changes**
   ```bash
   cp articles.xml articles.xml.backup
   ```

2. **Monitor GitHub Actions quota**
   - Free tier: 2,000 minutes/month
   - Every 5 min = ~8,640 runs/month
   - Each run takes ~1 minute
   - Stay well within limits

3. **Handle encoding properly**
   - Always use UTF-8 for Bengali text
   - Verify encoding in editors

4. **Test locally first**
   - Run scraper locally before pushing
   - Verify XML output
   - Check for errors

5. **Keep logs for debugging**
   - Review GitHub Actions logs
   - Add logging for custom changes

---

## Troubleshooting

### Common Issues

**Issue**: XML file is empty
```bash
# Solution: Run scraper manually
python scraper.py
```

**Issue**: Encoding errors with Bengali text
```python
# Solution: Ensure UTF-8 everywhere
with open('articles.xml', 'r', encoding='utf-8') as f:
    content = f.read()
```

**Issue**: GitHub Actions fails
```bash
# Check logs in Actions tab
# Verify requirements.txt
# Test locally first
```

---

## More Examples

See the `examples/` directory (if available) for more use cases and integrations.

For questions or issues, please open a GitHub issue!

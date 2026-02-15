#!/usr/bin/env python3
"""
Deshrupantor News Scraper with FlareSolverr
Scrapes articles from deshrupantor.com and saves them to XML
Supports Cloudflare bypass via FlareSolverr
"""

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import hashlib
from datetime import datetime
import logging
import sys
import time
import json

# Import configuration
try:
    from config import (
        URL, CSS_SELECTOR as SELECTOR, MAX_ARTICLES, XML_FILE,
        REQUEST_TIMEOUT, USER_AGENT, LOG_LEVEL, LOG_FORMAT,
        USE_FLARESOLVERR, FLARESOLVERR_URL, CLICK_LOAD_MORE,
        LOAD_MORE_BUTTON_TEXT, WAIT_AFTER_CLICK
    )
except ImportError:
    # Fallback to defaults if config.py not found
    URL = "https://www.deshrupantor.com/printversion"
    SELECTOR = ".each .title .link_overlay"
    MAX_ARTICLES = 500
    XML_FILE = "articles.xml"
    REQUEST_TIMEOUT = 30
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    LOG_LEVEL = "INFO"
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    USE_FLARESOLVERR = True
    FLARESOLVERR_URL = "http://localhost:8191/v1"
    CLICK_LOAD_MORE = True
    LOAD_MORE_BUTTON_TEXT = "আরও দেখুন"
    WAIT_AFTER_CLICK = 5

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def generate_article_id(title, url):
    """Generate unique ID for article based on URL"""
    unique_string = f"{url}"
    return hashlib.md5(unique_string.encode()).hexdigest()


def fetch_with_flaresolverr(url):
    """Fetch URL using FlareSolverr to bypass Cloudflare"""
    logger.info(f"Fetching via FlareSolverr: {url}")
    
    try:
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": REQUEST_TIMEOUT * 1000,  # Convert to milliseconds
            "returnRawHtml": True
        }
        
        response = requests.post(
            FLARESOLVERR_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT + 10
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'ok':
            solution = data.get('solution', {})
            html = solution.get('response', '')
            logger.info("Successfully fetched via FlareSolverr")
            return html
        else:
            error_msg = data.get('message', 'Unknown error')
            logger.error(f"FlareSolverr error: {error_msg}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"FlareSolverr request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"FlareSolverr unexpected error: {e}")
        return None


def fetch_with_selenium_and_click(url):
    """Fetch URL using FlareSolverr with button clicking support"""
    if not CLICK_LOAD_MORE:
        return fetch_with_flaresolverr(url)
    
    logger.info(f"Fetching with button click via FlareSolverr: {url}")
    
    try:
        # First, get the page and create session
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": REQUEST_TIMEOUT * 1000,
            "returnRawHtml": True,
            "session": "scraper_session"
        }
        
        response = requests.post(
            FLARESOLVERR_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT + 10
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') != 'ok':
            logger.error(f"FlareSolverr initial fetch failed: {data.get('message')}")
            return None
        
        # Click all "আরও দেখুন" buttons one by one
        logger.info(f"Searching for '{LOAD_MORE_BUTTON_TEXT}' buttons...")
        
        # Use JavaScript to find and click all buttons
        click_all_script = f"""
        (function() {{
            const buttons = Array.from(document.querySelectorAll('a, button')).filter(el => 
                el.textContent.includes('{LOAD_MORE_BUTTON_TEXT}')
            );
            console.log('Found ' + buttons.length + ' buttons');
            
            async function clickAll() {{
                for (let i = 0; i < buttons.length; i++) {{
                    console.log('Clicking button ' + (i+1) + '/' + buttons.length);
                    buttons[i].click();
                    await new Promise(resolve => setTimeout(resolve, {WAIT_AFTER_CLICK * 1000}));
                }}
            }}
            
            clickAll();
            return buttons.length;
        }})();
        """
        
        execute_payload = {
            "cmd": "request.execute",
            "session": "scraper_session",
            "script": click_all_script,
            "maxTimeout": (REQUEST_TIMEOUT + 30) * 1000
        }
        
        try:
            exec_response = requests.post(
                FLARESOLVERR_URL,
                json=execute_payload,
                timeout=REQUEST_TIMEOUT + 40
            )
            
            if exec_response.status_code == 200:
                exec_data = exec_response.json()
                button_count = exec_data.get('solution', {}).get('result', 0)
                logger.info(f"Clicked {button_count} '{LOAD_MORE_BUTTON_TEXT}' buttons, waiting for content to load...")
                
                # Wait additional time for all content to load
                time.sleep(WAIT_AFTER_CLICK)
            else:
                logger.warning("Button clicking may have failed, continuing anyway...")
                
        except Exception as e:
            logger.warning(f"Could not execute button clicks: {e}, continuing with initial page...")
        
        # Get the final HTML after all clicks
        final_payload = {
            "cmd": "request.get",
            "url": url,
            "session": "scraper_session",
            "maxTimeout": REQUEST_TIMEOUT * 1000,
            "returnRawHtml": True
        }
        
        final_response = requests.post(
            FLARESOLVERR_URL,
            json=final_payload,
            timeout=REQUEST_TIMEOUT + 10
        )
        
        if final_response.status_code == 200:
            final_data = final_response.json()
            html = final_data.get('solution', {}).get('response', '')
        else:
            # Fallback to initial HTML
            html = data.get('solution', {}).get('response', '')
        
        logger.info("Successfully fetched page content with expanded sections")
        return html
        
    except requests.RequestException as e:
        logger.error(f"FlareSolverr request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"FlareSolverr unexpected error: {e}")
        return None


def fetch_html(url):
    """Fetch HTML with or without FlareSolverr"""
    if USE_FLARESOLVERR:
        return fetch_with_selenium_and_click(url)
    else:
        # Regular requests without FlareSolverr
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            logger.error(f"Regular fetch failed: {e}")
            return None


def fetch_articles():
    """Fetch articles from the website"""
    logger.info(f"Fetching articles from {URL}")
    
    try:
        html = fetch_html(URL)
        
        if not html:
            logger.error("Failed to fetch HTML content")
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all article links using the selector
        article_elements = soup.select(SELECTOR)
        
        articles = []
        for element in article_elements:
            title = element.get('title', '').strip()
            url = element.get('href', '').strip()
            
            # Make URL absolute if relative
            if url.startswith('//'):
                url = 'https:' + url
            elif url.startswith('/'):
                url = 'https://www.deshrupantor.com' + url
            
            if title and url:
                article_id = generate_article_id(title, url)
                articles.append({
                    'id': article_id,
                    'title': title,
                    'url': url,
                    'scraped_at': datetime.now().isoformat()
                })
        
        logger.info(f"Found {len(articles)} articles")
        return articles
        
    except requests.RequestException as e:
        logger.error(f"Error fetching articles: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []


def load_existing_articles():
    """Load existing articles from XML file"""
    if not os.path.exists(XML_FILE):
        logger.info("No existing XML file found, creating new one")
        return {}
    
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        
        existing = {}
        for article in root.findall('article'):
            article_id = article.find('id').text
            existing[article_id] = {
                'id': article_id,
                'title': article.find('title').text,
                'url': article.find('url').text,
                'scraped_at': article.find('scraped_at').text
            }
        
        logger.info(f"Loaded {len(existing)} existing articles")
        return existing
        
    except ET.ParseError as e:
        logger.error(f"Error parsing XML file: {e}")
        logger.info("Creating backup and starting fresh")
        if os.path.exists(XML_FILE):
            os.rename(XML_FILE, f"{XML_FILE}.backup")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error loading XML: {e}")
        return {}


def save_articles_to_xml(articles_dict):
    """Save articles to XML file"""
    logger.info(f"Saving {len(articles_dict)} articles to XML")
    
    try:
        # Create root element
        root = ET.Element('articles')
        root.set('last_updated', datetime.now().isoformat())
        root.set('total_count', str(len(articles_dict)))
        
        # Sort by scraped_at (newest first)
        sorted_articles = sorted(
            articles_dict.values(),
            key=lambda x: x['scraped_at'],
            reverse=True
        )
        
        # Add articles
        for article in sorted_articles:
            article_elem = ET.SubElement(root, 'article')
            
            id_elem = ET.SubElement(article_elem, 'id')
            id_elem.text = article['id']
            
            title_elem = ET.SubElement(article_elem, 'title')
            title_elem.text = article['title']
            
            url_elem = ET.SubElement(article_elem, 'url')
            url_elem.text = article['url']
            
            scraped_elem = ET.SubElement(article_elem, 'scraped_at')
            scraped_elem.text = article['scraped_at']
        
        # Pretty print XML
        xml_string = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(
            indent="  ",
            encoding='utf-8'
        )
        
        # Write to file
        with open(XML_FILE, 'wb') as f:
            f.write(xml_string)
        
        logger.info(f"Successfully saved articles to {XML_FILE}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving XML file: {e}")
        return False


def update_articles():
    """Main function to update articles"""
    logger.info("=" * 50)
    logger.info("Starting article update")
    logger.info("=" * 50)
    
    # Fetch new articles
    new_articles = fetch_articles()
    
    if not new_articles:
        logger.warning("No articles fetched, skipping update")
        return False
    
    # Load existing articles
    existing_articles = load_existing_articles()
    
    # Merge new and existing articles
    added_count = 0
    for article in new_articles:
        if article['id'] not in existing_articles:
            existing_articles[article['id']] = article
            added_count += 1
        else:
            # Update scraped_at for existing articles
            existing_articles[article['id']]['scraped_at'] = article['scraped_at']
    
    logger.info(f"Added {added_count} new articles")
    
    # Limit to MAX_ARTICLES (keep newest)
    if len(existing_articles) > MAX_ARTICLES:
        sorted_articles = sorted(
            existing_articles.values(),
            key=lambda x: x['scraped_at'],
            reverse=True
        )
        existing_articles = {
            article['id']: article 
            for article in sorted_articles[:MAX_ARTICLES]
        }
        logger.info(f"Trimmed to {MAX_ARTICLES} articles")
    
    # Save to XML
    success = save_articles_to_xml(existing_articles)
    
    if success:
        logger.info("Update completed successfully")
        logger.info(f"Total articles in XML: {len(existing_articles)}")
    else:
        logger.error("Update failed")
    
    logger.info("=" * 50)
    return success


if __name__ == "__main__":
    try:
        update_articles()
    except KeyboardInterrupt:
        logger.info("\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

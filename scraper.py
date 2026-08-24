#!/usr/bin/env python3
"""
Deshrupantor News Scraper with FlareSolverr
Scrapes articles from deshrupantor.com and saves them as RSS 2.0 feeds
Supports Cloudflare bypass via FlareSolverr
"""

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
from email.utils import formatdate, parsedate_to_datetime
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
    LOAD_MORE_BUTTON_TEXT = "আরও"
    WAIT_AFTER_CLICK = 5

# Opinion section config
OPINION_URL = "https://www.deshrupantor.com/topic/%E0%A6%9A%E0%A6%BF%E0%A6%A8%E0%A7%8D%E0%A6%A4%E0%A6%BE"
OPINION_SELECTOR = ".tag_title_holder h2.title a.link_overlay"
OPINION_XML_FILE = "opinion.xml"

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def generate_article_id(url):
    """Generate unique ID for article based on URL"""
    return hashlib.md5(url.encode()).hexdigest()


def to_rfc2822(iso_str):
    """Convert an ISO 8601 string to RFC 2822 format used in RSS <pubDate>."""
    try:
        dt = datetime.fromisoformat(iso_str)
        return formatdate(dt.timestamp(), usegmt=True)
    except Exception:
        return formatdate(usegmt=True)


def from_rfc2822(rfc_str):
    """Parse an RFC 2822 date string back to ISO 8601 for internal sorting/storage."""
    try:
        return parsedate_to_datetime(rfc_str).isoformat()
    except Exception:
        return datetime.now().isoformat()


# ---------------------------------------------------------------------------
# Fetch layer (unchanged)
# ---------------------------------------------------------------------------

def fetch_with_flaresolverr(url):
    """Fetch URL using FlareSolverr to bypass Cloudflare"""
    logger.info(f"Fetching via FlareSolverr: {url}")
    try:
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": REQUEST_TIMEOUT * 1000,
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
            html = data.get('solution', {}).get('response', '')
            logger.info("Successfully fetched via FlareSolverr")
            return html
        else:
            logger.error(f"FlareSolverr error: {data.get('message', 'Unknown error')}")
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

        logger.info(f"Searching for '{LOAD_MORE_BUTTON_TEXT}' buttons...")
        click_all_script = f"""
        (function() {{
            const buttons = Array.from(document.querySelectorAll('a, button')).filter(el =>
                el.textContent && el.textContent.trim() === '{LOAD_MORE_BUTTON_TEXT}'
            );
            console.log('Found ' + buttons.length + ' buttons');
            async function clickAll() {{
                for (let i = 0; i < buttons.length; i++) {{
                    console.log('Clicking button ' + (i+1) + '/' + buttons.length);
                    try {{ buttons[i].click(); }} catch(e) {{ console.log('click failed', e); }}
                    await new Promise(resolve => setTimeout(resolve, {WAIT_AFTER_CLICK * 1000}));
                }}
            }}
            return (async function() {{
                await clickAll();
                return buttons.length;
            }})();
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
                logger.info(f"Clicked {button_count} '{LOAD_MORE_BUTTON_TEXT}' buttons, waiting for content...")
                time.sleep(WAIT_AFTER_CLICK)
            else:
                logger.warning("Button clicking may have failed, continuing anyway...")
        except Exception as e:
            logger.warning(f"Could not execute button clicks: {e}, continuing with initial page...")

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
            html = final_response.json().get('solution', {}).get('response', '')
        else:
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
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            logger.error(f"Regular fetch failed: {e}")
            return None


def fetch_articles(url, selector, base_url="https://www.deshrupantor.com"):
    """Fetch articles from a given URL using a CSS selector"""
    logger.info(f"Fetching articles from {url}")
    try:
        html = fetch_html(url)
        if not html:
            logger.error("Failed to fetch HTML content")
            return []

        soup = BeautifulSoup(html, 'html.parser')
        article_elements = soup.select(selector)

        articles = []
        for element in article_elements:
            title = element.get('title', '').strip()
            href = element.get('href', '').strip()

            if href.startswith('//'):
                href = 'https:' + href
            elif href.startswith('/'):
                href = base_url + href

            if title and href:
                articles.append({
                    'id': generate_article_id(href),
                    'title': title,
                    'url': href,
                    'scraped_at': datetime.now().isoformat()  # ISO internally
                })

        logger.info(f"Found {len(articles)} articles")
        return articles

    except Exception as e:
        logger.error(f"Unexpected error fetching articles: {e}")
        return []


# ---------------------------------------------------------------------------
# RSS 2.0 persistence
# ---------------------------------------------------------------------------

def load_existing_articles(xml_file):
    """Load existing articles from an RSS 2.0 XML file.

    Falls back gracefully to the old custom <articles>/<article> format so
    existing files aren't lost on first run after upgrading.
    """
    if not os.path.exists(xml_file):
        logger.info(f"No existing {xml_file} found, will create new one")
        return {}
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        existing = {}

        if root.tag == 'rss':
            # --- RSS 2.0 format ---
            channel = root.find('channel')
            items = channel.findall('item') if channel is not None else []
            for item in items:
                guid_elem = item.find('guid')
                url = (guid_elem.text or '').strip() if guid_elem is not None else ''
                if not url:
                    link_elem = item.find('link')
                    url = (link_elem.text or '').strip() if link_elem is not None else ''

                title_elem = item.find('title')
                title = (title_elem.text or '').strip() if title_elem is not None else ''

                pub_date_elem = item.find('pubDate')
                # Convert RFC 2822 → ISO for internal sorting
                scraped_at = (
                    from_rfc2822(pub_date_elem.text)
                    if pub_date_elem is not None and pub_date_elem.text
                    else datetime.now().isoformat()
                )

                if url:
                    article_id = generate_article_id(url)
                    existing[article_id] = {
                        'id': article_id,
                        'title': title,
                        'url': url,
                        'scraped_at': scraped_at,
                    }
        else:
            # --- Legacy custom format fallback ---
            for article in root.findall('article'):
                article_id = article.find('id').text
                url_elem = article.find('url')
                title_elem = article.find('title')
                scraped_at_elem = article.find('scraped_at')
                existing[article_id] = {
                    'id': article_id,
                    'title': title_elem.text if title_elem is not None else '',
                    'url': url_elem.text if url_elem is not None else '',
                    'scraped_at': scraped_at_elem.text if scraped_at_elem is not None else datetime.now().isoformat(),
                }

        logger.info(f"Loaded {len(existing)} existing articles from {xml_file}")
        return existing

    except ET.ParseError as e:
        logger.error(f"Error parsing {xml_file}: {e}")
        if os.path.exists(xml_file):
            os.rename(xml_file, f"{xml_file}.backup")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error loading {xml_file}: {e}")
        return {}


def save_articles_to_xml(articles_dict, xml_file, feed_title="", feed_link="", feed_description=""):
    """Save articles as a valid RSS 2.0 feed readable by Inoreader and other readers."""
    logger.info(f"Saving {len(articles_dict)} articles to {xml_file}")
    try:
        root = ET.Element('rss')
        root.set('version', '2.0')

        channel = ET.SubElement(root, 'channel')
        ET.SubElement(channel, 'title').text = feed_title
        ET.SubElement(channel, 'link').text = feed_link
        ET.SubElement(channel, 'description').text = feed_description
        ET.SubElement(channel, 'lastBuildDate').text = formatdate(usegmt=True)
        ET.SubElement(channel, 'generator').text = 'Deshrupantor Scraper'

        sorted_articles = sorted(
            articles_dict.values(),
            key=lambda x: x['scraped_at'],
            reverse=True
        )

        for article in sorted_articles:
            item = ET.SubElement(channel, 'item')
            ET.SubElement(item, 'title').text = article['title']
            ET.SubElement(item, 'link').text = article['url']
            guid = ET.SubElement(item, 'guid')
            guid.set('isPermaLink', 'true')
            guid.text = article['url']
            # Convert ISO → RFC 2822 only at write time
            ET.SubElement(item, 'pubDate').text = to_rfc2822(article['scraped_at'])

        xml_string = minidom.parseString(
            ET.tostring(root, encoding='utf-8')
        ).toprettyxml(indent="  ", encoding='utf-8')

        with open(xml_file, 'wb') as f:
            f.write(xml_string)

        logger.info(f"Successfully saved to {xml_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving {xml_file}: {e}")
        return False


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def update_articles(url, selector, xml_file, max_articles=MAX_ARTICLES,
                    feed_title="", feed_description=""):
    """Fetch, merge, trim, and save articles for a single source."""
    logger.info("=" * 50)
    logger.info(f"Updating: {xml_file} <- {url}")
    logger.info("=" * 50)

    new_articles = fetch_articles(url, selector)
    if not new_articles:
        logger.warning("No articles fetched, skipping update")
        return False

    existing_articles = load_existing_articles(xml_file)

    added_count = 0
    for article in new_articles:
        if article['id'] not in existing_articles:
            existing_articles[article['id']] = article
            added_count += 1
        else:
            existing_articles[article['id']]['scraped_at'] = article['scraped_at']

    logger.info(f"Added {added_count} new articles")

    if len(existing_articles) > max_articles:
        sorted_articles = sorted(
            existing_articles.values(),
            key=lambda x: x['scraped_at'],
            reverse=True
        )
        existing_articles = {a['id']: a for a in sorted_articles[:max_articles]}
        logger.info(f"Trimmed to {max_articles} articles")

    success = save_articles_to_xml(
        existing_articles, xml_file,
        feed_title=feed_title,
        feed_link=url,
        feed_description=feed_description,
    )
    if success:
        logger.info(f"Update complete. Total in {xml_file}: {len(existing_articles)}")
    else:
        logger.error("Update failed")

    logger.info("=" * 50)
    return success


if __name__ == "__main__":
    try:
        update_articles(
            URL, SELECTOR, XML_FILE,
            feed_title="Deshrupantor - Print Version",
            feed_description="Print edition articles from Deshrupantor",
        )
        update_articles(
            OPINION_URL, OPINION_SELECTOR, OPINION_XML_FILE,
            feed_title="Deshrupantor - Opinion",
            feed_description="Opinion articles from Deshrupantor",
        )
    except KeyboardInterrupt:
        logger.info("\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

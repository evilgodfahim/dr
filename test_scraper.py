#!/usr/bin/env python3
"""
Test script for the Deshrupantor scraper
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from scraper import fetch_articles, load_existing_articles, save_articles_to_xml
import xml.etree.ElementTree as ET


def test_fetch_articles():
    """Test fetching articles from website"""
    print("Testing article fetching...")
    articles = fetch_articles()
    
    if not articles:
        print("❌ No articles fetched!")
        return False
    
    print(f"✅ Fetched {len(articles)} articles")
    
    # Display first few articles
    for i, article in enumerate(articles[:3], 1):
        print(f"\n  Article {i}:")
        print(f"    Title: {article['title'][:60]}...")
        print(f"    URL: {article['url']}")
        print(f"    ID: {article['id']}")
    
    return True


def test_xml_operations():
    """Test XML save and load"""
    print("\nTesting XML operations...")
    
    # Create test data
    test_articles = {
        'test1': {
            'id': 'test1',
            'title': 'Test Article 1',
            'url': 'https://example.com/1',
            'scraped_at': '2026-02-15T10:00:00'
        },
        'test2': {
            'id': 'test2',
            'title': 'Test Article 2',
            'url': 'https://example.com/2',
            'scraped_at': '2026-02-15T10:01:00'
        }
    }
    
    # Save
    test_file = 'test_articles.xml'
    from scraper import XML_FILE
    import scraper
    scraper.XML_FILE = test_file
    
    success = save_articles_to_xml(test_articles)
    if not success:
        print("❌ Failed to save XML")
        return False
    
    print("✅ XML saved successfully")
    
    # Load
    loaded = load_existing_articles()
    if len(loaded) != 2:
        print(f"❌ Expected 2 articles, got {len(loaded)}")
        return False
    
    print("✅ XML loaded successfully")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    
    return True


def test_xml_validation():
    """Validate the actual articles.xml file"""
    print("\nValidating articles.xml...")
    
    if not os.path.exists('articles.xml'):
        print("⚠️  articles.xml doesn't exist yet")
        return True
    
    try:
        tree = ET.parse('articles.xml')
        root = tree.getroot()
        
        article_count = len(root.findall('article'))
        print(f"✅ XML is valid with {article_count} articles")
        
        return True
    except ET.ParseError as e:
        print(f"❌ XML parsing error: {e}")
        return False


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("DESHRUPANTOR SCRAPER TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Fetch Articles", test_fetch_articles),
        ("XML Operations", test_xml_operations),
        ("XML Validation", test_xml_validation)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {name}")
        print('='*60)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    return all(r for _, r in results)


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

from processor import Processor
from retriever import Retriever
from blog_scraper_simple import WebScraper
import json
import logging

url = "https://www.gov.uk/foreign-travel-advice/mexico"


scraper = WebScraper()
doc = scraper.scrape(url)
logging.info('scraping')

print(doc)

print()

if not doc or 'body' not in doc or 'titles' not in doc or 'url' not in doc:
    logging.error("Scraped document is missing required fields.")

logging.info(f"Scraped document: {doc['titles']} from {doc['url']}")
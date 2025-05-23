from processor import Processor
from retriever import Retriever
from blog_scraper_simple import WebScraper
import json
import logging

docs_file = 'scraped_docs.json'

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_scraped():
    try:
        with open('scraped_docs.json', 'r') as f1:
            return json.load(f1)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def update_scraped(docs):
    with open(docs_file, 'w') as f2:
        json.dump(docs, f2, indent=4)

def fetch_new(file):
    try:
        with open(file, 'w') as f3:
            return json.load(f3)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def in_pipeline(url):

    scraped = load_scraped()

    if url in scraped:
        logging.info('Doc already scraped')
        return


    scraper = WebScraper()
    doc = scraper.scrape(url)

    if not doc or 'body' not in doc or 'titles' not in doc or 'url' not in doc:
        logging.error("Scraped document is missing required fields.")
        return

    logging.info(f"Scraped document: {doc['titles']} from {doc['url']}")

    processor = Processor()

    processor.split_text()
    processor.transform()
    processor.insert()

    scraped[url] = 'true'
    update_scraped(scraped)

    logging.info("Document processed and stored.")

if __name__ == "__main__":

    to_fetch = fetch_new('new_docs.json')
    if to_fetch:
        in_pipeline(to_fetch)
    else:
        logging.warning("No URL provided.")
from processor import Processor
from retriever import Retriever
from blog_scraper_simple import WebScraper
import json

with open('Docs.json', 'r') as f1:
    docs = json.load(f1)

def in_pipeline(doc):

    scraper = WebScraper()
    doc = scraper.scrape(doc)

    print(doc['body'], doc['titles'], None, doc['url'])

    processor = Processor()

    processor.split_text()
    processor.transform()
    processor.insert()
from processor import Processor
from retriever import Retriever
from blog_scraper_simple import WebScraper
import json

def in_pipeline(url):

    with open('Docs.json', 'w') as f1:
        scrapped_docs = json.load(f1)

        exists = url in scrapped_docs

        if not exists:

            scraper = WebScraper()
            doc = scraper.scrape(url)

            print(doc['body'], doc['titles'], None, doc['url'])

            processor = Processor()

            processor.split_text()
            processor.transform()
            processor.insert()

            scrapped_docs[url] = 'true'

        else:
            print('Document already scraped...')

if __name__ == "__main__":

    user_link = input('Enter url site: ')
    in_pipeline(user_link)
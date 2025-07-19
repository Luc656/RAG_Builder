from processor import Processor
from blog_scraper_simple import WebScraper


blogs = [
    "https://www.gov.uk/foreign-travel-advice/mexico"
]

if __name__ == '__main__':

    scraper = WebScraper()
    doc = scraper.scrape(url=blogs[0])

    print(doc['body'], doc['titles'], None, doc['url'])

    #processor = Processor(doc['body'])

    #processor.chunk_document()
    #processor.transform()
    #pipeline.insert()



from processor import Processor
from retriever import Retriever
from blog_scraper_simple import WebScraper


blogs = [
    'https://www.myitaliandiaries.com/my-favourite-things-to-do-in-livorno/',
    'https://www.myitaliandiaries.com/things-to-do-in-ferrara-europes-first-modern-city/',
    'https://www.myitaliandiaries.com/easy-day-trips-from-venice-by-train/',
    'https://www.theblondeabroad.com/best-things-to-do-on-the-amalfi-coast/'
]

def in_pipeline(doc):

    scraper = WebScraper()
    doc = scraper.scrape(doc)

    print(doc['body'], doc['titles'], None, doc['url'])

    processor = Processor()

    processor.split_text()
    processor.transform()
    processor.insert()
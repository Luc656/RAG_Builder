from blog_pipeline_v2 import Pipeline
from blog_scraper_simple import WebScraper


blogs = [
    'https://www.myitaliandiaries.com/my-favourite-things-to-do-in-livorno/',
    'https://www.myitaliandiaries.com/things-to-do-in-ferrara-europes-first-modern-city/',
    'https://www.myitaliandiaries.com/easy-day-trips-from-venice-by-train/',
    'https://www.theblondeabroad.com/best-things-to-do-on-the-amalfi-coast/'
]

if __name__ == '__main__':

    scraper = WebScraper()
    doc = scraper.scrape(url=blogs[0])

    print(doc['body'], doc['titles'], None, doc['url'])

    pipeline = Pipeline(doc['body'], doc['titles'], None, doc['url'])

    pipeline.split_text()
    pipeline.transform()
    pipeline.insert()



from news_pipeline import get_urls
from news_scraper import NewsScraper

scraper = NewsScraper()

API_KEY = os.getenv("NEWS_API_KEY")
site = "https://newsapi.org/v2/everything"


params = {
    'q' : 'geopolitics OR international affairs OR diplomacy OR war OR global economy',
    'apiKey' : API_KEY,
    'language' : 'en',
    'sources' : "bbc-news, al-jazeera-english, the-guardian-uk, reuters"
}

urls = get_urls(api_key=API_KEY, site=site, params=params)

for url in urls:

    scraper.url = url
    scraper.fetch_html()
    try:
        data = scaper.parse()
    except NotImplementedError:
        data = scraper.extract_with_newspaper()
    print(data)
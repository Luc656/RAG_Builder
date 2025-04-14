
from blog_scraper import BlogScraper
#
# scraper = NewsScraper()
#
# API_KEY = os.getenv("NEWS_API_KEY")
# site = "https://newsapi.org/v2/everything"
#
#
# params = {
#     'q' : 'geopolitics OR international affairs OR diplomacy OR war OR global economy',
#     'apiKey' : API_KEY,
#     'language' : 'en',
#     'sources' : "bbc-news, al-jazeera-english, the-guardian-uk, reuters"
# }
#
# urls = get_urls(api_key=API_KEY, site=site, params=params)
#
# for url in urls:
#
#     scraper.url = url
#     scraper.fetch_html()
#     try:
#         data = scaper.parse()
#     except NotImplementedError:
#         data = scraper.extract_with_newspaper()
#     print(data)

blogs = [
    'https://www.myitaliandiaries.com/my-favourite-things-to-do-in-livorno/',
    'https://www.myitaliandiaries.com/things-to-do-in-ferrara-europes-first-modern-city/',
    'https://www.myitaliandiaries.com/easy-day-trips-from-venice-by-train/',
    'https://www.theblondeabroad.com/best-things-to-do-on-the-amalfi-coast/'
]

scraper = BlogScraper("https://www.myitaliandiaries.com")

posts = scraper.scrape(
    post = 'my-favourite-things-to-do-in-livorno',
    title = 'h1',
    link = 'https://www.myitaliandiaries.com/my-favourite-things-to-do-in-livorno/',
    content = 'dynamic-entry-content',
    url = 'https://www.myitaliandiaries.com/my-favourite-things-to-do-in-livorno/'

)

for post in posts:
    print(post)
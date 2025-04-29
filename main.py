from blog_scraper_simple import WebScraper


blogs = [
    'https://www.myitaliandiaries.com/my-favourite-things-to-do-in-livorno/',
    'https://www.myitaliandiaries.com/things-to-do-in-ferrara-europes-first-modern-city/',
    'https://www.myitaliandiaries.com/easy-day-trips-from-venice-by-train/',
    'https://www.theblondeabroad.com/best-things-to-do-on-the-amalfi-coast/'
]

scraper = WebScraper()
print(f'blog 0 = {blogs[0]}')
xx = scraper.scrape(url=blogs[0])

print(xx)



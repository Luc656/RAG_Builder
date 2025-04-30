from blog_scraper_simple import WebScraper
from blog_transformation_functions import split_text, transform

blogs = [
    'https://www.myitaliandiaries.com/my-favourite-things-to-do-in-livorno/',
    'https://www.myitaliandiaries.com/things-to-do-in-ferrara-europes-first-modern-city/',
    'https://www.myitaliandiaries.com/easy-day-trips-from-venice-by-train/',
    'https://www.theblondeabroad.com/best-things-to-do-on-the-amalfi-coast/'
]

scraper = WebScraper()
post_data = scraper.scrape(url=blogs[0])

print(f'post_data: {post_data}')

title = post_data['titles']
content = post_data['body']

content = ' '.join(content)

print(title)
print(content)

if content:
    chunks = split_text(content)
    embeddings = transform(chunks)

    print(embeddings)
else:
    print('no content')
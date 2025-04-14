import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

blogs = [
    'https://www.myitaliandiaries.com/my-favourite-things-to-do-in-livorno/',
    'https://www.myitaliandiaries.com/things-to-do-in-ferrara-europes-first-modern-city/',
    'https://www.myitaliandiaries.com/easy-day-trips-from-venice-by-train/',
    'https://www.theblondeabroad.com/best-things-to-do-on-the-amalfi-coast/'
]

class BlogScraper:

    def __init__(self, base_url, headers=None):

        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

    def get_page(self, url):

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"error fetching {url}:{e}")
            return None

    def extract_posts(self, soup, post_selector, title_selector, link_selector, content_selector=None):
        posts = []
        for post in soup.select(post_selector):
            title = post.select_one(title_selector)
            link = post.select_one(link_selector)

            post_data = {
                'title': title.get_text(strip=True) if title else "No Title",
                'link': urljoin(self.base_url, link['href']) if link else "No Link"
            }

            if content_selector:
                content = post.select_one(content_selector)
                post_data['content'] = content.get_text(strip=True) if content else "No Content"

            posts.append(post_data)
        return posts


    def scrape(self, post, title, link, content, url):

        url = url or self.base_url
        soup = self.get_page(url)

        if soup:
            return self.extract_posts(soup, posst, title, link, content, url)
        return []
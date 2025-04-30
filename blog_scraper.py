import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
        #posts = []
        print()
        print(1)
        for post in soup.select(post_selector):
            title = post.select_one(title_selector)
            print(f'title: {title}')
            link = post.select_one(link_selector)
            print(f'link: {link}')

            post_data = {
                'title': title.get_text(strip=True) if title else "No Title",
                'link': urljoin(self.base_url, link['href']) if link else "No Link"
            }

            print(post_data)

            if content_selector:
                content = post.select_one(content_selector)
                print(f'content: {content}')
                post_data['content'] = content.get_text(strip=True) if content else None

            #posts.append(post_data)
        return post_data


    def scrape(self, post, title, link, content, url):

        url = url or self.base_url
        print(f'url: {url}')
        soup = self.get_page(url)
        print(f'soup:{soup}')

        if soup:
            print('got soup')
            return self.extract_posts(soup, post, title, link, content)
        else:
            print('no soup')
            return []
import requests
from bs4 import BeautifulSoup
from newspaper import Article

class NewsScraper:

    headers = {"User-Agent": "Mozilla/5.0"}

    def __init__(self, url):

        self.url = url
        self.html = None
        self.soup = None

    def fetch_html(self):
        resp = requests.get(self.url, headers=self.headers)
        if resp.status_code == 200:
            self.html = response.text
            self.soup = BeautifulSoup(self.url, 'html.parser')
        else:
            raise Exception(f"Failed to fetch page: {self.url}")

    def extract_with_newspaper(self):
        article = Article(self.url)
        article.download()
        article.parse()

        return {
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "publish_date": article.publish_date,
            "url": self.url
        }

    def parse(self):
        title = self.soup.find('h1').get_text(strip=True) if self.soup.find('h1') else None
        paras = self.soup.find_all('p')
        text = '\n'.join(p.get_text(strip=True) for p in paras)
        return {"title": title, "text": text, "url": self.url}

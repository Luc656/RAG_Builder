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

import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, user_agent=None):

        self.session = requests.Session()
        if user_agent:
            self.session.headers.update({'User-Agent': user_agent})
        else:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })

    def scrape(self, url):

        try:
            response = self.session.get(url)
            response.raise_for_status() # only raised for bad codes

            soup = BeautifulSoup(response.text, 'html.parser')

            titles = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]

            body = [p.get_text(strip=True) for p in soup.find_all('p')]

            return {
                'titles': titles,
                'body': body,
                'url': url
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the webpage: {e}")
            return {'titles': [], 'body': [], 'url': []}
        except Exception as e:
            print(f"Error during scraping: {e}")
            return {'titles': [], 'body': [], 'url': []}

import requests
from bs4 import BeautifulSoup
import time

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

        print('sleeping 3 secs')
        time.sleep(3)

        try:
            response = self.session.get(url)
            response.raise_for_status() # only raised for bad codes

            soup = BeautifulSoup(response.text, 'html.parser')

            titles = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]

            body = [p.get_text(strip=True) for p in soup.find_all('p')
                    if not p.find_parent('div', id='global-cookie-message')]

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

    def scrape_uk_gov(self, url):

        print('sleeping 3 secs')
        time.sleep(3)

        try:
            response = self.session.get(url)
            response.raise_for_status() # only raised for bad codes

            soup = BeautifulSoup(response.text, 'html.parser')

            title_element = soup.find('h1', class_='gem-c-heading__text govuk-heading-xl')
            titles = title_element.get_text(strip=True) if title_element else "No title found"
            #titles = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]

            # body = [p.get_text(strip=True) for p in soup.find_all('p')
            #         if not p.find_parent('div', id='global-cookie-message')]

            main_element = soup.find('main', {'role': 'main', 'id': 'content'})
            main_text = ""

            if main_element:
                # Get all text from main element, preserving some structure
                main_text = main_element.get_text(separator='\n', strip=True)
            else:
                main_text = "Main content not found"

            return {
                'titles': titles,
                'body': main_text,
                'url': url
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the webpage: {e}")
            return {'titles': [], 'body': [], 'url': []}
        except Exception as e:
            print(f"Error during scraping: {e}")
            return {'titles': [], 'body': [], 'url': []}

    def scrape_uk_gov2(self, url):

        response = self.session.get(url)
        response.raise_for_status()  # only raised for bad codes

        soup = BeautifulSoup(response.text, 'html.parser')
        main_element = soup.find('main', {'role': 'main', 'id': 'content'})

        sections = []
        curr_section = None

        for tag in main_element.children:
            print(tag.name)
            if tag.name == 'h3':
                if curr_section:
                    sections.append(curr_section)
                curr_section = {
                    'header': tag,
                    'content': []
                }
            elif curr_section and tag.name:
                curr_section['content'].append(tag)

        if curr_section:
            sections.append(curr_section)

        for section in sections:
            print(f"Header: {section['header'].text}")
            print("Content:")
            for elem in section['content']:
                print(f" - {elem}")
            print("----")


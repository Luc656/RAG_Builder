import requests
import sqlite3
import time
import os
import json

urls = []

API_KEY = os.getenv("NEWS_API_KEY")
site = "https://newsapi.org/v2/everything"

params = {
    'q' : 'geopolitics OR international affairs OR diplomacy OR war OR global economy',
    'apiKey' : API_KEY,
    'language' : 'en',
    'sources' : "bbc-news, al-jazeera-english, the-guardian-uk, reuters"
}

resp = requests.get(site,params=params)

print(resp.status_code)

print(resp.json()['totalResults'])
print(resp.json()['articles'])

print()

articles = resp.json()['articles']

for i in articles:

    print(i['url'])
    urls.append(i['url'])

print(urls)
print(len(urls))

# with open('test.txt', 'w') as f1:
#
#     json.dump(resp.json()['articles'], f1, indent=4)




print(API_KEY)


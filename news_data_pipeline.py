import requests
import sqlite3
import time
import os
import json

API_KEY = os.getenv("NEWS_DATA_API_KEY")
print(API_KEY)
site = "https://newsdata.io/api/1/latest"

params = {
    'q' : 'geopolitics OR international affairs OR diplomacy OR war OR global economy',
    'apiKey' : API_KEY,
    'language' : 'en',
    #'full_content' : '1'
    #'sources' : "bbc-news, al-jazeera-english, the-guardian-uk, reuters"
}

resp = requests.get(site,params=params)

print(resp.status_code)

print(resp.json())

print(resp.json()['totalResults'])
print(resp.json()['results'])

print()

with open('test_news_data.txt', 'w') as f1:

    json.dump(resp.json()['results'], f1, indent=4)




print(API_KEY)


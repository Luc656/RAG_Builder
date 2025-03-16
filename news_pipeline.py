import requests
import sqlite3
import time
import os
import json

def get_urls(api_key, site, params):

    urls = []

    resp = requests.get(site,params=params)
    print(resp.status_code)

    articles = resp.json()['articles']

    for i in articles:
        print(i['url'])
        urls.append(i['url'])

    print(urls)
    print(len(urls))

    return urls

# print(resp.json()['totalResults'])
# print(resp.json()['articles'])








# with open('test.txt', 'w') as f1:
#
#     json.dump(resp.json()['articles'], f1, indent=4)



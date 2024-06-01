#!/bin/env python
import requests
import dotenv
import os

dotenv.load_dotenv(dotenv_path='/home/jw/src/crewai/news/.env')

# Replace 'your_api_key_here' with your actual API key from Serper
API_KEY = os.environ['SERPER_API_KEY']
SEARCH_URL = 'https://api.serper.dev/search'

def search_serper(query):
    headers = {
        'X-API-KEY': API_KEY,
        'Content-Type': 'application/json',
    }
    payload = {
        'q': query,
        'num': 10  # Number of search results to return
    }

    response = requests.post(SEARCH_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example search query
query = 'high-protein recipes for irritable bowel syndrome'
results = search_serper(query)

# Print the results
for idx, result in enumerate(results.get('results', []), start=1):
    print(f"{idx}. {result.get('title')}\n{result.get('link')}\n")


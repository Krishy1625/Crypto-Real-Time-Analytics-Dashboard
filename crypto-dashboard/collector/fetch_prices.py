# fetch_prices.py
# Fetch price API :  CoinGecko
# https://www.youtube.com/watch?v=-GfeGQxdwG4

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COINGECKO_API_KEY")

url = "https://api.coingecko.com/api/v3/simple/price"

headers = {
    "x-cg-demo-api-key": API_KEY
}

params = {
    "ids": "bitcoin,ethereum",
    "vs_currencies": "gbp"
}

def fetch_prices():
    response = requests.get(url, headers=headers, params=params)
    return response.json()

#  print(fetch_prices())

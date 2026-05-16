# fetch_and_store.py
import requests
from database import init_db, insert_price
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Initialise DB once
init_db()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY") or os.getenv("coingecko_api_key") or ""


def fetch_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"

    headers = {}
    if COINGECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

    params = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "gbp"
    }

    response = requests.get(url, params=params, headers=headers)
    return response.json()


print("Starting price fetcher...")
while True:
    try:
        data = fetch_prices()

        insert_price("bitcoin", data["bitcoin"]["gbp"])
        insert_price("ethereum", data["ethereum"]["gbp"])
        insert_price("solana", data["solana"]["gbp"])

        print("Inserted new batch")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(30)

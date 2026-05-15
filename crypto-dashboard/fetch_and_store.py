# fetch_and_store.py
import requests
from database import init_db, insert_price
import time

# initialise DB once
init_db()

def fetch_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "gbp"
    }

    response = requests.get(url, params=params)
    return response.json()

while True:
    data = fetch_prices()

    insert_price("bitcoin", data["bitcoin"]["gbp"])
    insert_price("ethereum", data["ethereum"]["gbp"])
    insert_price("solana", data["solana"]["gbp"])

    print("Inserted new batch")

    time.sleep(30)
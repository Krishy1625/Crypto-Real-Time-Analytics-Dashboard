# analytics.py
import sqlite3
import pandas as pd

def load_data():
    conn = sqlite3.connect("crypto.db")
    df = pd.read_sql_query("SELECT * FROM prices", conn)
    conn.close()
    return df

def get_coin_data(df, coin):
    return df[df["coin"] == coin]


def moving_average(df, window=5):
    df = df.copy()
    df["moving_avg"] = df["price"].rolling(window).mean()
    return df

def stats(df):
    return {
        "mean": df["price"].mean(),
        "max": df["price"].max(),
        "min": df["price"].min(),
        "volatility": df["price"].std()
    }
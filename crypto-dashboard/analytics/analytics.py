# analytics.py
import sqlite3
import pandas as pd

def load_data():
    conn = sqlite3.connect("crypto.db")
    df = pd.read_sql("SELECT * FROM prices", conn)
    conn.close()
    return df

def get_coin(df, coin):
    return df[df["coin"] == coin]

def add_moving_average(df):
    df = df.copy()
    df["ma_10"] = df["price"].rolling(10).mean()
    return df

def volatility(df):
    return df["price"].std()
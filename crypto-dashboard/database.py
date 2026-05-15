#database.py
import sqlite3

def init_db():
    conn = sqlite3.connect("crypto.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin TEXT,
        price REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_price(coin, price):
    conn = sqlite3.connect("crypto.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prices (coin, price)
        VALUES (?, ?)
    """, (coin, price))

    conn.commit()
    conn.close()
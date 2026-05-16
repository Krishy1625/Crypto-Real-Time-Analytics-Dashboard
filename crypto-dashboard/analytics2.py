# analytics2.py
import pandas as pd
from database import get_connection
from dotenv import load_dotenv

load_dotenv()


def load_data():
    """Load all price records from PostgreSQL."""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM prices ORDER BY timestamp", conn)
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def get_coin(df, coin):
    """Filter dataframe for a specific coin."""
    return df[df["coin"] == coin].copy()


def add_moving_average(df, window=10):
    """Add a rolling moving average column."""
    df = df.copy()
    df["ma_10"] = df["price"].rolling(window).mean()
    return df


def volatility(df):
    """Return standard deviation of prices."""
    return df["price"].std()


def compute_rsi(df, period=14):
    """
    Compute RSI (Relative Strength Index) for the price series.
    RSI > 70 = overbought, RSI < 30 = oversold.
    """
    df = df.copy()
    delta = df["price"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))
    return df


def build_ohlc(df, freq="5min"):
    """
    Resample price data into OHLC (Open, High, Low, Close) format
    for candlestick charts.
    freq: pandas resample frequency e.g. '5min', '1h', '1D'
    """
    df = df.set_index("timestamp")
    ohlc = df["price"].resample(freq).ohlc().dropna()
    ohlc = ohlc.reset_index()
    return ohlc

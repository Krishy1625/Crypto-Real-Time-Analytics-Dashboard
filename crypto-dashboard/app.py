# app.py
# https://docs.streamlit.io/develop/api-reference

import streamlit as st
from analytics import load_data, get_coin, add_moving_average
import plotly.express as px

st.title("Crypto Batch Processed Dashboard")
st.text("Using CoinGecko API")

df = load_data()

coin = st.selectbox("Choose coin", df["coin"].unique())
coin_df = get_coin(df, coin)
coin_df = add_moving_average(coin_df)

st.metric("Latest Price", coin_df["price"].iloc[-1])
st.metric("Max Price", coin_df["price"].max())
st.metric("Min Price", coin_df["price"].min())

fig = px.line(coin_df, x="timestamp", y="price", title=f"{coin} Price Over Time")

st.plotly_chart(fig)
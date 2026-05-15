# app.py
import streamlit as st
import plotly.express as px
import time

from analytics import load_data, get_coin_data, moving_average, stats

st.title("Crypto Real-Time Analytics Dashboard")
st.autorefresh(interval=5000)

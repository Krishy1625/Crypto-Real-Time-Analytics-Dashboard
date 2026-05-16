import streamlit as st
from analytics2 import load_data, get_coin, add_moving_average, compute_rsi
from ui import configure_page, render_header, render_refresh_section, render_metrics, render_export_button, render_no_data_warning
from sidebar import render_sidebar
from alerts import render_alerts
from charts import render_tabs

configure_page()
render_header()
render_refresh_section()

df = load_data()
if df.empty:
    render_no_data_warning()

coin, interval, alert_enabled, alert_above, alert_below = render_sidebar(df)

coin_df = get_coin(df, coin)
coin_df = add_moving_average(coin_df)
coin_df = compute_rsi(coin_df)

latest_price = coin_df["price"].iloc[-1]
max_price = coin_df["price"].max()
min_price = coin_df["price"].min()
prev_price = coin_df["price"].iloc[-2] if len(coin_df) > 1 else latest_price
price_change = latest_price - prev_price

render_alerts(alert_enabled, alert_above, alert_below, coin, latest_price)
render_metrics(
    latest_price,
    price_change,
    max_price,
    min_price,
    coin_df["rsi"].dropna().iloc[-1] if not coin_df["rsi"].dropna().empty else None
)

st.markdown("---")
render_tabs(coin_df, coin, interval, alert_enabled, alert_above, alert_below)

st.markdown("---")
render_export_button(coin_df, coin)

import streamlit as st


def render_sidebar(df):
    st.sidebar.header("⚙️ Settings")

    coin = st.sidebar.selectbox("🪙 Select Coin", df["coin"].unique())
    interval = st.sidebar.selectbox(
        "⏱️ Candlestick Interval",
        ["1min", "5min", "15min", "30min", "1h"],
        index=1
    )

    st.sidebar.markdown("---")
    st.sidebar.header("🔔 Price Alerts")

    alert_enabled = st.sidebar.toggle("Enable Alerts", value=False)
    alert_above = st.sidebar.number_input(
        "Alert if price ABOVE (£)",
        min_value=0.0,
        value=0.0,
        step=100.0
    )
    alert_below = st.sidebar.number_input(
        "Alert if price BELOW (£)",
        min_value=0.0,
        value=0.0,
        step=100.0
    )

    return coin, interval, alert_enabled, alert_above, alert_below

# app.py
# Crypto Real-Time Analytics Dashboard
# Features: Candlestick Charts, RSI Indicator, Price Alerts

import datetime
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from analytics.analytics2 import load_data, get_coin, add_moving_average, compute_rsi, build_ohlc

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Crypto Analytics Dashboard",
    layout="wide",
    page_icon="📈"
)

st.title("📈 Crypto Analytics Dashboard")
st.caption("Powered by CoinGecko API · Live prices in GBP")

# ── Refresh ───────────────────────────────────────────────────────────────────
col_refresh, col_time = st.columns([1, 4])
with col_refresh:
    if st.button(" Refresh"):
        st.rerun()
with col_time:
    st.write(f"Last updated: **{datetime.datetime.now().strftime('%H:%M:%S')}**")

# ── Load data ─────────────────────────────────────────────────────────────────
df = load_data()

if df.empty:
    st.warning(" No price data yet. Start `fetch_and_store.py` and refresh.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Settings")

# Coin selector
coin = st.sidebar.selectbox("🪙 Select Coin", df["coin"].unique())

# Candlestick interval
interval = st.sidebar.selectbox(
    "⏱️ Candlestick Interval",
    ["1min", "5min", "15min", "30min", "1h"],
    index=1
)

# ── Price Alerts ──────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.header("🔔 Price Alerts")

alert_enabled = st.sidebar.toggle("Enable Alerts", value=False)
alert_above = st.sidebar.number_input("Alert if price ABOVE (£)", min_value=0.0, value=0.0, step=100.0)
alert_below = st.sidebar.number_input("Alert if price BELOW (£)", min_value=0.0, value=0.0, step=100.0)

# ── Filter coin data ──────────────────────────────────────────────────────────
coin_df = get_coin(df, coin)
coin_df = add_moving_average(coin_df)
coin_df = compute_rsi(coin_df)

latest_price = coin_df["price"].iloc[-1]
max_price    = coin_df["price"].max()
min_price    = coin_df["price"].min()
prev_price   = coin_df["price"].iloc[-2] if len(coin_df) > 1 else latest_price
price_change = latest_price - prev_price

# ── Price Alert Notifications ─────────────────────────────────────────────────
if alert_enabled:
    if alert_above > 0 and latest_price > alert_above:
        st.error(f"🚨 ALERT: {coin.capitalize()} is ABOVE £{alert_above:,.2f} — Current: £{latest_price:,.2f}")
    if alert_below > 0 and latest_price < alert_below:
        st.warning(f"⚠️ ALERT: {coin.capitalize()} is BELOW £{alert_below:,.2f} — Current: £{latest_price:,.2f}")

# ── Metrics row ───────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 Latest Price",  f"£{latest_price:,.2f}", f"£{price_change:+,.2f}")
m2.metric("📈 All-Time High", f"£{max_price:,.2f}")
m3.metric("📉 All-Time Low",  f"£{min_price:,.2f}")

# RSI badge
latest_rsi = coin_df["rsi"].dropna().iloc[-1] if not coin_df["rsi"].dropna().empty else None
if latest_rsi is not None:
    if latest_rsi > 70:
        rsi_label = f"{latest_rsi:.1f} 🔴 Overbought"
    elif latest_rsi < 30:
        rsi_label = f"{latest_rsi:.1f} 🟢 Oversold"
    else:
        rsi_label = f"{latest_rsi:.1f} 🟡 Neutral"
    m4.metric("📊 RSI (14)", rsi_label)

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🕯️ Candlestick + RSI", "📉 Line Chart"])

# ── TAB 1: Candlestick + RSI ──────────────────────────────────────────────────
with tab1:
    ohlc = build_ohlc(coin_df, freq=interval)

    if ohlc.empty or len(ohlc) < 2:
        st.info(f"⏳ Not enough data for {interval} candles yet. Keep the fetcher running and check back soon!")
    else:
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.7, 0.3],
            vertical_spacing=0.05,
            subplot_titles=(f"{coin.capitalize()} Candlestick ({interval})", "RSI (14)")
        )

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=ohlc["timestamp"],
            open=ohlc["open"],
            high=ohlc["high"],
            low=ohlc["low"],
            close=ohlc["close"],
            name="Price",
            increasing_line_color="#26a69a",
            decreasing_line_color="#ef5350"
        ), row=1, col=1)

        # RSI line
        rsi_data = coin_df.dropna(subset=["rsi"])
        fig.add_trace(go.Scatter(
            x=rsi_data["timestamp"],
            y=rsi_data["rsi"],
            name="RSI",
            line=dict(color="#7c83f5", width=1.5)
        ), row=2, col=1)

        # RSI overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red",   annotation_text="Overbought (70)", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)",   row=2, col=1)

        fig.update_layout(
            height=600,
            xaxis_rangeslider_visible=False,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        fig.update_yaxes(title_text="Price (£)", row=1, col=1)
        fig.update_yaxes(title_text="RSI", row=2, col=1, range=[0, 100])

        st.plotly_chart(fig, use_container_width=True)

        # RSI explanation
        with st.expander("ℹ️ What is RSI?"):
            st.markdown("""
            **RSI (Relative Strength Index)** is a momentum indicator (0–100):
            - **Above 70** 🔴 — Coin may be **overbought** (price could drop soon)
            - **Below 30** 🟢 — Coin may be **oversold** (price could rise soon)
            - **30–70** 🟡 — **Neutral** zone
            """)

# ── TAB 2: Line Chart ─────────────────────────────────────────────────────────
with tab2:
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=coin_df["timestamp"],
        y=coin_df["price"],
        name="Price",
        line=dict(color="#7c83f5", width=2)
    ))

    fig2.add_trace(go.Scatter(
        x=coin_df["timestamp"],
        y=coin_df["ma_10"],
        name="10-period MA",
        line=dict(color="#f5a623", width=1.5, dash="dash")
    ))

    # Alert lines on chart
    if alert_enabled and alert_above > 0:
        fig2.add_hline(y=alert_above, line_dash="dot", line_color="red",
                       annotation_text=f"Alert Above £{alert_above:,.0f}")
    if alert_enabled and alert_below > 0:
        fig2.add_hline(y=alert_below, line_dash="dot", line_color="orange",
                       annotation_text=f"Alert Below £{alert_below:,.0f}")

    fig2.update_layout(
        title=f"{coin.capitalize()} Price Over Time",
        xaxis_title="Time",
        yaxis_title="Price (£)",
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )

    st.plotly_chart(fig2, use_container_width=True)

# ── Export ────────────────────────────────────────────────────────────────────
st.markdown("---")
csv = coin_df[["timestamp", "coin", "price"]].to_csv(index=False)
st.download_button(
    label="📥 Download Price Data as CSV",
    data=csv,
    file_name=f"{coin}_prices.csv",
    mime="text/csv"
)

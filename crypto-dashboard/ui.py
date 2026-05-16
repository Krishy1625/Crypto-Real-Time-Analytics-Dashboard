import datetime
import streamlit as st


def configure_page():
    st.set_page_config(
        page_title="Crypto Analytics Dashboard",
        layout="wide",
        page_icon="📈"
    )


def render_header():
    st.title("📈 Crypto Analytics Dashboard")
    st.caption("Powered by CoinGecko API · Live prices in GBP")


def render_refresh_section():
    col_refresh, col_time = st.columns([1, 4])
    with col_refresh:
        if st.button(" Refresh"):
            st.rerun()
    with col_time:
        st.write(f"Last updated: **{datetime.datetime.now().strftime('%H:%M:%S')}**")


def render_no_data_warning():
    st.warning(" No price data yet. Start `fetch_and_store.py` and refresh.")
    st.stop()


def render_metrics(latest_price, price_change, max_price, min_price, latest_rsi):
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("💰 Latest Price",  f"£{latest_price:,.2f}", f"£{price_change:+,.2f}")
    m2.metric("📈 All-Time High", f"£{max_price:,.2f}")
    m3.metric("📉 All-Time Low",  f"£{min_price:,.2f}")

    if latest_rsi is not None:
        if latest_rsi > 70:
            rsi_label = f"{latest_rsi:.1f} 🔴 Overbought"
        elif latest_rsi < 30:
            rsi_label = f"{latest_rsi:.1f} 🟢 Oversold"
        else:
            rsi_label = f"{latest_rsi:.1f} 🟡 Neutral"
        m4.metric("📊 RSI (14)", rsi_label)


def render_export_button(coin_df, coin):
    csv = coin_df[["timestamp", "coin", "price"]].to_csv(index=False)
    st.download_button(
        label="📥 Download Price Data as CSV",
        data=csv,
        file_name=f"{coin}_prices.csv",
        mime="text/csv"
    )

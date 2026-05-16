import streamlit as st


def render_alerts(alert_enabled, alert_above, alert_below, coin, latest_price):
    if not alert_enabled:
        return

    if alert_above > 0 and latest_price > alert_above:
        st.error(
            f"🚨 ALERT: {coin.capitalize()} is ABOVE £{alert_above:,.2f} — Current: £{latest_price:,.2f}"
        )
    if alert_below > 0 and latest_price < alert_below:
        st.warning(
            f"⚠️ ALERT: {coin.capitalize()} is BELOW £{alert_below:,.2f} — Current: £{latest_price:,.2f}"
        )

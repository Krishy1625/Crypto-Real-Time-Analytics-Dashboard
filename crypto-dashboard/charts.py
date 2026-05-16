import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from analytics2 import build_ohlc


def render_tabs(coin_df, coin, interval, alert_enabled, alert_above, alert_below):
    tab1, tab2 = st.tabs(["🕯️ Candlestick + RSI", "📉 Line Chart"])

    with tab1:
        ohlc = build_ohlc(coin_df, freq=interval)

        if ohlc.empty or len(ohlc) < 2:
            st.info(
                f"⏳ Not enough data for {interval} candles yet. Keep the fetcher running and check back soon!"
            )
        else:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                row_heights=[0.7, 0.3],
                vertical_spacing=0.05,
                subplot_titles=(f"{coin.capitalize()} Candlestick ({interval})", "RSI (14)")
            )

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

            rsi_data = coin_df.dropna(subset=["rsi"])
            fig.add_trace(go.Scatter(
                x=rsi_data["timestamp"],
                y=rsi_data["rsi"],
                name="RSI",
                line=dict(color="#7c83f5", width=1.5)
            ), row=2, col=1)

            fig.add_hline(y=70, line_dash="dash", line_color="red",
                          annotation_text="Overbought (70)", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green",
                          annotation_text="Oversold (30)", row=2, col=1)

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

            with st.expander("ℹ️ What is RSI?"):
                st.markdown(
                    """
                    **RSI (Relative Strength Index)** is a momentum indicator (0–100):
                    - **Above 70** 🔴 — Coin may be **overbought** (price could drop soon)
                    - **Below 30** 🟢 — Coin may be **oversold** (price could rise soon)
                    - **30–70** 🟡 — **Neutral** zone
                    """
                )

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

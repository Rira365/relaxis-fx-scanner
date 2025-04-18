import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta, timezone

# Set timezone to JST
jst = timezone(timedelta(hours=9))

# Title
st.title("Relaxis Future Forecast - BTC/USD")

# API key from Streamlit Secrets
API_KEY = st.secrets["API_KEY"]
SYMBOL = "BTC/USD"
INTERVAL = "1min"
URL = f"https://api.twelvedata.com/time_series?symbol={SYMBOL}&interval={INTERVAL}&outputsize=60&apikey={API_KEY}"

# Fetch data
@st.cache_data(ttl=60)
def get_data():
    response = requests.get(URL)
    data = response.json()
    if "values" in data:
        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")
        df = df.set_index("datetime")
        df = df.astype(float)
        return df
    return None

df = get_data()

if df is not None:
    # Simulate future prediction
    last_price = df["close"].iloc[-1]
    prediction_trend = np.random.choice(["Up", "Down"])
    confidence = np.random.randint(70, 95)
    trend_sign = 1 if prediction_trend == "Up" else -1
    future_times = [df.index[-1] + timedelta(minutes=i) for i in range(1, 11)]
    future_prices = [last_price + trend_sign * i * 5 for i in range(1, 11)]

    # Display prediction
    st.markdown(f"### Forecast: **{prediction_trend}** (Confidence: {confidence}%)")
    st.markdown(f"### Current BTC/USD: **${last_price:,.2f}**")

    # Create candlestick chart
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Price"
    ))

    fig.add_trace(go.Scatter(
        x=future_times,
        y=future_prices,
        mode="lines",
        name=f"Forecast ({confidence}%)",
        line=dict(dash="dash", color="orange")
    ))

    # Current price marker
    fig.add_trace(go.Scatter(
        x=[df.index[-1]],
        y=[last_price],
        mode="text",
        text=[f"${last_price:,.2f}"],
        textposition="bottom right",
        textfont=dict(color="blue", size=14),
        showlegend=False
    ))

    # Layout
    fig.update_layout(
        xaxis_title="Time (JST)",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
        margin=dict(l=20, r=20, t=40, b=20),
        height=600
    )

    fig.update_xaxes(tickformat="%H:%M", tickangle=-30, tickfont=dict(size=10))

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Failed to retrieve data. Please check your API key or network connection.")

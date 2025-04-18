import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# タイトル
st.title("BTC/USD リアルタイムチャート - 未来予測準備版")

# CoinGeckoのAPIで過去1日（24時間）の価格データ取得
@st.cache_data
def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "interval": "minutely"
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        prices = res.json()["prices"]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        return df
    else:
        st.error("データ取得に失敗しました")
        return None

# データ取得
df = get_btc_data()

# 表示
if df is not None:
    current_price = df["price"].iloc[-1]
    st.metric(label="現在のBTC/USD", value=f"${current_price:,.2f}")

    # チャート
    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["price"], label="BTC/USD")
    ax.set_xlabel("時間")
    ax.set_ylabel("価格（USD）")
    ax.set_title("過去24時間のBTC/USD")
    plt.xticks(rotation=45)
    st.pyplot(fig)

from io import StringIO
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# タイトル
st.title("Relaxis Future Forecast - BTC/USDリアルタイムチャート")

# Twelve Data APIキー
API_KEY = "2ac3e17a9afc4542863605905fadfc7d"
symbol = "BTC/USD"
interval = "1min"

# データ取得関数
def get_btc_data():
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize=30&format=JSON"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "values" in data:
            df = pd.DataFrame(data["values"])
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.sort_values("datetime")
            df = df.rename(columns={"close": "Close"})
            return df
        else:
            st.error("データがありません。APIの使用制限に達していないか確認してください。")
    else:
        st.error("データ取得に失敗しました。")
    return None

# データ取得＆表示
df = get_btc_data()

if df is not None:
    st.line_chart(df.set_index("datetime")["Close"], use_container_width=True)
    current_price = df["Close"].iloc[-1]
    st.metric(label="現在のBTC/USD", value=f"{current_price} USD")

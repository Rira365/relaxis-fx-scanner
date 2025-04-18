from io import StringIO
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Relaxis FX Scanner - USD/JPYリアルタイム価格")

API_KEY = "7RNGQ9UBYSWC32P2"

def get_fx_data():
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=JPY&interval=1min&apikey={API_KEY}&outputsize=compact"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        if "Time Series FX (1min)" in data:
            df = pd.DataFrame.from_dict(data["Time Series FX (1min)"], orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.rename(columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close"
            })
            df = df.sort_index()
            return df
        else:
            st.error("❌ データが見つかりません（無料枠制限の可能性あり）")
            st.write("レスポンス内容：", data)
            return None
    else:
        st.error("❌ API通信エラー")
        return None

df = get_fx_data()

if df is not None:
    st.line_chart(df["close"], use_container_width=True)
    current_price = float(df["close"].iloc[-1])
    st.metric(label="現在のUSD/JPY", value=f"{current_price:.2f}")

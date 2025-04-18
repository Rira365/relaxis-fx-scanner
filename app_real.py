import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# タイトル
st.title("Relaxis FX Scanner - USD/JPYリアルタイム価格")

# Alpha Vantage APIキー（ユーザーのキー）
API_KEY = "7RNGQ9UBYSWC32P2"
symbol = "USD/JPY"

# データ取得関数
def get_fx_data():
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=JPY&interval=1min&apikey={API_KEY}&datatype=csv"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(pd.compat.StringIO(response.text))
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        return df
    else:
        return None

# データ取得
df = get_fx_data()

if df is not None:
    st.line_chart(df.set_index('timestamp')['close'], use_container_width=True)
    current_price = df['close'].iloc[-1]
    st.metric(label="現在のUSD/JPY", value=f"{current_price:.2f}")
else:
    st.error("データ取得に失敗しました。ネットワーク環境をご確認ください。")

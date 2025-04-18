from io import StringIO
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Relaxis FX Scanner - USD/JPYリアルタイム価格")

API_KEY = "7RNGQ9UBYSWC32P2"

def get_fx_data():
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=JPY&interval=1min&apikey={API_KEY}&datatype=csv"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text))
        st.write("📊 データプレビュー", df.head())  # ← デバッグ用
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            return df
        else:
            st.error("❌ 'timestamp' カラムが存在しません。フォーマットを確認してください。")
            return None
    else:
        st.error("❌ データ取得に失敗しました。")
        return None

df = get_fx_data()

if df is not None:
    st.line_chart(df.set_index('timestamp')['close'], use_container_width=True)
    current_price = df['close'].iloc[-1]
    st.metric(label="現在のUSD/JPY", value=f"{current_price:.2f}")

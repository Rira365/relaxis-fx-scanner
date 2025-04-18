
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# ページ設定
st.set_page_config(page_title="Relaxis FX Scanner - Real", layout="wide")
st.title("Relaxis FX Scanner - USD/JPYリアルタイム価格")

# 日本時間取得用
JST = datetime.timezone(datetime.timedelta(hours=9))
now_jst = datetime.datetime.now(JST)

# ヒストリカルデータ取得
symbol = "JPY=X"  # Yahoo FinanceでのUSD/JPY
data = yf.download(symbol, interval="1m", period="60m")  # 過去60分の1分足

# 現在価格を取得（最新の終値）
current_price = round(data["Close"][-1], 3) if not data.empty else None

if current_price:
    st.subheader(f"現在のUSD/JPY価格: {current_price} 円（{now_jst.strftime('%Y-%m-%d %H:%M:%S')} JST）")

    # グラフ描画
    fig, ax = plt.subplots()
    ax.plot(data.index, data["Close"], label="リアルタイム価格", color="blue")
    ax.scatter(data.index[-1], current_price, color="red", label=f"現在値: {current_price}")
    ax.set_xlabel("時刻")
    ax.set_ylabel("USD/JPY")
    ax.set_title("USD/JPY リアルタイムチャート（過去60分・1分足）")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.error("データ取得に失敗しました。ネットワーク環境をご確認ください。")

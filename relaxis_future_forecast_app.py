from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import requests
import datetime
import plotly.graph_objects as go
import os

# タイトル
st.title("Relaxis Future Forecast - BTC/USD")
# 自動リロード（60秒ごと）
st_autorefresh(interval=60 * 1000, key="data_refresh")

# シークレットからAPIキーを取得
API_KEY = st.secrets["API_KEY"]

# データ取得関数（1分足）
@st.cache_data(ttl=60)
def get_btc_data():
    url = f"https://api.twelvedata.com/time_series?symbol=BTC/USD&interval=1min&outputsize=50&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["datetime"] = df["datetime"].dt.tz_localize("UTC").dt.tz_convert("Asia/Tokyo")
    df = df.sort_values("datetime")
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
    return df

# 未来予測（仮の予測ロジック）
def predict_future(df):
    last_price = df["close"].iloc[-1]
    future_times = [df["datetime"].iloc[-1] + datetime.timedelta(minutes=i) for i in range(1, 6)]
    future_prices = [last_price + i * 30 for i in range(1, 6)]
    future_df = pd.DataFrame({"datetime": future_times, "predicted": future_prices})
    return future_df, "上昇", 86  # 上昇/下降, 確率(%)

# データ取得
df = get_btc_data()
future_df, direction, confidence = predict_future(df)

# 現在価格
current_price = df["close"].iloc[-1]
st.markdown(f"### 未来予測：**{direction}**（確率{confidence}%）")
st.metric(label="現在のBTC/USD", value=f"${current_price:,.2f}")

# ローソク足チャート描画
fig = go.Figure()

# 実データ（ローソク足）
fig.add_trace(go.Candlestick(
    x=df["datetime"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="実データ"
))

# 現在価格ラベル
fig.add_trace(go.Scatter(
    x=[df["datetime"].iloc[-1]],
    y=[current_price],
    mode="text",
    text=[f"${current_price:.2f}"],
    textposition="bottom right",
    name="現在価格",
    textfont=dict(color="blue", size=12)
))

# 未来予測ライン
fig.add_trace(go.Scatter(
    x=future_df["datetime"],
    y=future_df["predicted"],
    mode="lines",
    name=f"未来予測（{direction}, 確率{confidence}%）",
    line=dict(dash="dash", color="orange")
))

# レイアウト
fig.update_layout(
    xaxis_title="日時（日本時間）",
    yaxis_title="価格（USD）",
    legend_title="凡例",
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import requests
import datetime
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta
from ta.trend import MACD
from ta.momentum import RSIIndicator

# タイトルと画面設定
st.set_page_config(layout="wide")
st.title("Relaxis Future Forecast - BTC/USD")
# ⏱ 自動更新：60秒ごとにページをリロード
st_autorefresh(interval=60 * 1000, key="data_refresh")

# タイムゾーン切替（東京／NY）
timezone = st.radio("表示する時間帯を選択:", ("Tokyo (JST)", "New York (EST)"))

# APIキー（Secretsで管理）
API_KEY = st.secrets["API_KEY"]

# データ取得
@st.cache_data(ttl=60)
def get_data():
    url = f"https://api.twelvedata.com/time_series?symbol=BTC/USD&interval=1min&outputsize=100&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime")
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
    if timezone == "Tokyo (JST)":
        df["datetime"] = df["datetime"].dt.tz_localize("UTC").dt.tz_convert("Asia/Tokyo")
    else:
        df["datetime"] = df["datetime"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")
    return df

df = get_data()

# --- テクニカル指標計算（表示せず予測にのみ利用） ---
df["sma"] = df["close"].rolling(window=5).mean()
macd = MACD(df["close"])
df["macd_diff"] = macd.macd_diff()
rsi = RSIIndicator(df["close"])
df["rsi"] = rsi.rsi()

# --- 予測ロジック ---
current_price = df["close"].iloc[-1]
sma_trend = df["sma"].iloc[-1] - df["sma"].iloc[-5]
macd_trend = df["macd_diff"].iloc[-1]
rsi_level = df["rsi"].iloc[-1]

# スコアリングで方向判断
score = 0
if sma_trend > 0: score += 1
if macd_trend > 0: score += 1
if rsi_level < 30: score -= 1
if rsi_level > 70: score += 1

direction = "上昇" if score >= 1 else "下降"
confidence = 85 + score * 3 if direction == "上昇" else 75 - score * 2

# --- 自動コメント生成 ---
reason = []
if sma_trend > 0:
    reason.append("短期移動平均が上昇中")
if macd_trend > 0:
    reason.append("MACDが強気傾向")
if rsi_level > 70:
    reason.append("RSIが過熱気味（買われすぎ）")
if rsi_level < 30:
    reason.append("RSIが売られすぎゾーン")
comment = "・" + "\n・".join(reason) if reason else "・特筆すべきシグナルはありません"

# --- 未来価格を予測（簡易版） ---
future_steps = 5
step_size = 25 if direction == "上昇" else -25
future_times = [df["datetime"].iloc[-1] + timedelta(minutes=i) for i in range(1, future_steps + 1)]
future_prices = [current_price + i * step_size for i in range(1, future_steps + 1)]

# --- 表示エリア ---
st.metric(label="現在のBTC/USD", value=f"${current_price:,.2f}")
st.markdown(f"### 未来予測：**{direction}**（信頼度 {confidence}%）")
st.markdown("#### 根拠：\n" + comment)

# --- チャート表示 ---
fig = go.Figure()

# 実データ（ローソク足）
fig.add_trace(go.Candlestick(
    x=df["datetime"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="価格",
))

# 未来予測ライン（点線・ラベル付き）
fig.add_trace(go.Scatter(
    x=future_times,
    y=future_prices,
    mode="lines+markers+text",
    name="未来予測",
    line=dict(dash="dot", color="orange"),
    text=[f"${p:,.0f}" for p in future_prices],
    textposition="top right",
))

# 現在価格ラベル
fig.add_trace(go.Scatter(
    x=[df["datetime"].iloc[-1]],
    y=[current_price],
    mode="text",
    text=[f"${current_price:.2f}"],
    textposition="bottom right",
    showlegend=False
))

fig.update_layout(
    xaxis_title="時間",
    yaxis_title="価格 (USD)",
    xaxis_rangeslider_visible=False,
    legend=dict(orientation="h"),
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

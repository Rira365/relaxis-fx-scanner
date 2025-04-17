
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

st.title("Relaxis FX Scanner - 1分足バージョン")

# 時間設定（過去30分、未来5分）
history_points = 30
forecast_points = 5
delta = datetime.timedelta(minutes=1)

# 現在時刻からタイムスタンプ生成
now = datetime.datetime.now()
timestamps = [now - delta * i for i in range(history_points-1, -1, -1)]

# ダミーの価格データ
np.random.seed(42)
prices = 130 + np.cumsum(np.random.randn(history_points) * 0.2)

# 未来予測データ（仮の傾向）
future_timestamps = [now + delta * (i+1) for i in range(forecast_points)]
future_prices = [prices[-1] + (i+1)*0.05 for i in range(forecast_points)]

# データ結合
history_df = pd.DataFrame({"Time": timestamps, "Price": prices})
future_df = pd.DataFrame({"Time": future_timestamps, "Price": future_prices})

# チャート描画
fig, ax = plt.subplots()
ax.plot(history_df["Time"], history_df["Price"], label="Past", color="skyblue")
ax.plot(future_df["Time"], future_df["Price"], label="Forecast", linestyle="--", color="orange")
ax.set_xlabel("Time")
ax.set_ylabel("USD/JPY")
ax.set_title("USD/JPY Forecast (1分足)")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

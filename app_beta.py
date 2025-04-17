
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# タイトル
st.title("Relaxis FX Scanner")

# ダミーの時間軸（過去20分）
now = datetime.datetime.now()
timestamps = [now - datetime.timedelta(minutes=i) for i in range(19, -1, -1)]

# ダミーの価格データ（USD/JPY的な値動き）
np.random.seed(42)
prices = 130 + np.cumsum(np.random.randn(20) * 0.2)

# 未来予測（5分先を予測：ここでは単純な傾向で伸ばす）
future_timestamps = [now + datetime.timedelta(minutes=i+1) for i in range(5)]
future_prices = [prices[-1] + (i+1)*0.05 for i in range(5)]

# データフレーム作成
history_df = pd.DataFrame({"Time": timestamps, "Price": prices})
future_df = pd.DataFrame({"Time": future_timestamps, "Price": future_prices})

# 結合
combined_df = pd.concat([history_df, future_df])

# チャート描画
fig, ax = plt.subplots()
ax.plot(history_df["Time"], history_df["Price"], label="Past", color="skyblue")
ax.plot(future_df["Time"], future_df["Price"], label="Forecast", linestyle="--", color="orange")
ax.set_xlabel("Time")
ax.set_ylabel("USD/JPY")
ax.set_title("USD/JPY Forecast (Demo)")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

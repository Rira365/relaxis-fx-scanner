
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import random

# 日本時間
jst = pytz.timezone("Asia/Tokyo")
now = datetime.now(pytz.utc).astimezone(jst)

# 擬似的な過去データ（30分）
timestamps = [now - timedelta(minutes=i) for i in reversed(range(30))]
prices = np.cumsum(np.random.randn(30)) * 50 + 30000  # BTC/USD

# 未来予測（15分）
future_steps = 15
future_timestamps = [now + timedelta(minutes=i) for i in range(1, future_steps + 1)]
direction = np.random.choice(["上昇", "下降"])
certainty = np.random.randint(70, 95)
trend = np.linspace(0.5, 3.0, future_steps) * (1 if direction == "上昇" else -1)
future_prices = prices[-1] + trend * 50

# データフレーム化
past_df = pd.DataFrame({'timestamp': timestamps, 'price': prices})
future_df = pd.DataFrame({'timestamp': future_timestamps, 'price': future_prices})

# タイトルと表示
st.title("Relaxis Future Forecast - BTC/USD")
st.write(f"未来予測：**{direction}（確率{certainty}%）**")

# 現在価格
current_price = prices[-1]
st.metric(label="現在のBTC/USD", value=f"${current_price:,.2f}")

# チャート描画
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.plot(past_df['timestamp'], past_df['price'], label='過去の価格', linewidth=2)
plt.plot(future_df['timestamp'], future_df['price'], label=f'未来予測（{direction}, 確率{certainty}%）',
         linestyle='--', linewidth=2, color='orange')
plt.axvline(x=now, color='gray', linestyle=':', label='現在')
plt.text(now, current_price, f"${current_price:,.2f}", verticalalignment='bottom', fontsize=9, color='blue')
plt.xlabel('時間（日本時間）')
plt.ylabel('価格（USD）')
plt.legend()
plt.xticks(rotation=30, fontsize=8)
plt.yticks(fontsize=9)
plt.grid(True)
st.pyplot(plt)

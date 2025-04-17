
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

st.set_page_config(page_title="Relaxis FX Scanner LIVE", layout="wide")
st.title("Relaxis FX Scanner - 🔁 リアルタイム更新バージョン（1分足）")

placeholder = st.empty()

while True:
    with placeholder.container():
        # 設定
        history_points = 30
        forecast_points = 5
        delta = datetime.timedelta(minutes=1)
        now = datetime.datetime.now()

        # 時系列データ
        timestamps = [now - delta * i for i in range(history_points-1, -1, -1)]
        np.random.seed(int(time.time()) % 10000)
        prices = 130 + np.cumsum(np.random.randn(history_points) * 0.2)

        # 予測データ
        future_timestamps = [now + delta * (i+1) for i in range(forecast_points)]
        future_prices = [prices[-1] + (i+1)*0.05 for i in range(forecast_points)]

        # DataFrame
        history_df = pd.DataFrame({"Time": timestamps, "Price": prices})
        future_df = pd.DataFrame({"Time": future_timestamps, "Price": future_prices})

        # グラフ描画
        fig, ax = plt.subplots()
        ax.plot(history_df["Time"], history_df["Price"], label="Past", color="skyblue")
        ax.plot(future_df["Time"], future_df["Price"], label="Forecast", linestyle="--", color="orange")
        ax.set_xlabel("Time")
        ax.set_ylabel("USD/JPY")
        ax.set_title("USD/JPY Forecast (Live - 1分足)")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.markdown(f"🕒 最終更新: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    time.sleep(60)

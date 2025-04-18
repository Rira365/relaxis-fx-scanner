@st.cache_data
def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "interval": "minutely"
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            prices = res.json()["prices"]
            df = pd.DataFrame(prices, columns=["timestamp", "price"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
            return df
        else:
            st.error(f"取得失敗：HTTP {res.status_code}")
            return None
    except Exception as e:
        st.error(f"エラー発生: {str(e)}")
        return None

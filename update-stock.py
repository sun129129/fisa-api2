# update_stock.py
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SYMBOL = "TSLA"
README_PATH = "README.md"

URL = (
    f"https://www.alphavantage.co/query"
    f"?function=TIME_SERIES_INTRADAY"
    f"&symbol={SYMBOL}"
    f"&interval=60min"
    f"&apikey={API_KEY}"
)

def get_stock_data():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get("Time Series (60min)")
        if not time_series:
            return "❌ 데이터를 가져오지 못했습니다."

        latest_time = sorted(time_series.keys())[-1]
        latest_data = time_series[latest_time]

        open_price = float(latest_data["1. open"])
        high = float(latest_data["2. high"])
        low = float(latest_data["3. low"])
        close = float(latest_data["4. close"])
        volume = int(float(latest_data["5. volume"]))

        return (
            f"{SYMBOL} 주식 정보 (최근 업데이트: {latest_time} UTC)\n"
            f"- 시가: ${open_price:.2f}\n"
            f"- 고가: ${high:.2f}\n"
            f"- 저가: ${low:.2f}\n"
            f"- 종가: ${close:.2f}\n"
            f"- 거래량: {volume:,}"
        )
    else:
        return "❌ API 요청 실패"

def update_readme():
    stock_info = get_stock_data()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
# TSLA (Tesla) Stock Tracker 📈

이 리포지토리는 Alpha Vantage API를 통해 테슬라(TSLA) 주식 데이터를 주기적으로 업데이트합니다.

## 📊 최근 주식 정보
> {stock_info}

⏳ 업데이트 시간: {now} (UTC)

---

자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()

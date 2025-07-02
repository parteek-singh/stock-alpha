import os
import requests_cache
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPHA_API_KEY")

# Setup requests cache (SQLite file, expires in 12 hours)
session = requests_cache.CachedSession("alpha_cache", expire_after=43200)

def fetch_ohlcv(symbol: str, interval: str = "5min") -> pd.DataFrame:
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "outputsize": "compact",
        "apikey": API_KEY,
    }
    r = session.get(url, params=params)
    print(f"[CACHE:OHLCV] {symbol} {interval} from_cache: {r.from_cache}")
    data = r.json()

    # Use the correct key for intraday
    key = f"Time Series ({interval})"
    if key not in data:
        raise Exception(f"AlphaVantage error: {data}")

    df = pd.DataFrame.from_dict(data[key], orient="index", dtype=float)
    df.rename(
        columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume",
        },
        inplace=True,
    )
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    return df


def fetch_indicator(symbol: str, indicator: str, time_period: int = 20) -> pd.Series:
    url = "https://www.alphavantage.co/query"
    params = {
        "function": indicator,
        "symbol": symbol,
        "interval": "daily",  # indicators only support 'daily' in free tier
        "time_period": time_period,
        "series_type": "close",
        "apikey": API_KEY,
    }
    r = session.get(url, params=params)
    print(f"[CACHE:{indicator}] {symbol} from_cache: {r.from_cache}")
    data = r.json()

    key_map = {
        "SMA": "Technical Analysis: SMA",
        "RSI": "Technical Analysis: RSI",
    }

    key = key_map.get(indicator)
    if key not in data:
        raise Exception(f"AlphaVantage indicator error: {data}")

    df = pd.DataFrame.from_dict(data[key], orient="index", dtype=float)
    df.columns = [indicator]
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    return df[indicator]

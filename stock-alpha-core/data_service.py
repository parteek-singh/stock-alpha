import os
import pandas as pd
import requests
import yfinance as yf
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# CSV cache directory
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

def load_from_csv(symbol: str, interval: str) -> pd.DataFrame:
    file_path = CACHE_DIR / f"{symbol}_{interval}.csv"
    if file_path.exists():
        df = pd.read_csv(file_path, parse_dates=["datetime"])
        df.set_index("datetime", inplace=True)  # ✅ Set as index after parsing
        print(f"📁 Loaded {symbol} from CSV cache")
        return df
    return None


def save_to_csv(symbol: str, interval: str, df: pd.DataFrame):
    df = df.copy()
    df["datetime"] = df.index  # ✅ Add this line
    df.to_csv(CACHE_DIR / f"{symbol}_{interval}.csv", index=False)

def fetch_from_finnhub_new(symbol: str, interval: str = "1d") -> pd.DataFrame:
    resolution_map = {
        "1min": "1",
        "5min": "5",
        "15min": "15",
        "30min": "30",
        "60min": "60",
        "1d": "D",
        "1wk": "W"
    }

    resolution = resolution_map.get(interval, "D")

    now = int(time.time())
    past = now - 60 * 60 * 24 * 90  # last 90 days

    url = f"https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "from": past,
        "to": now,
        "token": FINNHUB_API_KEY
    }

    res = requests.get(url, params=params).json()
    if res.get("s") != "ok":
        raise Exception(f"Finnhub error: {res}")

    df = pd.DataFrame({
        "time": [datetime.utcfromtimestamp(ts) for ts in res["t"]],
        "Open": res["o"],
        "High": res["h"],
        "Low": res["l"],
        "Close": res["c"],
        "Volume": res["v"]
    })
    df.rename(columns={"time": "datetime"}, inplace=True)
    return df

def fetch_from_finnhub(symbol: str) -> pd.DataFrame:
    print(f"📡 Fetching from Finnhub: {symbol}")
    url = f"https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": "D",
        "from": int((datetime.now() - pd.Timedelta(days=120)).timestamp()),
        "to": int(datetime.now().timestamp()),
        "token": FINNHUB_API_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()
    if data.get("s") != "ok":
        raise Exception("Finnhub failed")

    df = pd.DataFrame({
        "datetime": pd.to_datetime(data["t"], unit="s"),
        "Open": data["o"],
        "High": data["h"],
        "Low": data["l"],
        "Close": data["c"],
        "Volume": data["v"]
    }).set_index("datetime")
    return df

def fetch_from_yfinance_new(symbol: str, interval: str = "1d") -> pd.DataFrame:
    interval_map = {
        "1min": "1m",
        "5min": "5m",
        "15min": "15m",
        "1d": "1d",
        "1wk": "1wk"
    }
    yf_interval = interval_map.get(interval, "1d")

    data = yf.download(
        tickers=symbol,
        period="90d" if "min" in interval else "1y",
        interval=yf_interval,
        progress=False
    )

    if data.empty:
        raise Exception("No data returned from yfinance")

    data.reset_index(inplace=True)
    data.rename(columns={"Date": "datetime"}, inplace=True)
    return data[["datetime", "Open", "High", "Low", "Close", "Volume"]]

def fetch_from_yfinance(symbol: str) -> pd.DataFrame:
    print(f"🔁 Fallback: Fetching {symbol} from yFinance")
    df = yf.download(symbol, period="6mo", interval="1d", progress=False)
    df.rename(columns=str.title, inplace=True)
    return df

def fetch_ohlcv(symbol: str, interval: str = "1d") -> pd.DataFrame:
    # Try CSV cache first
    df = load_from_csv(symbol, interval)
    if df is not None and not df.empty:
        print("✅ Loaded from CSV cache")
    else:
        # Try Finnhub
        try:
            df = fetch_from_finnhub(symbol)
            print("📡 Loaded from Finnhub")
        except Exception as e:
            print(f"⚠️ Finnhub failed: {e}")
            # Fallback to yfinance
            try:
                df = fetch_from_yfinance(symbol)
                print("🪙 Fallback to yfinance")
            except Exception as e2:
                print(f"❌ yfinance failed: {e2}")
                return pd.DataFrame()

        # Save to CSV for future caching
        save_to_csv(symbol, interval, df)

    # ✅ Ensure datetime is a column (not just index)
    if df.index.name == "datetime" or isinstance(df.index, pd.DatetimeIndex):
        df = df.reset_index()

    # ✅ Rename column if needed
    if "Date" in df.columns:
        df.rename(columns={"Date": "datetime"}, inplace=True)
    elif "index" in df.columns:
        df.rename(columns={"index": "datetime"}, inplace=True)

    # ✅ Convert to proper datetime format
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
    else:
        raise KeyError("No 'datetime' column found in OHLCV data")

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


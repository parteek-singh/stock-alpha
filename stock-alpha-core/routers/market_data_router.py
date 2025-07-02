from fastapi import APIRouter
from services.data_service import fetch_ohlcv
# from utils.indicator_utils import compute_sma, compute_rsi
import pandas as pd

router = APIRouter()

@router.get("/api/ping")
def ping():
    return {"status": "ok"}

@router.get("/api/ohlcv")
def get_ohlcv(symbol: str = "AAPL", interval: str = "1d"):
    df = fetch_ohlcv(symbol, interval)  # your existing function
    if df.empty:
        return []

    df = df.reset_index()

    # ✅ Rename and format cleanly
    df.rename(columns={"datetime": "time"}, inplace=True)

    response = []
    for _, row in df.iterrows():
        try:
            response.append({
                "time": int(pd.to_datetime(row["time"]).timestamp()),  # UNIX seconds
                "Open": float(row["Open"]),
                "High": float(row["High"]),
                "Low": float(row["Low"]),
                "Close": float(row["Close"]),
                "Volume": int(float(row["Volume"]))
            })
        except Exception as e:
            continue  # skip malformed rows

    return response

# @router.get("/api/indicators")
# def get_indicators(symbol: str = "AAPL", interval: str = "1d", sma_period: int = 14, rsi_period: int = 14):
#     df = fetch_ohlcv(symbol, interval)
#     if df.empty:
#         return {"SMA": [], "RSI": []}

#     df = df.reset_index()
#     df["time"] = pd.to_datetime(df["datetime"]).view("int64") // 10**9

#     sma_series = compute_sma(df["Close"], sma_period)
#     rsi_series = compute_rsi(df["Close"], rsi_period)

#     sma_data = [{"time": int(df.loc[i, "time"]), "value": float(sma_series[i])}
#                 for i in range(len(sma_series)) if not pd.isna(sma_series[i])]
#     rsi_data = [{"time": int(df.loc[i, "time"]), "value": float(rsi_series[i])}
#                 for i in range(len(rsi_series)) if not pd.isna(rsi_series[i])]

#     return {"SMA": sma_data, "RSI": rsi_data}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.backend_router import router as backtest_router
from routers.market_data_router import router as market_data_router
from lifecycle.startup_cleanup import lifespan

app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(backtest_router)
app.include_router(market_data_router)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






# from fastapi import FastAPI
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from services.data_service import fetch_ohlcv, CACHE_DIR
# import asyncio
# import os
# from datetime import datetime, timedelta
# from typing import List
# import pandas as pd
# import time
# from routers.backend_router import router as backtest_router
# from contextlib import asynccontextmanager

# app = FastAPI()
# app.include_router(backtest_router)

# # Setup CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # or ["http://localhost:5174"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/api/ping")
# def ping():
#     return {"status": "ok"}

# @app.get("/api/ohlcv")
# def get_ohlcv(symbol: str = "AAPL", interval: str = "1d"):
#     df = fetch_ohlcv(symbol, interval)  # your existing function
#     if df.empty:
#         return []

#     df = df.reset_index()

#     # ✅ Rename and format cleanly
#     df.rename(columns={"datetime": "time"}, inplace=True)

#     response = []
#     for _, row in df.iterrows():
#         try:
#             response.append({
#                 "time": int(pd.to_datetime(row["time"]).timestamp()),  # UNIX seconds
#                 "Open": float(row["Open"]),
#                 "High": float(row["High"]),
#                 "Low": float(row["Low"]),
#                 "Close": float(row["Close"]),
#                 "Volume": int(float(row["Volume"]))
#             })
#         except Exception as e:
#             continue  # skip malformed rows

#     return response


# @app.get("/api/indicators")
# def get_indicators(
#     symbol: str = "AAPL",
#     interval: str = "1d",
#     sma_period: int = 14,
#     rsi_period: int = 14
# ):
#     df = fetch_ohlcv(symbol, interval)
#     if df.empty:
#         return {"SMA": [], "RSI": []}

#     df = df.reset_index()
#     df["time"] = pd.to_datetime(df["datetime"]).view("int64") // 10**9

#     sma_series = compute_sma(df["Close"], sma_period)
#     rsi_series = compute_rsi(df["Close"], rsi_period)

#     sma_data = [
#         {"time": int(df.loc[i, "time"]), "value": float(sma_series[i])}
#         for i in range(len(sma_series))
#         if not pd.isna(sma_series[i])
#     ]

#     rsi_data = [
#         {"time": int(df.loc[i, "time"]), "value": float(rsi_series[i])}
#         for i in range(len(rsi_series))
#         if not pd.isna(rsi_series[i])
#     ]

#     return {"SMA": sma_data, "RSI": rsi_data}


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # STARTUP logic
#     symbols = ["AAPL", "TSLA", "GOOGL"]
#     intervals = ["1d", "1min"]
#     print("🔥 Warming up symbol data for:", symbols)

#     for symbol in symbols:
#         for interval in intervals:
#             try:
#                 fetch_ohlcv(symbol, interval)
#             except Exception as e:
#                 print(f"❌ Warmup failed for {symbol} {interval}: {e}")

#     print("🧹 Cleaning old cache files...")
#     now = datetime.now()
#     for file in CACHE_DIR.glob("*.csv"):
#         modified = datetime.fromtimestamp(os.path.getmtime(file))
#         if (now - modified).days > 3:
#             try:
#                 file.unlink()
#                 print(f"🗑️ Deleted old cache: {file.name}")
#             except Exception as e:
#                 print(f"⚠️ Failed to delete {file.name}: {e}")

#     print("✅ Startup tasks complete.")
#     yield
#     # SHUTDOWN logic (optional)




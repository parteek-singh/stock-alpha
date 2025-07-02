from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.data_service import fetch_ohlcv, CACHE_DIR
from datetime import datetime
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP logic
    symbols = ["AAPL"]
    intervals = ["1min"]
    print("🔥 Warming up symbol data for:", symbols)

    for symbol in symbols:
        for interval in intervals:
            try:
                fetch_ohlcv(symbol, interval)
            except Exception as e:
                print(f"❌ Warmup failed for {symbol} {interval}: {e}")

    # Cleanup old cache files
    now = datetime.now()
    for file in CACHE_DIR.glob("*.csv"):
        try:
            if (now - datetime.fromtimestamp(os.path.getmtime(file))).days > 3:
                file.unlink()
                print(f"🗑️ Deleted old cache: {file.name}")
        except Exception as e:
            print(f"⚠️ Failed to delete {file.name}: {e}")

    print("✅ Startup tasks complete.")
    yield
    # SHUTDOWN logic (optional)

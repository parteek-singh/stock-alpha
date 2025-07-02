import pandas as pd

def compute_sma(series: pd.Series, period: int = 14) -> pd.Series:
    return series.rolling(window=period).mean()

def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    series = pd.to_numeric(series, errors='coerce')  # 🔐 Ensure float values

    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi



def compute_ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


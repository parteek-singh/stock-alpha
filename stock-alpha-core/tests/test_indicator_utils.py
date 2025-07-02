import pandas as pd
from utils.indicator_utils import IndicatorUtils

def mock_df():
    # Create a small dummy OHLCV dataset
    return pd.DataFrame({
        'Open': [100, 102, 101, 103, 104],
        'High': [102, 103, 104, 105, 106],
        'Low': [99, 100, 100, 102, 103],
        'Close': [101, 102, 103, 104, 105],
        'Volume': [1000, 1100, 1200, 1300, 1400]
    })

def test_add_rsi():
    df = mock_df()
    ind = IndicatorUtils(df)
    ind.add_indicator("RSI_14")
    df_new = ind.get_df()
    assert "RSI_14" in df_new.columns
    assert not df_new["RSI_14"].isnull().all()

def test_add_multiple_and_cache():
    df = mock_df()
    ind = IndicatorUtils(df)
    ind.add_indicator("EMA_20")
    ind.add_indicator("EMA_20")  # should be skipped
    df_new = ind.get_df()
    assert "EMA_20" in df_new.columns
    assert df_new.columns.tolist().count("EMA_20") == 1

def test_add_all_from_conditions():
    df = mock_df()
    ind = IndicatorUtils(df)
    ind.add_all_from_conditions(["RSI_14 < 30", "Close > EMA_20"])
    df_new = ind.get_df()
    assert "RSI_14" in df_new.columns
    assert "EMA_20" in df_new.columns

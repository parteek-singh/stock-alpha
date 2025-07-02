import pandas as pd
import pandas_ta as ta


class IndicatorUtils:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.calculated_indicators = set(self.df.columns)  # track what's already in the df

    def add_indicator(self, indicator: str):
        if indicator in self.calculated_indicators:
            return  # Skip if already calculated

        if indicator.startswith("RSI"):
            length = int(indicator.split("_")[1]) if "_" in indicator else 14
            col = f"RSI_{length}"
            if col not in self.df.columns:
                self.df[col] = ta.rsi(self.df["Close"], length=length)

        elif indicator.startswith("EMA"):
            length = int(indicator.split("_")[1])
            col = f"EMA_{length}"
            if col not in self.df.columns:
                self.df[col] = ta.ema(self.df["Close"], length=length)

        elif indicator.startswith("SMA"):
            length = int(indicator.split("_")[1])
            col = f"SMA_{length}"
            if col not in self.df.columns:
                self.df[col] = ta.sma(self.df["Close"], length=length)

        elif indicator == "MACD":
            if "MACD_12_26_9" not in self.df.columns:
                macd = ta.macd(self.df["Close"])
                self.df = pd.concat([self.df, macd], axis=1)

        elif indicator.startswith("BBANDS"):
            if "BBL_20_2.0" not in self.df.columns:
                bb = ta.bbands(self.df["Close"], length=20)
                self.df = pd.concat([self.df, bb], axis=1)

        self.calculated_indicators = set(self.df.columns)

    def add_all_from_conditions(self, conditions: list[str]):
        needed = set()
        for cond in conditions:
            tokens = cond.replace(">", " ").replace("<", " ").replace("=", " ").split()
            for token in tokens:
                if token.startswith(("RSI", "EMA", "SMA", "MACD", "BBANDS")):
                    needed.add(token)
        for ind in needed:
            self.add_indicator(ind)

    def add_all(self, indicators: list[str]):
        for name in indicators:
            self.add_indicator(name)
    
    @staticmethod
    def normalize_indicator_token(token: str) -> str:
        if token == "RSI":
            return "RSI_14"
        elif token == "EMA":
            return "EMA_14"
        elif token == "SMA":
            return "SMA_14"
        return token

    @staticmethod
    def normalize_lhs(lhs: str) -> str:
        """
        Normalize short indicator names like RSI/EMA/SMA to their default column names (e.g. RSI -> RSI_14).
        """
        if lhs.startswith("RSI") and "_" not in lhs:
            return "RSI_14"
        elif lhs.startswith("EMA") and "_" not in lhs:
            return "EMA_14"
        elif lhs.startswith("SMA") and "_" not in lhs:
            return "SMA_14"
        return lhs


    def get_df(self):
        return self.df

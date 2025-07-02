from typing import Optional
from fastapi import APIRouter, Body
from pydantic import BaseModel
import pandas as pd
# ✅ Absolute import (works when running main.py directly)
from evaluator import evaluate_conditions_group
from data_service import fetch_ohlcv
from indicator_utils import compute_rsi
from models import ConditionGroup
from utils.indicator_utils import IndicatorUtils
from typing import List, Union
from models import Condition, ConditionGroup

router = APIRouter()



class BacktestRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    interval: str
    entry_conditions: ConditionGroup
    exit_conditions: ConditionGroup
    stop_loss: Optional[float] = None

def extract_lhs_from_conditions(group: Union[Condition, ConditionGroup]) -> List[str]:
    lhs_list = []

    if isinstance(group, Condition):
        lhs_list.append(group.lhs)
    elif isinstance(group, ConditionGroup):
        for cond in group.conditions:
            lhs_list.extend(extract_lhs_from_conditions(cond))

    return lhs_list

def get_all_required_indicators(entry, exit) -> List[str]:
    tokens = extract_lhs_from_conditions(entry) + extract_lhs_from_conditions(exit)
    result = []
    for token in tokens:
        if token == "RSI":
            result.append("RSI_14")
        elif token == "EMA":
            result.append("EMA_14")
        elif token == "SMA":
            result.append("SMA_14")
        else:
            result.append(token)
    return list(set(result))


def condition_triggered(value, op, rhs):
    try:
        rhs = float(rhs)
        if op == ">": return value > rhs
        if op == "<": return value < rhs
        if op == ">=": return value >= rhs
        if op == "<=": return value <= rhs
        if op == "==": return value == rhs
    except Exception:
        return False




def get_triggered_conditions(conditions, row, ind_util):
    triggered = []
    for cond in conditions:
        if isinstance(cond, dict):
            lhs = cond["lhs"]
            op = cond["operator"]
            rhs = cond["rhs"]
        else:
            lhs = cond.lhs
            op = cond.operator
            rhs = cond.rhs

        # Normalize indicator name based on logic used in IndicatorUtils
        # print(f"ROW : {row}")
        # print(f"Processing condition: {lhs} {op} {rhs}")
        lhs_column = IndicatorUtils.normalize_indicator_token(lhs)

        value = row.get(lhs_column)

        print( f"Evaluating condition: {lhs} {op} {rhs} (value={value})")
        if value is not None:
            try:
                if eval(f"{value} {op} {float(rhs)}"):
                    triggered.append(f"{lhs}={round(value, 2)} {op} {rhs}")
            except:
                pass
    return triggered



@router.post("/api/backtest")
def run_backtest(req: BacktestRequest):
    df = fetch_ohlcv(req.symbol, req.interval)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df[(df["datetime"] >= req.start_date) & (df["datetime"] <= req.end_date)].copy()

    # Step 1: Add required indicators
    indicators = get_all_required_indicators(req.entry_conditions, req.exit_conditions)
    ind_util = IndicatorUtils(df)
    ind_util.add_all(indicators)
    df = ind_util.get_df()

    # Step 2: Drop rows with missing values
    df.dropna(subset=indicators, inplace=True)

    # Step 3: Simulate backtest
    in_trade = False
    entry_price = 0
    entry_time = None
    entry_condition_reason = None
    trades = []

    pnl_threshold = 0.0  # Can be made configurable
    exit_reason_counts = {"exit_condition": 0, "stop_loss": 0, "both": 0}
    print(f"Starting backtest for {req.symbol} from {req.start_date} to {req.end_date}")
    for _, row in df.iterrows():
        if not in_trade and evaluate_conditions_group(req.entry_conditions, row):
             # 🔍 Track entry condition that triggered the trade
                       # 👇 Evaluate and explain which exit condition triggered (if any)
            print(f"Evaluating entry conditions for row: {row['datetime']}")
            triggered_conditions = get_triggered_conditions(req.entry_conditions.conditions, row, ind_util)
            entry_condition_reason = " + ".join(triggered_conditions) if triggered_conditions else "entry_conditions matched"
            in_trade = True
            
            entry_price = float(row["Close"])
            entry_time = row["datetime"]


        elif in_trade:
            # Exit if exit condition or stop-loss hit
            exit_condition = evaluate_conditions_group(req.exit_conditions, row)
            sl_hit = False
            exit_reason = None
            exit_condition_reason = None

            if req.stop_loss is not None:
                sl_price = entry_price * (1 - req.stop_loss)
                sl_hit = float(row["Close"]) <= sl_price

            # 👇 Evaluate and explain which exit condition triggered (if any)
            triggered_conditions = get_triggered_conditions(req.exit_conditions.conditions, row, ind_util)
            exit_condition_reason = " + ".join(triggered_conditions) if triggered_conditions else "exit_condition matched"


            # Handle exit conditions
            if exit_condition or sl_hit:
                if exit_condition and sl_hit:
                    exit_reason = "exit + stop_loss"
                    exit_reason_counts["both"] += 1
                elif exit_condition:
                    exit_reason = "exit"
                    exit_reason_counts["exit_condition"] += 1
                elif sl_hit:
                    exit_reason = "stop_loss"
                    exit_reason_counts["stop_loss"] += 1
                    
                exit_price = float(row["Close"])
                pnl = (exit_price - entry_price) / entry_price * 100
                outcome = "win" if pnl > pnl_threshold else "loss"
                duration = (row["datetime"] - entry_time).days

                trades.append({
                    "entry_time": entry_time,
                    "entry_price": round(entry_price, 2),
                    "entry_condition_reason": entry_condition_reason,
                    "exit_time": row["datetime"],
                    "exit_price": round(exit_price, 2),
                    "pnl_percent": round(pnl, 2),
                    "outcome": outcome,
                    "duration_days": duration,
                    "exit_reason": exit_reason,
                    "exit_condition_reason": exit_condition_reason if exit_condition else None
                })
                in_trade = False

    total_pnl = sum(t["pnl_percent"] for t in trades)
    win_count = sum(1 for t in trades if t["outcome"] == "win")
    loss_count = len(trades) - win_count

    return {
        "total_trades": len(trades),
        "total_pnl_percent": round(total_pnl, 2),
        "wins": win_count,
        "losses": loss_count,
        "exit_reasons": exit_reason_counts,
        "trades": trades
    }



# @router.post("/api/backtest")
# def run_backtest(req: BacktestRequest):
#     df = fetch_ohlcv(req.symbol, req.interval)
#     df["datetime"] = pd.to_datetime(df["datetime"])
#     df = df[(df["datetime"] >= req.start_date) & (df["datetime"] <= req.end_date)].copy()
    
#     # Step 1: Add required indicators
#     indicators = get_all_required_indicators(req.entry_conditions, req.exit_conditions)

#     for ind in indicators:
#         if ind == "RSI":
#             df["RSI"] = compute_rsi(df["Close"], period=14)
#         elif ind == "EMA":
#             df["EMA"] = df["Close"].ewm(span=14).mean()
#         elif ind == "SMA":
#             df["SMA"] = df["Close"].rolling(window=14).mean()

#     # Step 2: Drop rows with missing values
#     df.dropna(subset=indicators, inplace=True)

#     # Step 3: Simulate backtest
#     in_trade = False
#     entry_price = 0
#     trades = []

#     for _, row in df.iterrows():
#         if not in_trade and evaluate_conditions_group(req.entry_conditions, row):
#             in_trade = True
#             entry_price = float(row["Close"])
#             entry_time = row["datetime"]

#         elif in_trade:
#             # Exit if exit condition or stop-loss hit
#             exit_condition = evaluate_conditions_group(req.exit_conditions, row)
#             sl_hit = req.stop_loss and float(row["Close"]) <= entry_price * (1 - req.stop_loss)

#             if exit_condition or sl_hit:
#                 exit_price = float(row["Close"])
#                 pnl = (exit_price - entry_price) / entry_price * 100
#                 trades.append({
#                     "entry_time": entry_time,
#                     "entry_price": round(entry_price,2),
#                     "exit_time": row["datetime"],
#                     "exit_price": round(exit_price,2),
#                     "pnl_percent": round(pnl,2)
#                 })
#                 in_trade = False

#     total_pnl = sum(t["pnl_percent"] for t in trades)
#     return {
#         "total_trades": len(trades),
#         "total_pnl_percent": round(total_pnl, 2),
#         "trades": trades
#     }

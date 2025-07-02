import operator

from utils.indicator_utils import IndicatorUtils
from typing import List, Union
from models import Condition, ConditionGroup
import pandas as pd

# Supported operators
OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}

def evaluate_condition_row(condition: dict, row: dict) -> bool:
    lhs = row.get(condition["lhs"])
    rhs = condition["rhs"]

    if lhs is None:
        print(f"⚠️ Skipping condition: {condition} — missing {condition['lhs']} in row {row}")
        return False  # or raise Exception("Missing value")
    
    # If rhs is another column name, fetch its value from row
    if isinstance(rhs, str) and rhs in row:
        rhs = row[rhs]


    op = OPS.get(condition["operator"])
    if op is None:
        raise ValueError(f"Unsupported operator: {condition['operator']}")

    try:
        return op(lhs, float(rhs))
    except Exception as e:
        print(f"Evaluation error: {e}")
        return False

def evaluate_conditions_group(group: Union[ConditionGroup, Condition], row: pd.Series) -> bool:
    if isinstance(group, Condition):
        lhs = group.lhs
        op = group.operator
        rhs = group.rhs

        lhs_column = IndicatorUtils.normalize_lhs(lhs)
        value = row.get(lhs_column)
        if value is None or pd.isna(value):
            return False  # invalid or missing value

        try:
            return eval(f"{value} {op} {rhs}")
        except:
            return False

    if isinstance(group, ConditionGroup):
        results = [
            evaluate_conditions_group(cond, row)
            for cond in group.conditions
        ]
        return all(results) if group.logic == "and" else any(results)




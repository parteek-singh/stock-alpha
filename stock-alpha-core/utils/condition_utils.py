from typing import Union, List
from models.condition_models import Condition, ConditionGroup
from utils.indicator_utils import IndicatorUtils

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

def get_triggered_conditions(conditions, row):
    triggered = []
    for cond in conditions:
        lhs = cond["lhs"] if isinstance(cond, dict) else cond.lhs
        op = cond["operator"] if isinstance(cond, dict) else cond.operator
        rhs = cond["rhs"] if isinstance(cond, dict) else cond.rhs

        lhs_column = IndicatorUtils.normalize_indicator_token(lhs)
        value = row.get(lhs_column)
        if value is not None:
            try:
                if eval(f"{value} {op} {float(rhs)}"):
                    triggered.append(f"{lhs}={round(value, 2)} {op} {rhs}")
            except:
                pass
    return triggered

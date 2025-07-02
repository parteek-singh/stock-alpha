from pydantic import BaseModel
from typing import Union, List, Literal, Optional



class Condition(BaseModel):
    lhs: str
    operator: Literal['>', '<', '>=', '<=', '==']
    rhs: float

class ConditionGroup(BaseModel):
    logic: Literal['and', 'or']
    conditions: List[Union['Condition', 'ConditionGroup']]

ConditionGroup.model_rebuild()

class BacktestRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    interval: str
    entry_conditions: ConditionGroup
    exit_conditions: ConditionGroup
    stop_loss: Optional[float] = None


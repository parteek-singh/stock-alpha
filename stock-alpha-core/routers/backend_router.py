from fastapi import APIRouter
from models.condition_models import BacktestRequest
from services.backtest_service import BacktestService

router = APIRouter()

@router.post("/api/backtest")
def run_backtest(req: BacktestRequest):
    return BacktestService().run_backtest(req)

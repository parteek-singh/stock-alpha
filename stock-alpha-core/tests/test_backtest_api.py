import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_backtest_endpoint_success():
    payload = {
        "symbol": "AAPL",
        "start_date": "2023-01-01",
        "end_date": "2023-03-01",
        "interval": "1d",
        "entry_conditions": {
            "logic": "and",
            "conditions": [
                {"lhs": "RSI_14", "operator": "<", "rhs": 30.0}
            ]
        },
        "exit_conditions": {
            "logic": "or",
            "conditions": [
                {"lhs": "RSI_14", "operator": ">", "rhs": 70.0}
            ]
        },
        "stop_loss": 0.05
    }

    response = client.post("/api/backtest", json=payload)
    print(response.status_code)
    print(response.json())

    assert response.status_code == 200
    data = response.json()
    print(data)
    assert "total_trades" in data
    assert "total_pnl_percent" in data
    assert isinstance(data["trades"], list)

    if data["trades"]:
        trade = data["trades"][0]
        assert "entry_time" in trade
        assert "exit_time" in trade
        assert "pnl_percent" in trade

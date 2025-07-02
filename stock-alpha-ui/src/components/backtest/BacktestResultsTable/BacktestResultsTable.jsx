import React, { useEffect, useState } from "react";
import "./BacktestResultsTable.css";

const BacktestResultsTable = ({ results }) => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    console.log("Backtest results:", results);
    if (!results) return null;
    setData(results || []);
    // You can add any additional logic here if needed
  }, [results]);

  return (
    <div className="backtest-results-container">
      <h2>📊 Backtest Summary</h2>

      <div className="summary-cards">
        <div className="card">
          <div className="card-label">Total Trades</div>
          <div className="card-value">{data.total_trades}</div>
        </div>
        <div className="card">
          <div className="card-label">Profit / Loss %</div>
          <div className={`card-value ${data.total_pnl_percent >= 0 ? "profit" : "loss"}`}>
            {data.total_pnl_percent}%
          </div>
        </div>
        <div className="card">
          <div className="card-label">Win Trades</div>
          <div className="card-value">{data.wins}</div>
        </div>
        <div className="card">
          <div className="card-label">Loose Trades</div>
          <div className="card-value">{data.losses}</div>
        </div>
      </div>
      <p className="card-label">Exit reasons - condition matched</p>
      <div className="summary-cards">
        
        <div className="card">
          <div className="card-label">Exit condition</div>
          <div className="card-value">{data.exit_reasons?.exit_condition}</div>
        </div>
        
        <div className="card">
          <div className="card-label">Stop loss</div>
          <div className="card-value">{data.exit_reasons?.stop_loss}</div>
        </div>
        <div className="card">
          <div className="card-label">Both</div>
          <div className="card-value">{data.exit_reasons?.both}</div>
        </div>
      </div>

      <table className="backtest-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Entry Time</th>
            <th>Entry Price</th>
            <th>Exit Time</th>
            <th>Exit Price</th>
            <th>PnL (%)</th>
            <th>Exit Reason</th>
          </tr>
        </thead>
        <tbody>
          {data.trades?.map((trade, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{new Date(trade.entry_time).toLocaleDateString()}</td>
              <td>{trade.entry_price}</td>
              <td>{new Date(trade.exit_time).toLocaleDateString()}</td>
              <td>{trade.exit_price}</td>
              <td className={trade.pnl_percent >= 0 ? "profit" : "loss"}>
                {trade.pnl_percent?.toFixed(2)}%
              </td>
              <td>{trade.exit_reason}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BacktestResultsTable;

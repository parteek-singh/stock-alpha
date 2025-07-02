import React, { useState } from "react";
import { ConditionBuilder } from "./ConditionBuilder";

export const StrategyConditions = () => {
  const [conditions, setConditions] = useState({
    logic: "and",
    conditions: [],
  });

  const handleBacktest = () => {
    fetch("/api/backtest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ conditions }),
    })
      .then((res) => res.json())
      .then(console.log);
  };

  return (
    <div>
      <h3>📋 Strategy Builder</h3>
      <ConditionBuilder group={conditions} onChange={setConditions} />
      <button onClick={handleBacktest} style={{ marginTop: 12 }}>
        🚀 Run Backtest
      </button>
    </div>
  );
};

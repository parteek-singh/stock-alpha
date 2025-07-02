import { useState } from "react";
import { ConditionBuilder } from "../ConditionsPanel/ConditionBuilder";
import InputField from "../lib/InputField/InputField.jsx";
import Button from "../lib/Button/Button.jsx";
import BacktestResultsTable from "./BacktestResultsTable/BacktestResultsTable.jsx";

const BackTestPanel = (props) => {
  const [results, setResults] = useState(null);

  const [startDate, setStartDate] = useState("2025-02-01");
  const [endDate, setEndDate] = useState("2025-02-28");
  const [stoploss, setStoploss] = useState(3);
  const [entryConditions, setEntryConditions] = useState({
    logic: "and",
    conditions: [],
  });
  const [exitConditions, setExitConditions] = useState({
    logic: "and",
    conditions: [],
  });

  const handleBacktest = () => {
    const payload = {
      symbol: props.symbol || "AAPL",
      interval: props.interval || "1d",
      start_date: startDate,
      end_date: endDate,
      entry_conditions: entryConditions,
      exit_conditions: exitConditions,
      stop_loss: stoploss || 5,
    };

    fetch("http://localhost:8000/api/backtest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Backtest results:", data);
        props.onResult(data); // Call the parent callback with results
        setResults(data); // Save to state
        // Handle results here, e.g., display them in a modal or table
      })
      .catch((error) => {
        console.error("Error running backtest:", error);
        alert("Backtest failed. Check console for details.");
      });
  };

  return (
    <div>
      <div>
        <h1>Backtest Panel</h1>
        <div style={{ display: "flex", gap: "10px" , flexWrap:"wrap"}}>
          <InputField
            label="Start Date"
            type="date"
            value={startDate}
            onChange={setStartDate}
          />
          <InputField
            label="Start Date"
            type="date"
            value={endDate}
            onChange={setEndDate}
          />
          <InputField
            label="Stop Loss(%)"
            type="number"
            placeholder="Stop Loss %"
            value={stoploss}
            step="0.01"
            onChange={setStoploss}
          />
        </div>
        <div style={{ margin: "20px 0px" }}>
          <strong>Symbol:</strong> {props.symbol || "AAPL"} <br />
          <strong>Interval:</strong> {props.interval || "1d"} <br />
        </div>
        <h2>Conditions</h2>

        <div style={{ display: "flex", flexDirection: "row", gap: "10px", flexWrap:"wrap" }}>
          <ConditionBuilder
            title="Entry Conditions"
            group={entryConditions}
            onChange={setEntryConditions}
          />
          <ConditionBuilder
            title="Exit Conditions"
            group={exitConditions}
            onChange={setExitConditions}
          />
        </div>
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <Button onClick={handleBacktest} style={{ marginTop: 12 }}>
            🚀 Run Backtest
          </Button>
        </div>
      </div>
      {results && <BacktestResultsTable results={results} />}
    </div>
  );
};

export default BackTestPanel;

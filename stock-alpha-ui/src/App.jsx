import { useState } from "react";
import TickerChart from "./components/TickerChart";
import BackTestPanel from "./components/backtest/BackTestPanel";
import TickerSearchBar from "./components/ticker_search/TickerSerachBar";

function App() {
  const [symbol, setSymbol] = useState("");
  const [interval, setInterval] = useState("");
  const [refreshChart, setRefreshChart] = useState(false);
  const [showTickerChart, setShowTickerChart] = useState(false);
  const [backTestResult, setBackTestResult] = useState([]);

  const handleTickerSearchChange = (symbol, interval) => {
    setSymbol(symbol);
    setInterval(interval);
    setShowTickerChart(true);
    handleRefreshChart();
    console.log("Symbol changed to:", symbol + " with interval: " + interval);
  };

  const handleRefreshChart = () => {
    setRefreshChart(false);
    setTimeout(() => {
      setRefreshChart(true);
      console.log("Chart refresh triggered!!");
    }, 200);
    
    console.log("Chart refresh triggered");
  };
const onResultCall = (results) =>{
  setBackTestResult(results)
  handleRefreshChart();
  console.log("Backtest results updated, refreshing chart..."+results);
}

  return (
    <div id="sd" style={{margin:"10px"}}>
      <h1>Stock</h1>
      <TickerSearchBar  onChange={handleTickerSearchChange} />
      {refreshChart && showTickerChart && <TickerChart symbol={symbol} interval={interval} backTestResult={backTestResult}/>}
      <BackTestPanel symbol={symbol} interval={interval} onResult={onResultCall}/>
    </div>
  );
}

export default App;

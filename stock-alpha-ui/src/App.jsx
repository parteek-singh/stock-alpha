import { useState } from "react";
import TickerChart from "./components/TickerChart";
import BackTestPanel from "./components/backtest/BackTestPanel";
import TickerSearchBar from "./components/ticker_search/TickerSerachBar";

function App() {
  const [symbol, setSymbol] = useState("");
  const [interval, setInterval] = useState("");
  const [refreshChart, setRefreshChart] = useState(true);
  const [backTestResult, setBackTestResult] = useState([]);

  const handleSymbolChange = (newSymbol) => {
    setSymbol(newSymbol);
    handleRefreshChart();
    console.log("Symbol changed to:", newSymbol);
  };

  const handleIntervalChange = (newInterval) => {
    setInterval(newInterval);
    handleRefreshChart();
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
      <TickerSearchBar onSymbolChange={handleSymbolChange} onIntervalChange={handleIntervalChange} />
      {refreshChart && <TickerChart symbol={symbol} interval={interval} backTestResult={backTestResult}/>}
      <BackTestPanel symbol={symbol} interval={interval} onResult={onResultCall}/>
    </div>
  );
}

export default App;

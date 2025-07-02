import React, { useEffect, useRef, useState } from "react";
import { createChart } from "lightweight-charts";

const TickerChart = (props) => {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const [symbol, setSymbol] = useState("AAPL");
  const [interval, setInterval] = useState("1d");
  const [hoverData, setHoverData] = useState(null);
  const [backtestResults, setBacktestResults] = useState(null);
  // const [showTrades, setShowTrades] = useState(true);
  // const [tooltipData, setTooltipData] = useState(null);

  const tradeColor = (type, pnl) => {
    if (type === "buy") return pnl >= 0 ? "#4CAF50" : "#F44336";   // green/red
    if (type === "sell") return pnl >= 0 ? "#2196F3" : "#FF9800"; // blue/orange
  };

  useEffect(() => {
    setBacktestResults(props.backtestResults || null);
    setSymbol(props.symbol || "AAPL");
    setInterval(props.interval || "1d");
    const fetchChartData = async () => {
      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/ohlcv?symbol=${symbol}&interval=${interval}`
        );
        const data = await res.json();

        if (!Array.isArray(data)) {
          console.warn("No candle data received");
          return;
        }

        const candles = data
          .filter(
            (row) => row.time && row.Open && row.High && row.Low && row.Close
          )
          .map((row) => ({
            time: Number(row.time),
            open: parseFloat(row.Open),
            high: parseFloat(row.High),
            low: parseFloat(row.Low),
            close: parseFloat(row.Close),
          }));

        if (candles.length === 0) {
          console.warn("⚠️ No valid candles found to render.");
          return;
        }

        if (chartContainerRef.current) {
          // Remove old chart
          if (chartRef.current) {
            chartRef.current.remove();
          }
          const container = chartContainerRef.current;
          const chart = createChart(chartContainerRef.current, {
            width: container.clientWidth,
            height: container.clientHeight,
            layout: {
              background: { color: "white" },
              textColor: "black",
            },
            grid: {
              vertLines: { color: "#eee" },
              horzLines: { color: "#eee" },
            },
          });
          chart.applyOptions({
            localization: {
              timeFormatter: (timestamp) => {
                const date = new Date(timestamp * 1000);
                return date.toISOString().split("T")[0]; // YYYY-MM-DD
              },
            },
          });

          


          const series = chart.addCandlestickSeries();
          series.setData(candles);
          console.log("📈 props.backtestResult set:", props.backTestResult);
          if (props.backTestResult && props.backTestResult.trades?.length > 0) {
            const markers = props.backTestResult.trades.flatMap((trade) => {
              return [
                {
                  time: Math.floor(new Date(trade.entry_time).getTime() / 1000),
                  position: "belowBar",
                  color: tradeColor("buy", trade.pnl_percent),
                  shape: "arrowUp",
                  text: `Buy @ ${trade.entry_price.toFixed(2)}`,
                },
                {
                  time: Math.floor(new Date(trade.exit_time).getTime() / 1000),
                  position: "aboveBar",
                  color: tradeColor("sell", trade.pnl_percent),
                  shape: "arrowDown",
                  text: `Sell @ ${trade.exit_price.toFixed(
                    2
                  )} (${trade.pnl_percent.toFixed(2)}%)`,
                },
              ];
            });

            series.setMarkers(markers);
          }

          // Tooltip setup
          // const tooltip = document.createElement("div");
          // tooltip.className = "chart-tooltip";
          // tooltip.style.position = "absolute";
          // tooltip.style.display = "none";
          // tooltip.style.pointerEvents = "none";
          // tooltip.style.backgroundColor = "#fff";
          // tooltip.style.border = "1px solid #ccc";
          // tooltip.style.padding = "6px";
          // tooltip.style.borderRadius = "4px";
          // chartContainerRef.current.appendChild(tooltip);

          chart.subscribeCrosshairMove((param) => {
            if (!param || !param.time || !param.seriesData) {
              setHoverData(null);
              return;
            }

            const candle = param.seriesData.get(series);
            if (candle) {
              const volume =
                data.find((d) => Number(d.time) === param.time)?.Volume || null;

            //   tooltip.innerHTML = `
            //   <strong>${symbol}</strong><br/>
            //   Date: ${new Date(param.time * 1000).toLocaleDateString()}<br/>
            //   Open: ${candle.open}<br/>
            //   High: ${candle.high}<br/>
            //   Low: ${candle.low}<br/>
            //   Close: ${candle.close}<br/>
            // `;
            //   tooltip.style.left = param.point.x + 20 + "px";
            //   tooltip.style.top = param.point.y + 20 + "px";
            //   tooltip.style.display = "block";

              setHoverData({
                time: new Date(param.time * 1000).toLocaleDateString(),
                open: candle.open,
                high: candle.high,
                low: candle.low,
                close: candle.close,
                volume,
              });
            }
          });

          chartRef.current = chart;
          const resizeObserver = new ResizeObserver(() => {
            chart.applyOptions({
              width: container.clientWidth,
              height: container.clientHeight,
            });
          });
        
          resizeObserver.observe(container);
        
          return () => {
            resizeObserver.disconnect();
            chart.remove();
          };
        }
      } catch (err) {
        console.error("📉 Chart fetch error:", err);
      }
    };

    fetchChartData();

    return () => {
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [symbol, interval, backtestResults]);

  return (
    <div style={{ padding: 20 }}>
      <h2>📈 Ticker Chart Viewer</h2>
      
      {hoverData && (
        <div style={{ marginBottom: 10, fontFamily: "monospace" }}>
          <strong>{hoverData.time}</strong> | O: {hoverData.open?.toFixed(2)}{" "}
          &nbsp; H: {hoverData.high?.toFixed(2)} &nbsp; L:{" "}
          {hoverData.low?.toFixed(2)} &nbsp; C: {hoverData.close?.toFixed(2)}{" "}
          &nbsp; V: {hoverData.volume?.toLocaleString()}
        </div>
      )}
      {!hoverData && (
        <div style={{ marginBottom: 10, fontFamily: "monospace" }}>
          <strong>{}</strong> | O: {}{" "}
          &nbsp; H: {} &nbsp; L:{" "}
          &nbsp; V: 
        </div>
      )}

      <div ref={chartContainerRef} style={{ position: "relative", width: "100%", height: "400px" }}/>

      {/* <label style={{ marginLeft: 20 }}>
          <input
            type="checkbox"
            checked={showTrades}
            onChange={(e) => setShowTrades(e.target.checked)}
          />
          Show Trades
        </label> */}
    </div>
  );
};

export default TickerChart;

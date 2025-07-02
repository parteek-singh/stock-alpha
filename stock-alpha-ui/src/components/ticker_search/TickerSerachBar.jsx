import { useState } from "react";

const TickerSearchBar = ({ onSymbolChange, onIntervalChange }) => {
    const [symbol, setSymbol] = useState("AAPL");
    const [interval, setInterval] = useState("1d");

    const handleSymbolChange = (value) => {
        setSymbol(value);
        onSymbolChange(value, interval);
    };

    const handleIntervalChange = (value) => {
        setInterval(value);
        onIntervalChange(symbol, value);
    };

    return (
        <div>
            <div style={{ marginBottom: 12 }}>
                <input
                    value={symbol}
                    onChange={(e) => handleSymbolChange(e.target.value.toUpperCase())}
                    style={{ padding: 6, fontSize: 16, width: 160 }}
                />
                <select
                    value={interval}
                    onChange={(e) => handleIntervalChange(e.target.value)}
                    style={{ marginLeft: 10, padding: 6, fontSize: 16 }}
                >
                    <option value="1min">1min</option>
                    <option value="5min">5min</option>
                    <option value="15min">15min</option>
                    <option value="1d">1d</option>
                    <option value="1wk">1wk</option>
                </select>
            </div>
        </div>
    );
}

export default TickerSearchBar;

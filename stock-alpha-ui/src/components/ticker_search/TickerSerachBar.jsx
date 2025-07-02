import { useState } from "react";
import InputField from "../lib/InputField/InputField";
import LabeledSelect from "../lib/Select/LabeledSelect";
import Button from "../lib/Button/Button";
import "./TickerSearchBar.css"; // Assuming you have some styles for the search bar

const TickerSearchBar = ({ onChange }) => {
    const [symbol, setSymbol] = useState("AAPL");
    const [interval, setInterval] = useState("1d");


    const handleSearch = () => {  
        console.log("Searching for symbol:", symbol, "with interval:", interval);  
        onChange(symbol, interval);
    }

    const INDICATOR_FIELDS = {
        "1min": [ "1min"], 
        // "5min": [ "5min"],
        // "15min": [ "15min"],
        "1d": [ "1d"],
        // "1wk": [ "1wk"],
      };

    return (
        <div>
            <div className={"searchbar-container"}>
                <InputField
                    label="Symbol"
                    value={symbol}
                    onChange={ setSymbol}
                    style={{ padding: 6, fontSize: 16, width: 160 }}
                />
                <LabeledSelect 
                    label="Interval"
                    value={interval}
                    onChange={(e) => setInterval(e.target.value)}
                    style={{ marginLeft: 10, padding: 6, fontSize: 16 }}
                    options={Object.keys(INDICATOR_FIELDS).map((ind) => ({ label: ind, value: ind }))}
                >
                </LabeledSelect>
                <Button onClick={handleSearch}>Search</Button>
            </div>
            <p>For testing purpose only AAPL, GOOGL, TSLA and interval 1d works</p>
        </div>
    );
}

export default TickerSearchBar;

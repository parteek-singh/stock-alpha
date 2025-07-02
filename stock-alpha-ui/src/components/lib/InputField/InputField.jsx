import React from "react";
import "./InputField.css";

const InputField = ({ label, value, onChange, type = "text", placeholder }) => {
  return (
    <div className="input-field-container">
      <label className="input-label">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}  
        placeholder={placeholder || "Enter value ..."}
        className="input-box"
      />
    </div>
  );
};

export default InputField;

import React from "react";
import "./Select.css"; // Reuse same CSS for consistency

const LabeledSelect = ({ label, value, onChange, options, id }) => {
  return (
    <div className="input-field-container">
      <label htmlFor={id} className="input-label">{label}</label>
      <select
        id={id}
        value={value}
        onChange={onChange}
        className="input-box"
      >
        {options.map(opt => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LabeledSelect;


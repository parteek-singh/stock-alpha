import React from "react";
import "./Button.css";

const Button = ({ onClick, type = "button", children, disabled }) => {
  return (
    <button
      onClick={(e) => onClick?.(e)}
      type={type}
      className="custom-button"
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;

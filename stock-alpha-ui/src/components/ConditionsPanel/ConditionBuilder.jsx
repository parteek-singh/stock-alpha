import React from "react";

const fields = ["RSI", "EMA_20", "SMA_50", "Close", "Open", "Volume"];
const operators = ["<", ">", "<=", ">=", "==", "!="];

export const ConditionBuilder = ({ title, group, onChange, onRemove }) => {
  const updateCondition = (index, updated) => {
    const newGroup = { ...group };
    newGroup.conditions[index] = updated;
    onChange(newGroup);
  };

  const removeCondition = (index) => {
    const newGroup = {
      ...group,
      conditions: group.conditions.filter((_, i) => i !== index),
    };
    onChange(newGroup);
  };

  const addCondition = () => {
    onChange({
      ...group,
      conditions: [...group.conditions, { lhs: "RSI", operator: "<", rhs: 30 }],
    });
  };

  const addGroup = () => {
    onChange({
      ...group,
      conditions: [...group.conditions, { logic: "and", conditions: [] }],
    });
  };

  const changeLogic = (e) => {
    onChange({ ...group, logic: e.target.value });
  };

  return (
    <div
      style={{
        border: "1px solid #ccc",
        padding: 12,
        marginBottom: 12,
        borderRadius: 6,
      }}
    >
      <h3>{title}</h3>
      <div style={{ marginBottom: 10 }}>
        <strong>Logic:</strong>{" "}
        <select value={group.logic} onChange={changeLogic}>
          <option value="and">AND</option>
          <option value="or">OR</option>
        </select>
        {onRemove && (
          <button
            onClick={onRemove}
            style={{
              marginLeft: 12,
              color: "red",
              border: "none",
              background: "transparent",
            }}
          >
            🗑 Remove Group
          </button>
        )}
      </div>

      {group.conditions.map((cond, i) =>
        "logic" in cond ? (
          <ConditionBuilder
            key={i}
            group={cond}
            onChange={(updated) => updateCondition(i, updated)}
            onRemove={() => removeCondition(i)}
          />
        ) : (
          <div
            key={i}
            style={{
              display: "flex",
              gap: 8,
              alignItems: "center",
              marginBottom: 8,
            }}
          >
            <select
              value={cond.lhs}
              onChange={(e) =>
                updateCondition(i, { ...cond, lhs: e.target.value })
              }
            >
              {fields.map((f) => (
                <option key={f} value={f}>
                  {f}
                </option>
              ))}
            </select>
            <select
              value={cond.operator}
              onChange={(e) =>
                updateCondition(i, { ...cond, operator: e.target.value })
              }
            >
              {operators.map((op) => (
                <option key={op} value={op}>
                  {op}
                </option>
              ))}
            </select>
            <input
              value={cond.rhs}
              onChange={(e) =>
                updateCondition(i, { ...cond, rhs: e.target.value })
              }
              style={{ width: 80 }}
            />
            <button onClick={() => removeCondition(i)}>🗑</button>
          </div>
        )
      )}

      <div style={{ marginTop: 10 }}>
        <button onClick={addCondition}>+ Add Condition</button>
        <button onClick={addGroup} style={{ marginLeft: 10 }}>
          + Add Group
        </button>
      </div>
    </div>
  );
};

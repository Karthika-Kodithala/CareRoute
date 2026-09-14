import { useState } from "react";
import { STRESS_TEST_SCENARIOS } from "../../data/demoScenarios";

export default function StressTestModal({
  isOpen,
  onClose,
  onExecuteTurn,
  onResetSession,
}) {
  const [selectedScenario, setSelectedScenario] = useState(STRESS_TEST_SCENARIOS[0]);
  const [currentTurnIdx, setCurrentTurnIdx] = useState(0);

  if (!isOpen) return null;

  const handleSelectScenario = (sc) => {
    setSelectedScenario(sc);
    setCurrentTurnIdx(0);
  };

  const handlePlayNextTurn = () => {
    if (currentTurnIdx < selectedScenario.turns.length) {
      const msg = selectedScenario.turns[currentTurnIdx];
      onExecuteTurn(msg);
      setCurrentTurnIdx((prev) => prev + 1);
    }
  };

  const handlePlayAll = async () => {
    onResetSession();
    for (let i = 0; i < selectedScenario.turns.length; i++) {
      onExecuteTurn(selectedScenario.turns[i]);
      await new Promise((r) => setTimeout(r, 700));
    }
    setCurrentTurnIdx(selectedScenario.turns.length);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container" style={{ maxWidth: "800px" }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <span>▶</span>
            <span>TEST A FAILURE MODE (STRESS TEST)</span>
          </div>
          <button className="close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <p style={{ fontSize: "13px", color: "var(--text-secondary)", marginBottom: "16px" }}>
          Select a benchmark scenario to simulate real-time conversational edge cases and observe how CareRoute dynamically reassesses patient risk:
        </p>

        {/* Scenario Selection Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", marginBottom: "20px" }}>
          {STRESS_TEST_SCENARIOS.map((sc) => (
            <div
              key={sc.id}
              onClick={() => handleSelectScenario(sc)}
              style={{
                padding: "12px 14px",
                borderRadius: "var(--radius-md)",
                background: selectedScenario.id === sc.id ? "var(--primary-blue-bg)" : "#f8fafc",
                border: selectedScenario.id === sc.id ? "1px solid var(--primary-blue)" : "1px solid var(--border-subtle)",
                cursor: "pointer",
                transition: "all 0.18s ease",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "4px" }}>
                <span style={{ fontSize: "13px", fontWeight: 700, color: "var(--text-primary)" }}>
                  {sc.title}
                </span>
                <span className="status-badge live" style={{ fontSize: "10px", padding: "2px 6px" }}>
                  {sc.badge}
                </span>
              </div>
              <div style={{ fontSize: "11px", color: "var(--text-secondary)" }}>{sc.description}</div>
            </div>
          ))}
        </div>

        {/* Selected Scenario Preview */}
        <div
          style={{
            background: "#f8fafc",
            border: "1px solid var(--border-subtle)",
            borderRadius: "var(--radius-md)",
            padding: "18px",
            marginBottom: "20px",
          }}
        >
          <div style={{ fontSize: "12px", fontWeight: 700, color: "var(--primary-blue)", textTransform: "uppercase", marginBottom: "8px" }}>
            Scenario Conversation Steps:
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "8px", marginBottom: "16px" }}>
            {selectedScenario.turns.map((turnText, i) => (
              <div
                key={i}
                style={{
                  padding: "8px 12px",
                  borderRadius: "var(--radius-sm)",
                  background: i < currentTurnIdx ? "var(--emerald-bg)" : "#ffffff",
                  border: i < currentTurnIdx ? "1px solid var(--emerald-border)" : "1px solid var(--border-subtle)",
                  fontSize: "13px",
                  color: i < currentTurnIdx ? "#065f46" : "var(--text-secondary)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                <span>
                  <strong>Step {i + 1}:</strong> "{turnText}"
                </span>
                <span style={{ fontSize: "11px", fontWeight: 600 }}>{i < currentTurnIdx ? "✓ Completed" : "Pending"}</span>
              </div>
            ))}
          </div>

          {/* V1 vs V2 Preview */}
          <div className="diff-grid" style={{ marginBottom: 0 }}>
            <div className="diff-card before" style={{ padding: "10px" }}>
              <div style={{ fontSize: "11px", fontWeight: 700, color: "#991b1b" }}>V1 BASELINE ❌</div>
              <div style={{ fontSize: "12px", color: "var(--text-secondary)", marginTop: "4px" }}>
                {selectedScenario.v1Behavior}
              </div>
            </div>
            <div className="diff-card after" style={{ padding: "10px", background: "var(--emerald-bg)", borderColor: "var(--emerald-border)" }}>
              <div style={{ fontSize: "11px", fontWeight: 700, color: "#065f46" }}>
                V2 IMPROVEMENT ✓
              </div>
              <div style={{ fontSize: "12px", color: "var(--text-secondary)", marginTop: "4px" }}>
                {selectedScenario.v2Behavior}
              </div>
            </div>
          </div>
        </div>

        {/* Modal Controls */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <button
            className="btn-secondary"
            onClick={() => {
              onResetSession();
              setCurrentTurnIdx(0);
            }}
          >
            🔄 Reset Conversation
          </button>
          <div style={{ display: "flex", gap: "10px" }}>
            <button
              className="btn-secondary"
              onClick={handlePlayNextTurn}
              disabled={currentTurnIdx >= selectedScenario.turns.length}
            >
              Play Step {currentTurnIdx + 1}
            </button>
            <button className="btn-primary" onClick={handlePlayAll}>
              ▶ Play All Steps & Reassess
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

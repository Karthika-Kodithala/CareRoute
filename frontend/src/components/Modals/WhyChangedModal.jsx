export default function WhyChangedModal({ isOpen, onClose, whyData }) {
  if (!isOpen) return null;

  const data = whyData || {
    before: {
      symptoms: ["Dizziness"],
      risk: "moderate",
      route: "Routine evaluation / primary care consultation",
    },
    newInfo: "Fainting (Syncope) detected",
    events: [
      "✓ Message ingested and parsed for clinical entities",
      "✓ Context compared with existing patient state graph",
      "⚡ New important information detected: Fainting (Syncope)",
      "✓ Patient state updated",
      "✓ Risk level reassessed from MODERATE to EMERGENCY",
      "✓ Care route recalculated from Routine to Emergency evaluation",
    ],
    after: {
      symptoms: ["Dizziness", "Fainting"],
      risk: "emergency",
      route: "Immediate emergency evaluation (Call 911 / Go to ED)",
    },
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <span>❓</span>
            <span>WHY DID CAREROUTE CHANGE?</span>
          </div>
          <button className="close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Before / After Diff Columns */}
        <div className="diff-grid">
          <div className="diff-card before">
            <h4>BEFORE</h4>
            <div className="diff-item">
              <div className="diff-label">Symptoms:</div>
              <div className="diff-value">
                {data.before.symptoms.length > 0 ? data.before.symptoms.join(", ") : "None reported"}
              </div>
            </div>
            <div className="diff-item">
              <div className="diff-label">Risk:</div>
              <div className="diff-value" style={{ color: "var(--amber-warning)" }}>
                {data.before.risk.toUpperCase()}
              </div>
            </div>
            <div className="diff-item">
              <div className="diff-label">Route:</div>
              <div className="diff-value">{data.before.route}</div>
            </div>
          </div>

          <div className="diff-card after">
            <h4 style={{ color: "#991b1b" }}>AFTER REASSESSMENT</h4>
            <div className="diff-item">
              <div className="diff-label">Symptoms:</div>
              <div className="diff-value">
                {data.after.symptoms.length > 0 ? data.after.symptoms.join(", ") : "Dizziness, Fainting"}
              </div>
            </div>
            <div className="diff-item">
              <div className="diff-label">Risk:</div>
              <div className="diff-value" style={{ color: "var(--coral-red)" }}>
                🔴 {data.after.risk.toUpperCase()}
              </div>
            </div>
            <div className="diff-item">
              <div className="diff-label">Route:</div>
              <div className="diff-value" style={{ color: "var(--coral-red)" }}>
                🚨 {data.after.route}
              </div>
            </div>
          </div>
        </div>

        {/* New Information Detected */}
        <div
          style={{
            background: "var(--coral-bg)",
            border: "1px solid var(--coral-border)",
            borderRadius: "var(--radius-md)",
            padding: "14px 18px",
            marginBottom: "18px",
          }}
        >
          <div style={{ fontSize: "11px", fontWeight: 700, textTransform: "uppercase", color: "#991b1b" }}>
            ⚡ NEW INFORMATION
          </div>
          <div style={{ fontSize: "14px", fontWeight: 700, color: "var(--text-primary)", marginTop: "4px" }}>
            {data.newInfo}
          </div>
        </div>

        {/* Reassessment System Events */}
        <div style={{ marginBottom: "18px" }}>
          <div style={{ fontSize: "12px", fontWeight: 700, textTransform: "uppercase", color: "var(--primary-blue)", marginBottom: "10px" }}>
            REASSESSMENT
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            {data.events.map((ev, i) => (
              <div
                key={i}
                style={{
                  fontSize: "13px",
                  color: ev.includes("⚡") ? "#991b1b" : "var(--text-secondary)",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  fontWeight: ev.includes("⚡") ? 600 : 400,
                }}
              >
                {ev}
              </div>
            ))}
          </div>
        </div>

        {/* Result Summary */}
        <div
          style={{
            background: "#f8fafc",
            border: "1px solid var(--border-subtle)",
            borderRadius: "var(--radius-md)",
            padding: "14px 18px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div>
            <div style={{ fontSize: "11px", color: "var(--text-secondary)", textTransform: "uppercase", fontWeight: 600 }}>
              RESULT
            </div>
            <div style={{ fontSize: "13px", fontWeight: 700, color: "var(--text-primary)", marginTop: "2px" }}>
              Routine evaluation <span style={{ color: "var(--primary-blue)" }}>→</span>{" "}
              <span style={{ color: "var(--coral-red)" }}>Emergency evaluation</span>
            </div>
          </div>
          <button className="btn-primary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default function FullPatientStateView({
  patientState,
  riskLevel,
  navigation,
  journeyEvents = [],
  sources = [],
}) {
  return (
    <div className="prism-view-container">
      <div className="panel-card" style={{ padding: "28px" }}>
        <div className="panel-header">
          <div className="panel-title">
            <span>👤</span> PATIENT STATE CONTEXT GRAPH
          </div>
          <div className="panel-subtitle">Live Session: {patientState?.session_id}</div>
        </div>

        {/* State Summary Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "20px" }}>
          {/* Symptoms */}
          <div className="diff-card before" style={{ background: "#fffbeb", borderColor: "var(--amber-border)" }}>
            <h4 style={{ color: "#92400e" }}>Extracted Symptoms</h4>
            {(!patientState?.symptoms || patientState.symptoms.length === 0) ? (
              <p style={{ fontSize: "12px", color: "var(--text-muted)" }}>No symptoms extracted yet.</p>
            ) : (
              <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                {patientState.symptoms.map((s, i) => (
                  <span key={i} className="state-chip symptom">
                    🟡 {s}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Critical Red Flags */}
          <div className="diff-card after">
            <h4 style={{ color: "#991b1b" }}>Critical Red Flags</h4>
            {(!patientState?.critical_flags || patientState.critical_flags.length === 0) ? (
              <p style={{ fontSize: "12px", color: "var(--text-muted)" }}>No critical red flags detected.</p>
            ) : (
              <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                {patientState.critical_flags.map((f, i) => (
                  <span key={i} className="state-chip critical">
                    🚨 {f}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Conditions */}
          <div className="diff-card" style={{ background: "var(--primary-blue-bg)", borderColor: "var(--primary-blue-border)" }}>
            <h4 style={{ color: "#1e40af" }}>Reported Medical Conditions</h4>
            {(!patientState?.conditions || patientState.conditions.length === 0) ? (
              <p style={{ fontSize: "12px", color: "var(--text-muted)" }}>None disclosed.</p>
            ) : (
              <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                {patientState.conditions.map((c, i) => (
                  <span key={i} className="state-chip" style={{ background: "#ffffff", color: "#1e40af", borderColor: "var(--primary-blue-border)" }}>
                    🩺 {c}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Medications */}
          <div className="diff-card" style={{ background: "#fdf4ff", borderColor: "#f0abfc" }}>
            <h4 style={{ color: "#701a75" }}>Reconciled Medications</h4>
            {(!patientState?.medications || patientState.medications.length === 0) ? (
              <p style={{ fontSize: "12px", color: "var(--text-muted)" }}>None disclosed.</p>
            ) : (
              <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                {patientState.medications.map((m, i) => (
                  <span key={i} className="state-chip" style={{ background: "#ffffff", color: "#701a75", borderColor: "#f0abfc" }}>
                    💊 {m}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Grounded Guidelines Cited */}
        {sources.length > 0 && (
          <div>
            <div style={{ fontSize: "12px", fontWeight: 700, textTransform: "uppercase", color: "var(--primary-blue)", marginBottom: "8px" }}>
              Grounded Guideline Citations
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
              {sources.map((s, i) => (
                <div
                  key={i}
                  style={{
                    padding: "12px 16px",
                    background: "#f8fafc",
                    border: "1px solid var(--border-subtle)",
                    borderRadius: "var(--radius-md)",
                  }}
                >
                  <div style={{ fontSize: "13px", fontWeight: 700, color: "var(--primary-blue)" }}>
                    {s.title} ({s.url_or_id})
                  </div>
                  <div style={{ fontSize: "12px", color: "var(--text-secondary)", marginTop: "4px" }}>
                    {s.snippet}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

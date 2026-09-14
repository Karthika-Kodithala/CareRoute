export default function PatientStateView({
  patientState,
  newInformation = [],
  riskLevel = "routine",
  navigation,
  safety,
  sources = [],
  onOpenWhyModal,
  onNavigateToCareRoute,
}) {
  const isEmergency = riskLevel === "emergency" || (navigation?.urgency || "").toLowerCase() === "emergency";

  return (
    <section className="panel-card patient-state-panel">
      <div className="panel-header">
        <div>
          <div className="panel-title">
            <span>👤</span> PATIENT STATE
          </div>
          <div className="panel-subtitle">
            Live extracted context
          </div>
        </div>
        <div className={`status-badge ${isEmergency ? "live" : "prism"}`} style={{ fontSize: "11px", background: isEmergency ? "var(--coral-bg)" : "var(--primary-blue-bg)", color: isEmergency ? "#991b1b" : "#1e40af" }}>
          {isEmergency ? "RED FLAG ACTIVE" : "MONITORING"}
        </div>
      </div>

      {/* Extracted Symptoms */}
      <div style={{ marginBottom: "14px" }}>
        <div style={{ fontSize: "11px", fontWeight: 700, textTransform: "uppercase", color: "var(--text-secondary)", marginBottom: "6px" }}>
          SYMPTOMS
        </div>
        <div className="state-chips-container">
          {(!patientState?.symptoms || patientState.symptoms.length === 0) ? (
            <span style={{ fontSize: "12px", color: "var(--text-muted)", fontStyle: "italic" }}>
              No symptoms reported yet.
            </span>
          ) : (
            patientState.symptoms.map((symptom, idx) => {
              const isNew = newInformation.includes(symptom);
              const isCritical = symptom.toLowerCase().includes("faint") || symptom.toLowerCase().includes("syncope") || symptom.toLowerCase().includes("chest");
              return (
                <div key={idx} className={`state-chip ${isCritical ? "critical" : "symptom"}`}>
                  <span>{isCritical ? "🔴" : "🟡"}</span>
                  <span>{symptom}</span>
                  {isNew && <span className="state-chip new-badge">NEW</span>}
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Conditions & Medications */}
      {(patientState?.conditions?.length > 0 || patientState?.medications?.length > 0) && (
        <div style={{ marginBottom: "14px" }}>
          <div style={{ fontSize: "11px", fontWeight: 700, textTransform: "uppercase", color: "var(--text-secondary)", marginBottom: "6px" }}>
            CONDITIONS & MEDICATIONS
          </div>
          <div className="state-chips-container">
            {patientState.conditions?.map((cond, i) => (
              <span key={`cond-${i}`} className="state-chip" style={{ background: "var(--primary-blue-bg)", color: "#1e40af", borderColor: "var(--primary-blue-border)" }}>
                🩺 {cond}
              </span>
            ))}
            {patientState.medications?.map((med, i) => (
              <span key={`med-${i}`} className="state-chip" style={{ background: "#f3e8ff", color: "#6b21a8", borderColor: "#e9d5ff" }}>
                💊 {med}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Critical Red Flags */}
      {patientState?.critical_flags?.length > 0 && (
        <div style={{ marginBottom: "14px" }}>
          <div style={{ fontSize: "11px", fontWeight: 700, textTransform: "uppercase", color: "#991b1b", marginBottom: "6px" }}>
            CRITICAL RED FLAGS
          </div>
          <div className="state-chips-container">
            {patientState.critical_flags.map((flag, i) => (
              <span key={`flag-${i}`} className="state-chip critical">
                🚨 {flag}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Risk Level Box */}
      <div className="risk-meter-box">
        <div className="risk-level-display">
          <span style={{ fontSize: "11px", color: "var(--text-secondary)", fontWeight: 700, textTransform: "uppercase" }}>
            RISK LEVEL
          </span>
          <span className={`risk-tag ${riskLevel}`}>
            {riskLevel === "emergency" ? "🔴 EMERGENCY" : riskLevel === "high" ? "🟠 HIGH" : riskLevel === "moderate" ? "🟡 MODERATE" : "🟢 ROUTINE"}
          </span>
        </div>
      </div>

      {/* Current Care Route Card */}
      <div className={`care-route-card ${isEmergency ? "emergency" : ""}`}>
        <div className="route-badge">
          <span>{isEmergency ? "🚨" : "🧭"}</span>
          <span>{isEmergency ? "CARE ROUTE UPDATED" : "CURRENT ROUTE"}</span>
        </div>
        <div className="route-desc">
          {navigation?.next_step || "Provide patient symptoms to generate recommended care route."}
        </div>
        <button className="btn-why-changed" onClick={onOpenWhyModal}>
          <span>❓</span>
          <span>WHY DID THIS CHANGE?</span>
        </button>
      </div>

      {/* Grounding & Safety Verification Status */}
      <div style={{ marginTop: "auto", paddingTop: "12px", borderTop: "1px solid var(--border-subtle)" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", fontSize: "11px", color: "var(--text-secondary)" }}>
          <span>Safety Verification:</span>
          <span style={{ color: safety?.passed ? "var(--emerald-green)" : "var(--amber-warning)", fontWeight: 600 }}>
            {safety?.passed ? "✓ Passed (Non-Diagnostic)" : "⚠ Needs Review"}
          </span>
        </div>
        {sources.length > 0 && (
          <div style={{ marginTop: "6px", fontSize: "11px", color: "var(--text-muted)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            <span>Source: </span>
            <span style={{ color: "var(--primary-blue)" }}>{sources[0].title}</span>
          </div>
        )}
      </div>
    </section>
  );
}

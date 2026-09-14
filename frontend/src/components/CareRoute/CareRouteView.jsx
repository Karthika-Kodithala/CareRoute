export default function CareRouteView({
  patientState,
  riskLevel,
  navigation,
  onOpenWhyModal,
}) {
  const isEmergency = riskLevel === "emergency" || (navigation?.urgency || "").toLowerCase() === "emergency";

  return (
    <div className="prism-view-container">
      {/* Route Flow Card */}
      <div className="panel-card" style={{ padding: "28px" }}>
        <div className="panel-header">
          <div className="panel-title">
            <span>🚑</span> CARE ROUTE NAVIGATION MATRIX
          </div>
          <div className="panel-subtitle">State-Aware Care Navigation Assistant (Non-Diagnostic)</div>
        </div>

        {/* Visual Pipeline Flow */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            background: "#f8fafc",
            border: "1px solid var(--border-subtle)",
            borderRadius: "var(--radius-lg)",
            padding: "20px 24px",
            marginBottom: "24px",
            overflowX: "auto",
            gap: "12px",
          }}
        >
          <div style={{ textAlign: "center" }}>
            <div className="node-icon-circle" style={{ margin: "0 auto 6px auto" }}>👤</div>
            <div style={{ fontSize: "11px", fontWeight: 700, color: "var(--text-secondary)" }}>PATIENT</div>
          </div>
          <span style={{ color: "var(--text-muted)" }}>→</span>
          <div style={{ textAlign: "center" }}>
            <div className="node-icon-circle" style={{ margin: "0 auto 6px auto" }}>📋</div>
            <div style={{ fontSize: "11px", fontWeight: 700, color: "var(--text-secondary)" }}>SITUATION</div>
          </div>
          <span style={{ color: "var(--text-muted)" }}>→</span>
          <div style={{ textAlign: "center" }}>
            <div className="node-icon-circle" style={{ margin: "0 auto 6px auto", color: "var(--coral-red)" }}>⚡</div>
            <div style={{ fontSize: "11px", fontWeight: 700, color: "var(--coral-red)" }}>IMPORTANT INFO</div>
          </div>
          <span style={{ color: "var(--text-muted)" }}>→</span>
          <div style={{ textAlign: "center" }}>
            <div className="node-icon-circle" style={{ margin: "0 auto 6px auto", color: "var(--primary-blue)" }}>🔄</div>
            <div style={{ fontSize: "11px", fontWeight: 700, color: "var(--primary-blue)" }}>REASSESSMENT</div>
          </div>
          <span style={{ color: "var(--text-muted)" }}>→</span>
          <div style={{ textAlign: "center" }}>
            <div className="node-icon-circle" style={{ margin: "0 auto 6px auto", background: isEmergency ? "var(--coral-bg)" : "var(--primary-blue-bg)", borderColor: isEmergency ? "var(--coral-border)" : "var(--primary-blue-border)" }}>
              {isEmergency ? "🚨" : "🧭"}
            </div>
            <div style={{ fontSize: "11px", fontWeight: 700, color: isEmergency ? "var(--coral-red)" : "var(--primary-blue)" }}>
              {isEmergency ? "EMERGENCY" : "RECOMMENDED ROUTE"}
            </div>
          </div>
        </div>

        {/* Highlighted Next Step Box */}
        <div className={`care-route-card ${isEmergency ? "emergency" : ""}`} style={{ padding: "24px", marginBottom: "20px" }}>
          <div className="route-badge" style={{ fontSize: "13px" }}>
            <span>{isEmergency ? "🚨" : "🧭"}</span>
            <span>YOUR RECOMMENDED NEXT STEP</span>
          </div>

          <div style={{ fontSize: "18px", fontWeight: 700, color: "var(--text-primary)", margin: "8px 0 14px 0", lineHeight: 1.4 }}>
            {navigation?.next_step}
          </div>

          <div style={{ fontSize: "13px", color: "var(--text-secondary)", marginBottom: "16px" }}>
            <strong>Navigation Reasoning:</strong> {navigation?.reasoning_summary}
          </div>

          <div style={{ display: "flex", gap: "12px" }}>
            <button className="btn-why-changed" onClick={onOpenWhyModal} style={{ width: "auto", padding: "10px 20px" }}>
              <span>❓</span>
              <span>WHY DID THIS CHANGE?</span>
            </button>
          </div>
        </div>

        {/* Triage Urgency Level Guide */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px" }}>
          <div style={{ padding: "14px", borderRadius: "var(--radius-md)", background: "var(--emerald-bg)", border: "1px solid var(--emerald-border)" }}>
            <div style={{ fontSize: "12px", fontWeight: 700, color: "#065f46", marginBottom: "4px" }}>
              🟢 ROUTINE (Primary Care)
            </div>
            <div style={{ fontSize: "12px", color: "var(--text-secondary)" }}>
              Mild, stable symptoms without acute red flags. Monitored self-care and outpatient appointment.
            </div>
          </div>

          <div style={{ padding: "14px", borderRadius: "var(--radius-md)", background: "var(--amber-bg)", border: "1px solid var(--amber-border)" }}>
            <div style={{ fontSize: "12px", fontWeight: 700, color: "#92400e", marginBottom: "4px" }}>
              🟡 URGENT CARE (Within 24h)
            </div>
            <div style={{ fontSize: "12px", color: "var(--text-secondary)" }}>
              Moderate symptoms, medication conflicts (diabetes), or persistent non-syncopal dizziness.
            </div>
          </div>

          <div style={{ padding: "14px", borderRadius: "var(--radius-md)", background: "var(--coral-bg)", border: "1px solid var(--coral-border)" }}>
            <div style={{ fontSize: "12px", fontWeight: 700, color: "#991b1b", marginBottom: "4px" }}>
              🔴 EMERGENCY (911 / ED)
            </div>
            <div style={{ fontSize: "12px", color: "var(--text-secondary)" }}>
              Syncope (fainting), acute chest pain, dyspnea, or neurological deficits. Immediate EMS dispatch.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

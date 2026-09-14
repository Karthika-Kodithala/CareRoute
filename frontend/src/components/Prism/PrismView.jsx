import { PRISM_EVALUATION_DATA } from "../../data/prismEvidence";

export default function PrismView() {
  const { summary, failureObserved, rootCause, engineeringFix, metricsTable, scenarioComparisons } =
    PRISM_EVALUATION_DATA;

  return (
    <div className="prism-view-container">
      {/* Hero Header */}
      <div className="prism-hero">
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <h2>PRISM EVALUATION</h2>
            <p style={{ fontWeight: 600, color: "var(--primary-blue)" }}>
              {summary.headline}
            </p>
            <p style={{ fontSize: "12px", color: "var(--text-secondary)", marginTop: "2px" }}>
              Evaluate → Identify Weakness → Improve → Re-evaluate
            </p>
          </div>
          <div className="status-badge live" style={{ fontSize: "13px", padding: "8px 16px" }}>
            ⭐ {summary.absoluteImprovement}
          </div>
        </div>
      </div>

      {/* 4-Stage PRISM Improvement Story Flow */}
      <div className="panel-card" style={{ padding: "20px" }}>
        <div className="panel-title" style={{ marginBottom: "16px" }}>
          <span>📈</span> PRISM IMPROVEMENT STORY
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "12px" }}>
          {/* Stage 1: V1 */}
          <div style={{ padding: "16px", borderRadius: "var(--radius-md)", background: "var(--coral-bg)", border: "1px solid var(--coral-border)" }}>
            <div style={{ fontSize: "14px", fontWeight: 800, color: "#991b1b", marginBottom: "6px" }}>
              1. V1 BASELINE ❌
            </div>
            <p style={{ fontSize: "12px", color: "#991b1b", lineHeight: 1.4 }}>
              Stateless turn handling missed late critical symptoms (fainting). Retained routine clinic route.
            </p>
          </div>

          {/* Stage 2: PRISM */}
          <div style={{ padding: "16px", borderRadius: "var(--radius-md)", background: "var(--amber-bg)", border: "1px solid var(--amber-border)" }}>
            <div style={{ fontSize: "14px", fontWeight: 800, color: "#92400e", marginBottom: "6px" }}>
              2. PRISM IDENTIFIES 🔍
            </div>
            <p style={{ fontSize: "12px", color: "#92400e", lineHeight: 1.4 }}>
              PRISM benchmark detected state drop across turns: 33.3% critical detection score.
            </p>
          </div>

          {/* Stage 3: FIX */}
          <div style={{ padding: "16px", borderRadius: "var(--radius-md)", background: "var(--primary-blue-bg)", border: "1px solid var(--primary-blue-border)" }}>
            <div style={{ fontSize: "14px", fontWeight: 800, color: "#1e40af", marginBottom: "6px" }}>
              3. ENGINEERING FIX 🔧
            </div>
            <p style={{ fontSize: "12px", color: "#1e40af", lineHeight: 1.4 }}>
              Implemented persistent state graph + change detection delta engine + automated reassessment.
            </p>
          </div>

          {/* Stage 4: V2 */}
          <div style={{ padding: "16px", borderRadius: "var(--radius-md)", background: "var(--emerald-bg)", border: "1px solid var(--emerald-border)" }}>
            <div style={{ fontSize: "14px", fontWeight: 800, color: "#065f46", marginBottom: "6px" }}>
              4. V2 PROOF ✓
            </div>
            <p style={{ fontSize: "12px", color: "#065f46", lineHeight: 1.4 }}>
              Replayed identical scenarios: 100% critical detection and emergency routing accuracy.
            </p>
          </div>
        </div>
      </div>

      {/* Root Cause & Fix Details */}
      <div className="diff-grid" style={{ marginBottom: 0 }}>
        <div className="panel-card" style={{ padding: "18px" }}>
          <div className="panel-title" style={{ color: "var(--coral-red)", marginBottom: "8px" }}>
            <span>🔍</span> WHAT FAILED (ROOT CAUSE)
          </div>
          <ul style={{ paddingLeft: "18px", fontSize: "13px", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "6px" }}>
            {rootCause.points.map((pt, i) => (
              <li key={i}>{pt}</li>
            ))}
          </ul>
        </div>

        <div className="panel-card" style={{ padding: "18px" }}>
          <div className="panel-title" style={{ color: "var(--emerald-green)", marginBottom: "8px" }}>
            <span>🛠️</span> WHAT WE CHANGED (FIX)
          </div>
          <ul style={{ paddingLeft: "18px", fontSize: "13px", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "6px" }}>
            {engineeringFix.points.map((pt, i) => (
              <li key={i}>{pt}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Actual PRISM Metrics Table */}
      <div className="panel-card">
        <div className="panel-header">
          <div className="panel-title">
            <span>📊</span> PRISM BENCHMARK METRICS
          </div>
          <div className="panel-subtitle">Recorded before/after evidence across test scenarios</div>
        </div>

        <table className="metric-table">
          <thead>
            <tr>
              <th>Evaluation Metric</th>
              <th>Description</th>
              <th>V1 Baseline</th>
              <th>V2 Improvement</th>
              <th>Measured Delta</th>
            </tr>
          </thead>
          <tbody>
            {metricsTable.map((row, idx) => (
              <tr key={idx}>
                <td>
                  <strong>{row.metric}</strong>
                </td>
                <td style={{ color: "var(--text-secondary)", fontSize: "12px" }}>{row.description}</td>
                <td style={{ color: "var(--coral-red)", fontWeight: 600 }}>{row.v1}</td>
                <td style={{ color: "var(--emerald-green)", fontWeight: 700 }}>{row.v2}</td>
                <td>
                  <span className="status-badge live" style={{ fontSize: "11px", padding: "2px 8px" }}>
                    {row.delta}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Scenario Breakdown */}
      <div className="panel-card">
        <div className="panel-header">
          <div className="panel-title">
            <span>🔬</span> SCENARIO EVIDENCE BREAKDOWN
          </div>
          <div className="panel-subtitle">Individual scenario pass/fail proof</div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {scenarioComparisons.map((item) => (
            <div
              key={item.id}
              style={{
                padding: "12px 16px",
                background: "#f8fafc",
                border: "1px solid var(--border-subtle)",
                borderRadius: "var(--radius-md)",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
              }}
            >
              <div>
                <strong style={{ fontSize: "13px", color: "var(--text-primary)" }}>{item.title}</strong>
                <div style={{ fontSize: "12px", color: "var(--text-secondary)", marginTop: "2px" }}>
                  <span style={{ color: "var(--coral-red)" }}>V1: {item.v1Detail}</span> →{" "}
                  <span style={{ color: "var(--emerald-green)" }}>V2: {item.v2Detail}</span>
                </div>
              </div>
              <div style={{ display: "flex", gap: "8px" }}>
                <span className="state-chip critical" style={{ fontSize: "11px" }}>
                  {item.v1Result}
                </span>
                <span className="status-badge live" style={{ fontSize: "11px" }}>
                  {item.v2Result}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

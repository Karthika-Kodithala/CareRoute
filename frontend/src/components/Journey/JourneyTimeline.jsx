import { useState } from "react";

export default function JourneyTimeline({
  patientState,
  riskLevel,
  navigation,
  journeyEvents = [],
}) {
  const [selectedNode, setSelectedNode] = useState(null);

  const hasSymptoms = (patientState?.symptoms || []).length > 0;
  const hasCritical = (patientState?.critical_flags || []).length > 0;
  const isReassessed = journeyEvents.length > 1;

  const STAGES = [
    {
      id: "stage-1",
      title: "UNDERSTAND",
      icon: "✓",
      status: hasSymptoms ? "completed" : "active",
      detail: hasSymptoms
        ? `Ingested patient message. Symptoms: ${patientState.symptoms.join(", ")}`
        : "Listening to patient conversational input.",
    },
    {
      id: "stage-2",
      title: "EXTRACT",
      icon: hasSymptoms ? "✓" : "🔄",
      status: hasSymptoms ? "completed" : "pending",
      detail: hasSymptoms
        ? `Structured context: ${patientState.symptoms.length} symptoms, ${patientState.conditions?.length || 0} conditions extracted into state graph.`
        : "Extracting clinical entities into graph.",
    },
    {
      id: "stage-3",
      title: "CHANGE DETECTED",
      icon: hasCritical ? "⚡" : isReassessed ? "✓" : "🔄",
      status: hasCritical ? "completed" : isReassessed ? "completed" : "pending",
      detail: hasCritical
        ? `⚡ Critical state change detected: ${patientState.critical_flags.join(", ")}`
        : isReassessed
        ? "State delta tracked across turns."
        : "Monitoring for state transitions.",
    },
    {
      id: "stage-4",
      title: "REASSESS",
      icon: isReassessed ? "🔄" : "⏱️",
      status: isReassessed ? "completed" : "pending",
      detail: `Current Risk Level: ${riskLevel.toUpperCase()}. Event-triggered navigation reassessment performed.`,
    },
    {
      id: "stage-5",
      title: "CARE ROUTE",
      icon: "🚑",
      status: isReassessed ? "completed" : "pending",
      detail: navigation?.next_step || "Recommended care route generated.",
    },
  ];

  return (
    <div className="journey-panel">
      <div className="panel-header" style={{ marginBottom: "8px", paddingBottom: "8px" }}>
        <div className="panel-title">
          <span>🧭</span> PATIENT JOURNEY
        </div>
        <div className="panel-subtitle">
          Understand → Remember → Detect Change → Reassess → Navigate (Click to inspect)
        </div>
      </div>

      <div className="journey-steps-row">
        {STAGES.map((stage, idx) => (
          <div key={stage.id} style={{ display: "flex", alignItems: "center", flex: 1 }}>
            <div
              className={`journey-node ${stage.status === "completed" ? "active" : ""}`}
              onClick={() => setSelectedNode(stage)}
              style={{ width: "100%" }}
            >
              <div className="node-icon-circle">
                <span style={{ fontWeight: 700 }}>{stage.icon}</span>
              </div>
              <span className="node-label">{stage.title}</span>
            </div>
            {idx < STAGES.length - 1 && <span className="journey-arrow" style={{ margin: "0 8px" }}>→</span>}
          </div>
        ))}
      </div>

      {selectedNode && (
        <div
          style={{
            marginTop: "12px",
            padding: "12px 16px",
            background: "var(--primary-blue-bg)",
            border: "1px solid var(--primary-blue-border)",
            borderRadius: "var(--radius-md)",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div>
            <strong style={{ color: "var(--primary-blue)", fontSize: "13px" }}>
              Stage: {selectedNode.title} —
            </strong>{" "}
            <span style={{ fontSize: "13px", color: "var(--text-primary)" }}>{selectedNode.detail}</span>
          </div>
          <button
            className="btn-secondary"
            style={{ fontSize: "11px", padding: "4px 8px" }}
            onClick={() => setSelectedNode(null)}
          >
            Close
          </button>
        </div>
      )}
    </div>
  );
}

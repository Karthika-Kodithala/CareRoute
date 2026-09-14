export default function PatientState({ state, changes = [] }) {
  if (!state) {
    return (
      <section className="card">
        <h2>Patient State</h2>
        <p className="muted">Waiting for conversation...</p>
      </section>
    );
  }

  return (
    <section className="card">
      <h2>Live Patient State</h2>
      <div className="state-grid">
        <div><b>Symptoms</b><span>{state.symptoms?.join(", ") || "—"}</span></div>
        <div><b>Conditions</b><span>{state.conditions?.join(", ") || "—"}</span></div>
        <div><b>Medications</b><span>{state.medications?.join(", ") || "—"}</span></div>
        <div><b>Critical flags</b><span>{state.critical_flags?.join(", ") || "None"}</span></div>
      </div>

      <h3>State changes</h3>
      {changes.length ? changes.map((item, i) => <p className="change" key={i}>⚠ {item}</p>) : <p className="muted">No changes detected.</p>}
    </section>
  );
}

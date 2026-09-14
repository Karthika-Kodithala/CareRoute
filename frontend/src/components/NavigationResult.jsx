export default function NavigationResult({ navigation, safety, sources = [] }) {
  return (
    <section className="card">
      <h2>Navigation</h2>
      {!navigation ? (
        <p className="muted">Navigation will appear here.</p>
      ) : (
        <>
          <div className="badge">{navigation.urgency}</div>
          <h3>Recommended next step</h3>
          <p>{navigation.next_step}</p>
          <h3>Safety</h3>
          <p>{safety?.passed ? "✓ Verification passed" : "⚠ Verification flagged issues"}</p>
          {sources.length > 0 && (
            <>
              <h3>Sources</h3>
              <ul>{sources.map((s, i) => <li key={i}>{s.title}</li>)}</ul>
            </>
          )}
        </>
      )}
    </section>
  );
}

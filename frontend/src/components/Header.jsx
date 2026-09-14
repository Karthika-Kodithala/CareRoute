export default function Header({ onOpenStressTest, onResetSession }) {
  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-icon">🩺</div>
        <div className="brand-text">
          <h1>CareRoute</h1>
          <p>Intelligent Patient Navigation</p>
        </div>
      </div>

      <div className="header-status">
        <div className="status-badge live">
          <span className="pulse-dot"></span>
          AI ACTIVE
        </div>
        <div className="status-badge prism">
          <span>✓</span>
          PRISM CONNECTED
        </div>
      </div>

      <div className="header-actions">
        <button
          className="prompt-btn alert"
          onClick={onOpenStressTest}
          title="Run pre-configured failure and stress-test scenarios"
        >
          ▶ STRESS TEST CAREROUTE
        </button>
        <button
          className="btn-secondary"
          onClick={onResetSession}
          title="Reset conversation and patient state context"
        >
          🔄 New Session
        </button>
      </div>
    </header>
  );
}

import { useState, useRef, useEffect } from "react";
import { DEMO_PROMPTS } from "../../data/demoScenarios";

export default function ChatView({
  messages,
  onSendMessage,
  loading,
  stateChangeBanner,
  onOpenWhyModal,
}) {
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim() || loading) return;
    onSendMessage(inputValue.trim());
    setInputValue("");
  };

  const handlePromptClick = (promptMessage) => {
    if (loading) return;
    onSendMessage(promptMessage);
  };

  return (
    <section className="panel-card chat-view-panel">
      <div className="panel-header">
        <div>
          <div className="panel-title">
            <span>💬</span> PATIENT CONVERSATION
          </div>
          <div className="panel-subtitle">
            Live interaction with CareRoute
          </div>
        </div>
      </div>

      {/* Quick Demo Buttons */}
      <div className="quick-prompts-bar">
        <span style={{ fontSize: "11px", fontWeight: 700, color: "var(--primary-blue)", textTransform: "uppercase" }}>
          Quick Demo:
        </span>
        {DEMO_PROMPTS.map((prompt) => (
          <button
            key={prompt.id}
            className={`prompt-btn ${prompt.id === "fainted" ? "alert" : ""}`}
            onClick={() => handlePromptClick(prompt.message)}
            disabled={loading}
          >
            <span>{prompt.icon}</span>
            <span>{prompt.label}</span>
          </button>
        ))}
      </div>

      {/* State Change Alert Banner */}
      {stateChangeBanner && (
        <div className="state-alert-banner">
          <div className="alert-content">
            <h4>{stateChangeBanner.title}</h4>
            <p>{stateChangeBanner.message}</p>
          </div>
          <button className="btn-secondary" onClick={onOpenWhyModal} style={{ fontSize: "11px", padding: "5px 12px" }}>
            Why Did This Change?
          </button>
        </div>
      )}

      {/* Message Stream */}
      <div className="chat-stream">
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-bubble ${msg.role}`}>
            <div className="bubble-meta">
              <span>{msg.role === "patient" ? "👤 Patient" : "🩺 CareRoute AI"}</span>
              <span>{msg.timestamp}</span>
            </div>
            <div style={{ color: msg.role === "patient" ? "#1e3a8a" : "var(--text-primary)" }}>
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-bubble assistant" style={{ fontStyle: "italic", background: "#f8fafc" }}>
            <div className="bubble-meta">
              <span>🩺 CareRoute AI</span>
              <span>Reassessing...</span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "var(--primary-blue)" }}>
              <span className="pulse-dot"></span>
              <span>Updating patient state and reassessing care route...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Composer */}
      <form onSubmit={handleSubmit} className="chat-composer">
        <input
          type="text"
          className="chat-input"
          placeholder="Type a patient response..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          disabled={loading}
        />
        <button type="submit" className="btn-primary" disabled={loading || !inputValue.trim()}>
          {loading ? "..." : "Send"}
        </button>
      </form>
    </section>
  );
}

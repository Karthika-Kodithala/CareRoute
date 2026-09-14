import { useState } from "react";

export default function Chat({ messages, onSend, loading }) {
  const [value, setValue] = useState("");

  function submit(event) {
    event.preventDefault();
    if (!value.trim() || loading) return;
    onSend(value.trim());
    setValue("");
  }

  return (
    <section className="card chat">
      <h2>Conversation</h2>
      <div className="messages">
        {messages.length === 0 && (
          <p className="muted">Try: “I'm dizzy.”</p>
        )}
        {messages.map((message, index) => (
          <div className={`message ${message.role}`} key={index}>
            <strong>{message.role === "patient" ? "Patient" : "CareRoute"}</strong>
            <span>{message.text}</span>
          </div>
        ))}
      </div>
      <form onSubmit={submit} className="composer">
        <input
          value={value}
          onChange={(event) => setValue(event.target.value)}
          placeholder="Describe the situation..."
        />
        <button type="submit">{loading ? "..." : "Send"}</button>
      </form>
    </section>
  );
}

import { useState } from "react";
import { sendMessage } from "../services/api";
import Chat from "../components/Chat";
import PatientState from "../components/PatientState";
import NavigationResult from "../components/NavigationResult";
import PrismPanel from "../components/PrismPanel";

export default function Dashboard() {
  const [sessionId] = useState("demo-001");
  const [messages, setMessages] = useState([]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSend(message) {
    setMessages((items) => [...items, { role: "patient", text: message }]);
    setLoading(true);

    try {
      const result = await sendMessage(sessionId, message);
      setData(result);
      setMessages((items) => [
        ...items,
        { role: "assistant", text: result.response },
      ]);
    } catch (error) {
      setMessages((items) => [
        ...items,
        { role: "assistant", text: `Connection error: ${error.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header>
        <h1>CareRoute</h1>
        <p>AI Patient Navigation — stateful, grounded, evaluated.</p>
      </header>

      <section className="grid">
        <Chat messages={messages} onSend={handleSend} loading={loading} />
        <PatientState state={data?.patient_state} changes={data?.state_changes} />
        <NavigationResult navigation={data?.navigation} safety={data?.safety} sources={data?.sources} />
        <PrismPanel />
      </section>
    </main>
  );
}

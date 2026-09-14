export default function Sidebar({ activeTab, onTabSelect }) {
  const navItems = [
    { id: "chat", label: "Conversation", icon: "💬" },
    { id: "state", label: "Patient State", icon: "👤" },
    { id: "journey", label: "Patient Journey", icon: "🧭" },
    { id: "careroute", label: "Care Route", icon: "🚑" },
    { id: "prism", label: "PRISM Evaluation", icon: "🔬" },
  ];

  return (
    <aside className="sidebar-nav">
      {navItems.map((item) => (
        <button
          key={item.id}
          className={`nav-item ${activeTab === item.id ? "active" : ""}`}
          onClick={() => onTabSelect(item.id)}
        >
          <span className="nav-icon">{item.icon}</span>
          <span>{item.label}</span>
        </button>
      ))}
    </aside>
  );
}

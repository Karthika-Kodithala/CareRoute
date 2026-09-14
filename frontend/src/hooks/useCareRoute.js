import { useState, useCallback, useRef } from "react";
import { sendMessage } from "../services/api";

const INITIAL_STATE = {
  session_id: "demo-session-001",
  symptoms: [],
  conditions: [],
  medications: [],
  critical_flags: [],
  missing_information: [],
};

export function useCareRoute() {
  const [sessionId, setSessionId] = useState(`demo-${Date.now().toString(36)}`);
  const [messages, setMessages] = useState([
    {
      id: "msg-0",
      role: "assistant",
      text: "Hello. I am CareRoute, an AI patient navigation assistant. Please describe what symptoms or health concerns you are experiencing.",
      timestamp: "Just now",
    },
  ]);

  const [patientState, setPatientState] = useState(INITIAL_STATE);
  const [previousPatientState, setPreviousPatientState] = useState(null);
  const [newInformation, setNewInformation] = useState([]);
  const [stateChangeBanner, setStateChangeBanner] = useState(null);

  const [riskLevel, setRiskLevel] = useState("routine"); // routine | moderate | high | emergency
  const [previousRiskLevel, setPreviousRiskLevel] = useState(null);

  const [navigation, setNavigation] = useState({
    urgency: "routine",
    next_step: "Describe your symptoms to receive grounded clinical navigation.",
    reasoning_summary: "Awaiting patient input.",
  });
  const [previousNavigation, setPreviousNavigation] = useState(null);

  const [safety, setSafety] = useState({ passed: true, safety_flags: [], grounding_flags: [] });
  const [sources, setSources] = useState([]);
  const [latestTraceId, setLatestTraceId] = useState("");
  const [loading, setLoading] = useState(false);

  // Active view tab: 'chat' | 'state' | 'journey' | 'careroute' | 'prism'
  const [activeTab, setActiveTab] = useState("chat");
  const [isWhyModalOpen, setIsWhyModalOpen] = useState(false);
  const [isStressModalOpen, setIsStressModalOpen] = useState(false);
  const [selectedJourneyStage, setSelectedJourneyStage] = useState(null);

  // Timeline events
  const [journeyEvents, setJourneyEvents] = useState([
    {
      id: "j-init",
      title: "Session Initialized",
      detail: "CareRoute navigation session started. Context graph active.",
      status: "completed",
      icon: "🟢",
    },
  ]);

  // Why it changed comparison state
  const [whyChangedData, setWhyChangedData] = useState(null);

  const handleSendMessage = useCallback(
    async (textToSend) => {
      if (!textToSend.trim()) return;

      const userMsgId = `msg-${Date.now()}-user`;
      const timeStr = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

      setMessages((prev) => [
        ...prev,
        { id: userMsgId, role: "patient", text: textToSend, timestamp: timeStr },
      ]);
      setLoading(true);

      try {
        const result = await sendMessage(sessionId, textToSend, patientState);
        const nextState = result.patient_state || patientState;
        const stateChanges = result.state_changes || [];
        const isCriticalChange =
          stateChanges.some((c) => c.includes("⚡") || c.includes("CRITICAL")) ||
          (result.navigation?.urgency === "emergency" && riskLevel !== "emergency");

        // Record previous before updating
        setPreviousPatientState(patientState);
        setPreviousRiskLevel(riskLevel);
        setPreviousNavigation(navigation);

        // Identify new items
        const newlyAdded = [];
        (nextState.symptoms || []).forEach((s) => {
          if (!patientState.symptoms.includes(s)) newlyAdded.push(s);
        });
        (nextState.critical_flags || []).forEach((f) => {
          if (!patientState.critical_flags.includes(f)) newlyAdded.push(f);
        });
        setNewInformation(newlyAdded);

        // Update Risk Level based on urgency and critical flags
        let calculatedRisk = "routine";
        const urgencyLower = (result.navigation?.urgency || "routine").toLowerCase();
        if (urgencyLower === "emergency" || nextState.critical_flags.length > 0) {
          calculatedRisk = "emergency";
        } else if (urgencyLower === "urgent-care" || urgencyLower === "high") {
          calculatedRisk = "high";
        } else if (urgencyLower === "moderate" || nextState.symptoms.length > 0) {
          calculatedRisk = "moderate";
        }
        setRiskLevel(calculatedRisk);

        // State Change Banner trigger
        if (isCriticalChange || stateChanges.length > 0) {
          setStateChangeBanner({
            title: isCriticalChange ? "⚡ IMPORTANT INFORMATION DETECTED" : "🔄 PATIENT STATE UPDATED",
            message: stateChanges[0] || "New symptom context extracted",
            type: isCriticalChange ? "emergency" : "update",
          });
          setTimeout(() => setStateChangeBanner(null), 6000);
        }

        // Build "Why Changed" explanation data
        if (newlyAdded.length > 0 || isCriticalChange || stateChanges.length > 0) {
          setWhyChangedData({
            before: {
              symptoms: [...patientState.symptoms],
              risk: riskLevel,
              route: navigation.next_step || "Routine evaluation",
            },
            newInfo: newlyAdded.length > 0 ? newlyAdded.join(", ") : stateChanges.join(", "),
            events: [
              "✓ Message ingested and parsed for clinical entities",
              "✓ Context compared with existing patient state graph",
              isCriticalChange
                ? "⚡ Red-flag symptom detected (Syncope / Acute Red Flag)"
                : "✓ New clinical context extracted and integrated",
              `✓ Risk level reassessed from ${riskLevel.toUpperCase()} to ${calculatedRisk.toUpperCase()}`,
              "✓ Grounded clinical navigation rules calculated next step",
              "✓ Safety constraints & non-diagnostic bounds verified",
            ],
            after: {
              symptoms: [...(nextState.symptoms || [])],
              risk: calculatedRisk,
              route: result.navigation?.next_step || "Emergency clinical evaluation",
            },
          });
        }

        // Update Main State
        setPatientState(nextState);
        setNavigation(result.navigation || navigation);
        setSafety(result.safety || { passed: true });
        setSources(result.sources || []);
        setLatestTraceId(result.trace_id || "");

        // Add assistant message
        const assistantMsgId = `msg-${Date.now()}-bot`;
        setMessages((prev) => [
          ...prev,
          {
            id: assistantMsgId,
            role: "assistant",
            text: result.response,
            timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
            urgency: result.navigation?.urgency,
            stateChanges,
          },
        ]);

        // Append Journey Events
        setJourneyEvents((prev) => [
          ...prev,
          {
            id: `j-${Date.now()}-1`,
            title: `Turn Processed (${newlyAdded.length > 0 ? "New Info" : "Clarification"})`,
            detail: `Extracted: ${newlyAdded.join(", ") || "No new entity"}. Urgency: ${result.navigation?.urgency}.`,
            status: "completed",
            icon: isCriticalChange ? "🚨" : "✓",
          },
        ]);
      } catch (err) {
        console.error("Error sending message:", err);
      } finally {
        setLoading(false);
      }
    },
    [sessionId, patientState, riskLevel, navigation]
  );

  const resetSession = useCallback(() => {
    const newId = `demo-${Date.now().toString(36)}`;
    setSessionId(newId);
    setPatientState(INITIAL_STATE);
    setPreviousPatientState(null);
    setNewInformation([]);
    setRiskLevel("routine");
    setPreviousRiskLevel(null);
    setNavigation({
      urgency: "routine",
      next_step: "Describe your symptoms to receive grounded clinical navigation.",
      reasoning_summary: "Awaiting patient input.",
    });
    setPreviousNavigation(null);
    setSafety({ passed: true, safety_flags: [], grounding_flags: [] });
    setSources([]);
    setStateChangeBanner(null);
    setWhyChangedData(null);
    setMessages([
      {
        id: "msg-init",
        role: "assistant",
        text: "Hello. I am CareRoute, an AI patient navigation assistant. Please describe what symptoms or health concerns you are experiencing.",
        timestamp: "Just now",
      },
    ]);
    setJourneyEvents([
      {
        id: "j-reset",
        title: "Session Reset",
        detail: "Cleared patient context. Ready for new evaluation scenario.",
        status: "completed",
        icon: "🟢",
      },
    ]);
  }, []);

  return {
    sessionId,
    messages,
    patientState,
    previousPatientState,
    newInformation,
    riskLevel,
    previousRiskLevel,
    navigation,
    previousNavigation,
    safety,
    sources,
    latestTraceId,
    loading,
    stateChangeBanner,
    whyChangedData,
    journeyEvents,
    activeTab,
    setActiveTab,
    isWhyModalOpen,
    setIsWhyModalOpen,
    isStressModalOpen,
    setIsStressModalOpen,
    selectedJourneyStage,
    setSelectedJourneyStage,
    handleSendMessage,
    resetSession,
  };
}

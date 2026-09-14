import { useCareRoute } from "../hooks/useCareRoute";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import ChatView from "../components/Chat/ChatView";
import PatientStateView from "../components/PatientState/PatientStateView";
import FullPatientStateView from "../components/PatientState/FullPatientStateView";
import CareRouteView from "../components/CareRoute/CareRouteView";
import PrismView from "../components/Prism/PrismView";
import JourneyTimeline from "../components/Journey/JourneyTimeline";
import WhyChangedModal from "../components/Modals/WhyChangedModal";
import StressTestModal from "../components/Modals/StressTestModal";

export default function Dashboard() {
  const {
    messages,
    patientState,
    newInformation,
    riskLevel,
    navigation,
    safety,
    sources,
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
    handleSendMessage,
    resetSession,
  } = useCareRoute();

  return (
    <div className="app-container">
      {/* Top Header */}
      <Header
        onOpenStressTest={() => setIsStressModalOpen(true)}
        onResetSession={resetSession}
      />

      {/* Main 3-Column Layout */}
      <main className="main-layout">
        {/* Left Column: Navigation Sidebar */}
        <Sidebar activeTab={activeTab} onTabSelect={setActiveTab} />

        {/* Center / Right Columns: Render based on Active Tab */}
        {activeTab === "chat" && (
          <>
            {/* Center Column: Live Patient Conversation */}
            <ChatView
              messages={messages}
              onSendMessage={handleSendMessage}
              loading={loading}
              stateChangeBanner={stateChangeBanner}
              onOpenWhyModal={() => setIsWhyModalOpen(true)}
            />

            {/* Right Column: Patient State & Navigation */}
            <PatientStateView
              patientState={patientState}
              newInformation={newInformation}
              riskLevel={riskLevel}
              navigation={navigation}
              safety={safety}
              sources={sources}
              onOpenWhyModal={() => setIsWhyModalOpen(true)}
              onNavigateToCareRoute={() => setActiveTab("careroute")}
            />
          </>
        )}

        {activeTab === "state" && (
          <FullPatientStateView
            patientState={patientState}
            riskLevel={riskLevel}
            navigation={navigation}
            journeyEvents={journeyEvents}
            sources={sources}
          />
        )}

        {activeTab === "journey" && (
          <div className="prism-view-container">
            <div className="panel-card" style={{ padding: "28px" }}>
              <div className="panel-header">
                <div className="panel-title">
                  <span>🧭</span> PATIENT JOURNEY & EVENT LOGS
                </div>
                <div className="panel-subtitle">Chronological progression of extracted clinical context</div>
              </div>
              <JourneyTimeline
                patientState={patientState}
                riskLevel={riskLevel}
                navigation={navigation}
                journeyEvents={journeyEvents}
              />
            </div>
          </div>
        )}

        {activeTab === "careroute" && (
          <CareRouteView
            patientState={patientState}
            riskLevel={riskLevel}
            navigation={navigation}
            onOpenWhyModal={() => setIsWhyModalOpen(true)}
          />
        )}

        {activeTab === "prism" && <PrismView />}

        {/* Bottom Full-Width Journey Timeline on Chat View */}
        {activeTab === "chat" && (
          <JourneyTimeline
            patientState={patientState}
            riskLevel={riskLevel}
            navigation={navigation}
            journeyEvents={journeyEvents}
          />
        )}
      </main>

      {/* Why Did This Change Modal */}
      <WhyChangedModal
        isOpen={isWhyModalOpen}
        onClose={() => setIsWhyModalOpen(false)}
        whyData={whyChangedData}
      />

      {/* Stress Test Modal */}
      <StressTestModal
        isOpen={isStressModalOpen}
        onClose={() => setIsStressModalOpen(false)}
        onExecuteTurn={handleSendMessage}
        onResetSession={resetSession}
      />
    </div>
  );
}

import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    content = f.read()

# Add smooth scroll ref and quick jump button to socket chat
old_comm_card = """          {/* Direct Paramedic Communication Card */}
          <div className="bg-surface-container rounded-xl p-stack-md flex flex-col gap-2 border border-tertiary/30">"""

new_comm_card = """          {/* Real-time Socket Chat Section */}
          <div id="socket-chat-section" className="scroll-mt-20">
            {incidentData?.incident_id && (
              <LiveEmergencyChat 
                incidentId={incidentData.incident_id}
                senderRole="citizen"
                senderName={citizenInfo?.name || 'Citizen User'}
                targetPhone="+919876543210"
              />
            )}
          </div>

          {/* Direct Paramedic Communication Card */}
          <div className="bg-surface-container rounded-xl p-stack-md flex flex-col gap-2 border border-tertiary/30">"""

if "id=\"socket-chat-section\"" not in content:
    content = content.replace(
        """          {/* Real-time Socket Chat & Direct Call */}
          {incidentData?.incident_id && (
            <LiveEmergencyChat 
              incidentId={incidentData.incident_id}
              senderRole="citizen"
              senderName={citizenInfo?.name || 'Citizen User'}
              targetPhone="+919876543210"
            />
          )}""",
        ""
    )
    content = content.replace(old_comm_card, new_comm_card)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(content)

print("CitizenDashboard.jsx updated to place LiveEmergencyChat right above communication card")

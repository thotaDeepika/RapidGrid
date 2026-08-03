import sys

# 1. Update CitizenDashboard.jsx
cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

if "LiveEmergencyChat" not in c_content:
    c_content = c_content.replace(
        "import MapOverlay",
        "import LiveEmergencyChat from '../components/LiveEmergencyChat';\nimport MapOverlay"
    )
    if "import LiveEmergencyChat" not in c_content:
        c_content = "import LiveEmergencyChat from '../components/LiveEmergencyChat';\n" + c_content

# Add LiveEmergencyChat component below responder card in Citizen tracking view
cit_chat_mount = """
          {/* Real-time Socket Chat & Direct Call */}
          {incidentData?.incident_id && (
            <LiveEmergencyChat 
              incidentId={incidentData.incident_id}
              senderRole="citizen"
              senderName={citizenInfo?.name || 'Citizen User'}
              targetPhone="+919876543210"
            />
          )}"""

if "LiveEmergencyChat" in c_content and "<LiveEmergencyChat" not in c_content:
    c_content = c_content.replace(
        "{/* Direct Paramedic Communication Card */}",
        cit_chat_mount + "\n\n          {/* Direct Paramedic Communication Card */}"
    )

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)


# 2. Update DriverDashboard.jsx
drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

if "LiveEmergencyChat" not in d_content:
    d_content = "import LiveEmergencyChat from '../components/LiveEmergencyChat';\n" + d_content

drv_chat_mount = """
        {/* Real-time Socket Emergency Chat */}
        {selectedIncident?.incident_id && (
          <LiveEmergencyChat
            incidentId={selectedIncident.incident_id}
            senderRole="driver"
            senderName="Paramedic Unit AMB-04"
            targetPhone={selectedIncident.citizen_phone || '+919876543210'}
          />
        )}"""

if "<LiveEmergencyChat" not in d_content:
    d_content = d_content.replace(
        "{/* Patient Report Card */}",
        drv_chat_mount + "\n\n        {/* Patient Report Card */}"
    )

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)


# 3. Update HospitalDashboard.jsx
hosp_file = "src/views/HospitalDashboard.jsx"
with open(hosp_file, "r", encoding="utf-8") as f:
    h_content = f.read()

if "LiveEmergencyChat" not in h_content:
    h_content = "import LiveEmergencyChat from '../components/LiveEmergencyChat';\n" + h_content

hosp_chat_mount = """
                    {/* Live ER Socket Chat */}
                    <div className="mt-3">
                      <LiveEmergencyChat
                        incidentId={inc.incident_id}
                        senderRole="hospital"
                        senderName={hospitalInfo?.name || 'Hospital ER Desk'}
                        targetPhone="+919876543210"
                      />
                    </div>"""

if "<LiveEmergencyChat" not in h_content:
    h_content = h_content.replace(
        "</div>\n                </div>\n              );\n            })}",
        hosp_chat_mount + "\n</div>\n                </div>\n              );\n            })}"
    )

with open(hosp_file, "w", encoding="utf-8") as f:
    f.write(h_content)

print("Mounted LiveEmergencyChat into Citizen, Driver, and Hospital dashboards")

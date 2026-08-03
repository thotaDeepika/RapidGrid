import sys

drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    content = f.read()

# Remove squished chat from narrow right column
old_right_col = """        {/* Real-time Socket Emergency Chat */}
        {selectedIncident?.incident_id && (
          <LiveEmergencyChat
            incidentId={selectedIncident.incident_id}
            senderRole="driver"
            senderName="Paramedic Unit AMB-04"
            targetPhone={selectedIncident.citizen_phone || '+919876543210'}
          />
        )}"""

content = content.replace(old_right_col, "")

# Add LiveEmergencyChat as a full-width section below the main navigation grid
new_bottom_chat = """
      {/* Real-time Socket Emergency Chat - Full Width Expanded */}
      {selectedIncident?.incident_id && (
        <div className="w-full">
          <LiveEmergencyChat
            incidentId={selectedIncident.incident_id}
            senderRole="driver"
            senderName="Paramedic Unit AMB-04"
            targetPhone={selectedIncident.citizen_phone || '+919876543210'}
          />
        </div>
      )}"""

content = content.replace(
    '</div>\n      </div>\n\n      {/* Right: Hospital & Patient Details Panel */}',
    '</div>\n      </div>\n\n      {/* Right: Hospital & Patient Details Panel */}'
)

content = content.replace(
    '</div>\n    </div>\n  );\n}',
    new_bottom_chat + '\n    </div>\n  );\n}'
)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(content)

print("DriverDashboard.jsx updated to place LiveEmergencyChat in full-width expanded layout")

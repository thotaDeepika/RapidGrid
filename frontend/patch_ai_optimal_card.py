import sys

drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

# Replace emoji chars and add AI Optimal Route badge card above dropdown
old_dropdown_block = """            {/* Interactive Hospital Destination Selector & Live Rerouting */}
            <div className="space-y-1.5">
              <div className="text-lg font-bold text-on-surface">
                {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Commercial Building Fire, Bellary Rd' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Incident Site, MG Road' : (selectedIncident?.citizen_view?.hospital_name || selectedIncident.hospital_name)}
              </div>
              <label className="text-[10px] font-mono text-tertiary font-bold block uppercase">
                Change Hospital Destination (Live Uber-Style Reroute):
              </label>"""

new_dropdown_block = """            {/* AI Optimal Hospital Card + Optional Manual Reroute */}
            <div className="space-y-2">
              <div className="bg-tertiary/10 p-3 rounded-xl border border-tertiary/30 space-y-1">
                <div className="text-[10px] font-mono text-tertiary font-bold uppercase flex items-center gap-1">
                  <span className="material-symbols-outlined text-[14px]">auto_awesome</span>
                  AI OPTIMAL ROUTE (SHORTEST, FASTEST & BEDS READY):
                </div>
                <div className="text-sm font-bold text-on-surface font-mono">
                  {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Commercial Building Fire, Bellary Rd' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Incident Site, MG Road' : (selectedIncident?.citizen_view?.hospital_name || selectedIncident.hospital_name)}
                </div>
              </div>

              <label className="text-[10px] font-mono text-on-surface-variant font-bold block uppercase pt-1">
                Manual Driver Override (Optional Reroute):
              </label>"""

d_content = d_content.replace(old_dropdown_block, new_dropdown_block)

# Clean non-UTF8 emojis in button labels
d_content = d_content.replace("?? MARK ARRIVED AT PATIENT SPOT", "MARK ARRIVED AT PATIENT SPOT")
d_content = d_content.replace("?? MARK ARRIVED AT DESTINATION HOSPITAL", "MARK ARRIVED AT DESTINATION HOSPITAL")

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("DriverDashboard.jsx updated with prominent AI Optimal Route card and clean driver overrides")

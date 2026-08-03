import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# Enhance status subtitle and multi-vehicle status badge list
old_status_p = """                  <p className="font-status-code text-status-code text-primary">
                    {incidentData?.status === 'completed' 
                      ? ((citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Control Active on Scene' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Scene Secured by Police' : 'Arrived at Hospital ER') 
                      : incidentData?.status === 'dispatched' ? 'Emergency Driver En Route to Site' : 'Awaiting Dispatcher'}
                  </p>"""

new_status_p = """                  <p className="font-status-code text-status-code text-primary font-mono font-bold flex items-center gap-1.5 mt-0.5">
                    <span className="w-2 h-2 rounded-full bg-primary animate-ping"></span>
                    {incidentData?.status === 'completed' 
                      ? ((citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE CONTROL ACTIVE ON SCENE' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'SCENE SECURED BY POLICE' : 'ARRIVED AT HOSPITAL ER') 
                      : incidentData?.status === 'dispatched' || incidentData?.driver_claimed ? 'FIRST RESPONDER EN ROUTE TO SITE' : 'AI DISPATCH APPROVED - UNIT EN ROUTE'}
                  </p>"""

c_content = c_content.replace(old_status_p, new_status_p)

# Add Multi-Vehicle Standby Status Cards below emergency type badge
multi_vehicle_badge = """            {/* Dual Multi-Vehicle Dispatch Status Badges */}
            <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/20 mb-3 space-y-2">
              <span className="text-[10px] font-mono font-bold text-tertiary uppercase tracking-wider block">Active Field Units Dispatched</span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <div className="bg-surface-container p-2.5 rounded-lg border border-primary/30 flex items-center justify-between">
                  <div className="flex items-center gap-2 text-xs font-mono font-bold">
                    <span className="text-primary font-black">
                      {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? '?? FIRE-UNIT-09' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? '?? POLICE-UNIT-02' : '?? AMB-UNIT-04'}
                    </span>
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary/20 text-primary font-bold">
                    {incidentData?.status === 'completed' ? 'ARRIVED' : 'EN ROUTE'}
                  </span>
                </div>

                <div className="bg-surface-container p-2.5 rounded-lg border border-tertiary/30 flex items-center justify-between">
                  <div className="flex items-center gap-2 text-xs font-mono font-bold">
                    <span className="text-tertiary font-black">?? MEDICAL AMBULANCE</span>
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-tertiary/20 text-tertiary font-bold">
                    {incidentData?.status === 'completed' ? 'MEDICAL STANDBY' : 'STANDBY READY'}
                  </span>
                </div>
              </div>
            </div>"""

if "Active Field Units Dispatched" not in c_content:
    c_content = c_content.replace(
        "{/* Emergency type + severity */}",
        multi_vehicle_badge + "\n\n            {/* Emergency type + severity */}"
    )

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("CitizenDashboard.jsx updated with multi-vehicle status cards and clean dispatch statuses")

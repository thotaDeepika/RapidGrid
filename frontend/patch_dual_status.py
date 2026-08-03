import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# Replace non-UTF8 icons and enhance dual status section
old_dual_section = """            {/* Dual Multi-Vehicle Dispatch Status Badges */}
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

new_dual_section = """            {/* Multi-Vehicle Dual Dispatch Live Status Cards */}
            <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/30 mb-4 space-y-2">
              <div className="flex justify-between items-center text-[10px] font-mono font-bold uppercase tracking-wider text-tertiary">
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
                  Active Dispatched Field Units (2 Units Assigned)
                </span>
                <span className="text-on-surface-variant font-normal">Realtime Telemetry</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                {/* Primary Response Unit (Fire Engine / Police / Ambulance) */}
                <div className="bg-surface-container p-3 rounded-xl border border-primary/40 space-y-1.5 shadow-md">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-mono font-black text-primary uppercase flex items-center gap-1.5">
                      <span className="material-symbols-outlined text-[16px]">
                        {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'local_fire_department' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'local_police' : 'ambulance'}
                      </span>
                      {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE-UNIT-09 (Fire Engine)' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'POLICE-UNIT-02 (Police)' : 'AMB-UNIT-04 (Ambulance)'}
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary/20 text-primary font-bold">
                      {incidentData?.status === 'completed' ? 'ARRIVED ON SITE' : 'EN ROUTE'}
                    </span>
                  </div>
                  <div className="text-[11px] text-on-surface-variant font-mono">
                    Target: <strong className="text-on-surface font-semibold">
                      {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Emergency Scene' : 'Patient Incident Scene'}
                    </strong>
                  </div>
                  <div className="text-[10px] text-primary font-mono font-bold">
                    ETA: {incidentData?.status === 'completed' ? '0m (On Scene)' : `${etaMinutes} mins`}
                  </div>
                </div>

                {/* Secondary Medical Ambulance Unit (Backing up Fire/Police) */}
                <div className="bg-surface-container p-3 rounded-xl border border-tertiary/40 space-y-1.5 shadow-md">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-mono font-black text-tertiary uppercase flex items-center gap-1.5">
                      <span className="material-symbols-outlined text-[16px]">medical_services</span>
                      AMB-UNIT-04 (Medical Ambulance)
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-tertiary/20 text-tertiary font-bold">
                      {incidentData?.status === 'completed' ? 'ON SITE STANDBY' : 'EN ROUTE (BACKUP)'}
                    </span>
                  </div>
                  <div className="text-[11px] text-on-surface-variant font-mono">
                    Target: <strong className="text-on-surface font-semibold">{hospitalName}</strong>
                  </div>
                  <div className="text-[10px] text-tertiary font-mono font-bold">
                    ETA: {incidentData?.status === 'completed' ? '0m (Bed Reserved)' : `${Math.max(1, etaMinutes - 2)} mins (ER Standby)`}
                  </div>
                </div>
              </div>
            </div>"""

c_content = c_content.replace(old_dual_section, new_dual_section)

# Update headline when multiple vehicles are dispatched
c_content = c_content.replace(
    "`${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol Unit' : 'Ambulance Unit'} En Route`",
    "`${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine & Medical Ambulance' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol & Medical Unit' : 'Medical Ambulance Unit'} En Route`"
)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("CitizenDashboard.jsx updated with dual Fire Engine & Ambulance live status cards")

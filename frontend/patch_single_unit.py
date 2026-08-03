import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# Replace multi-unit card with single dedicated unit card
old_dual_section = """            {/* Multi-Vehicle Dual Dispatch Live Status Cards */}
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

new_single_section = """            {/* Single Dedicated Emergency Unit Status Card */}
            <div className="bg-surface-container-low p-3.5 rounded-xl border border-outline-variant/30 mb-4 space-y-2">
              <div className="flex justify-between items-center text-[10px] font-mono font-bold uppercase tracking-wider text-tertiary">
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
                  Assigned Emergency Field Unit
                </span>
                <span className="text-on-surface-variant font-normal">Realtime GPS Telemetry</span>
              </div>

              <div className="bg-surface-container p-3.5 rounded-xl border border-primary/40 space-y-2 shadow-md">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-mono font-black text-primary uppercase flex items-center gap-2">
                    <span className="material-symbols-outlined text-[20px]">
                      {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'local_fire_department' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'local_police' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'helicopter' : 'ambulance'}
                    </span>
                    {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE-UNIT-09 (Fire Engine Rescue)' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'POLICE-UNIT-02 (Police Patrol)' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'RESCUE-UNIT-01 (Disaster Rescue)' : 'AMB-UNIT-04 (Medical Ambulance)'}
                  </span>
                  <span className="text-xs font-mono px-3 py-1 rounded-full bg-primary/20 text-primary font-bold">
                    {incidentData?.status === 'completed' ? 'ARRIVED ON SITE' : 'EN ROUTE'}
                  </span>
                </div>

                <div className="flex justify-between items-center pt-1 text-xs font-mono">
                  <span className="text-on-surface-variant">
                    Target Location: <strong className="text-on-surface font-semibold">
                      {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Emergency Structure, Bellary Road' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Incident Scene, MG Road' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Hazard Zone 4' : hospitalName}
                    </strong>
                  </span>
                  <span className="text-primary font-bold">
                    ETA: {incidentData?.status === 'completed' ? '0m (Arrived)' : `${etaMinutes} mins`}
                  </span>
                </div>
              </div>
            </div>"""

c_content = c_content.replace(old_dual_section, new_single_section)

# Update headline to match single dedicated vehicle
c_content = c_content.replace(
    "`${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine & Medical Ambulance' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol & Medical Unit' : 'Medical Ambulance Unit'} En Route`",
    "`${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance Unit'} En Route`"
)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("CitizenDashboard.jsx updated to render single dedicated vehicle for requested emergency service")

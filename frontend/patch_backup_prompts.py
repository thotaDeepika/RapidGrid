import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# 1. Add includeAmbulanceBackup state
if "includeAmbulanceBackup" not in c_content:
    c_content = c_content.replace(
        "const [selectedVehicle, setSelectedVehicle] = useState('Ambulance');",
        "const [selectedVehicle, setSelectedVehicle] = useState('Ambulance');\n  const [includeAmbulanceBackup, setIncludeAmbulanceBackup] = useState(false);"
    )

# 2. Update handleSOSTrigger to include backup in payload
c_content = c_content.replace(
    "vehicle_required: selectedVehicle,",
    "vehicle_required: selectedVehicle,\n      include_ambulance_backup: includeAmbulanceBackup,"
)

# 3. Add dynamic interactive backup prompt under vehicle selector
backup_prompt_ui = """            {/* Dynamic Multi-Vehicle Backup Prompt based on Emergency Service */}
            <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/30 text-xs font-mono space-y-2">
              {selectedVehicle === 'Ambulance' && (
                <div className="flex items-center gap-2 text-tertiary font-bold">
                  <span className="material-symbols-outlined text-[18px]">medical_services</span>
                  <span>Direct Medical Ambulance Dispatch (Patient Hospital Transport)</span>
                </div>
              )}

              {selectedVehicle === 'Fire Engine' && (
                <label className="flex items-center gap-2 cursor-pointer text-on-surface hover:text-primary transition-colors">
                  <input
                    type="checkbox"
                    checked={includeAmbulanceBackup}
                    onChange={(e) => setIncludeAmbulanceBackup(e.target.checked)}
                    className="w-4 h-4 rounded border-outline-variant text-primary focus:ring-primary accent-primary"
                  />
                  <span className="font-bold">Also Request Medical Ambulance Standby (For Burn/Injury Backup)</span>
                </label>
              )}

              {selectedVehicle === 'Police Cruiser' && (
                <label className="flex items-center gap-2 cursor-pointer text-on-surface hover:text-secondary transition-colors">
                  <input
                    type="checkbox"
                    checked={includeAmbulanceBackup}
                    onChange={(e) => setIncludeAmbulanceBackup(e.target.checked)}
                    className="w-4 h-4 rounded border-outline-variant text-secondary focus:ring-secondary accent-secondary"
                  />
                  <span className="font-bold">Also Request Medical Ambulance Backup (For Collision/Victim Injuries)</span>
                </label>
              )}

              {selectedVehicle === 'Disaster Rescue' && (
                <label className="flex items-center gap-2 cursor-pointer text-on-surface hover:text-tertiary transition-colors">
                  <input
                    type="checkbox"
                    checked={includeAmbulanceBackup}
                    onChange={(e) => setIncludeAmbulanceBackup(e.target.checked)}
                    className="w-4 h-4 rounded border-outline-variant text-tertiary focus:ring-tertiary accent-tertiary"
                  />
                  <span className="font-bold">Also Request Medical Ambulance Unit (For Disaster Evacuation Backup)</span>
                </label>
              )}
            </div>"""

c_content = c_content.replace(
    "          {/* Location display */}",
    backup_prompt_ui + "\n\n          {/* Location display */}"
)

# 4. Render dual vs single cards on tracking screen based on include_ambulance_backup
old_tracking_cards = """            {/* Single Dedicated Emergency Unit Status Card */}
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

new_tracking_cards = """            {/* Dynamic Single vs Dual Emergency Unit Status Cards */}
            <div className="bg-surface-container-low p-3.5 rounded-xl border border-outline-variant/30 mb-4 space-y-2">
              <div className="flex justify-between items-center text-[10px] font-mono font-bold uppercase tracking-wider text-tertiary">
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
                  {(citizenView?.include_ambulance_backup || incidentData?.include_ambulance_backup) ? 'Assigned Field Units (Primary + Medical Standby)' : 'Assigned Emergency Field Unit'}
                </span>
                <span className="text-on-surface-variant font-normal">Realtime GPS Telemetry</span>
              </div>

              <div className={`grid grid-cols-1 ${(citizenView?.include_ambulance_backup || incidentData?.include_ambulance_backup) ? 'sm:grid-cols-2' : ''} gap-3 pt-1`}>
                {/* Primary Dispatched Unit */}
                <div className="bg-surface-container p-3 rounded-xl border border-primary/40 space-y-1.5 shadow-md">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-mono font-black text-primary uppercase flex items-center gap-1.5">
                      <span className="material-symbols-outlined text-[16px]">
                        {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'local_fire_department' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'local_police' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'helicopter' : 'ambulance'}
                      </span>
                      {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE-UNIT-09 (Fire Engine)' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'POLICE-UNIT-02 (Police)' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'RESCUE-UNIT-01 (Disaster Rescue)' : 'AMB-UNIT-04 (Medical Ambulance)'}
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary/20 text-primary font-bold">
                      {incidentData?.status === 'completed' ? 'ARRIVED ON SITE' : 'EN ROUTE'}
                    </span>
                  </div>
                  <div className="text-[11px] text-on-surface-variant font-mono">
                    Target: <strong className="text-on-surface font-semibold">
                      {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Emergency Scene' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Incident Scene' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Hazard Zone 4' : hospitalName}
                    </strong>
                  </div>
                  <div className="text-[10px] text-primary font-mono font-bold">
                    ETA: {incidentData?.status === 'completed' ? '0m (Arrived)' : `${etaMinutes} mins`}
                  </div>
                </div>

                {/* Optional Medical Ambulance Backup (Rendered ONLY if requested) */}
                {(citizenView?.include_ambulance_backup || incidentData?.include_ambulance_backup) && (
                  <div className="bg-surface-container p-3 rounded-xl border border-tertiary/40 space-y-1.5 shadow-md">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-mono font-black text-tertiary uppercase flex items-center gap-1.5">
                        <span className="material-symbols-outlined text-[16px]">medical_services</span>
                        AMB-UNIT-04 (Medical Ambulance Backup)
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
                )}
              </div>
            </div>"""

c_content = c_content.replace(old_tracking_cards, new_tracking_cards)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("CitizenDashboard.jsx updated with interactive ambulance backup prompts")

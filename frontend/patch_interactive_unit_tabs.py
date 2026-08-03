import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# 1. Add activeTrackingUnit state
if "activeTrackingUnit" not in c_content:
    c_content = c_content.replace(
        "const [includeAmbulanceBackup, setIncludeAmbulanceBackup] = useState(false);",
        "const [includeAmbulanceBackup, setIncludeAmbulanceBackup] = useState(false);\n  const [activeTrackingUnit, setActiveTrackingUnit] = useState('primary'); // 'primary' | 'ambulance'"
    )

# 2. Make vehicle cards interactive buttons with click handlers
old_cards_code = """                {/* Primary Dispatched Unit */}
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

                {/* Optional Medical Ambulance Backup (Rendered if requested OR triggerable live) */}
                {(citizenView?.include_ambulance_backup || incidentData?.include_ambulance_backup) ? (
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
                )"""

new_cards_code = """                {/* Primary Dispatched Unit (Interactive Click Tab) */}
                <div 
                  onClick={() => setActiveTrackingUnit('primary')}
                  className={`bg-surface-container p-3 rounded-xl border cursor-pointer transition-all space-y-1.5 shadow-md ${
                    activeTrackingUnit === 'primary' 
                      ? 'border-primary ring-2 ring-primary/60 bg-surface-container-highest/50' 
                      : 'border-primary/30 hover:border-primary/70'
                  }`}
                >
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
                  <div className="text-[10px] text-primary font-mono font-bold flex justify-between items-center">
                    <span>ETA: {incidentData?.status === 'completed' ? '0m (Arrived)' : `${etaMinutes} mins`}</span>
                    <span className="text-[9px] text-tertiary font-bold uppercase underline">Click to inspect</span>
                  </div>
                </div>

                {/* Optional Medical Ambulance Backup (Interactive Click Tab) */}
                {(citizenView?.include_ambulance_backup || incidentData?.include_ambulance_backup) ? (
                  <div 
                    onClick={() => setActiveTrackingUnit('ambulance')}
                    className={`bg-surface-container p-3 rounded-xl border cursor-pointer transition-all space-y-1.5 shadow-md ${
                      activeTrackingUnit === 'ambulance' 
                        ? 'border-tertiary ring-2 ring-tertiary/60 bg-surface-container-highest/50' 
                        : 'border-tertiary/30 hover:border-tertiary/70'
                    }`}
                  >
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
                    <div className="text-[10px] text-tertiary font-mono font-bold flex justify-between items-center">
                      <span>ETA: {incidentData?.status === 'completed' ? '0m (Bed Reserved)' : `${Math.max(1, etaMinutes - 2)} mins (ER Standby)`}</span>
                      <span className="text-[9px] text-tertiary font-bold uppercase underline">Click to inspect</span>
                    </div>
                  </div>
                )"""

c_content = c_content.replace(old_cards_code, new_cards_code)

# 3. Dynamic headline and details based on activeTrackingUnit
old_headline_jsx = """                  <h2 className="font-headline-md text-headline-md text-on-surface">
                    {incidentData?.status === 'completed' 
                      ? `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance'} Arrived - On Site` 
                      : `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance Unit'} En Route`}
                  </h2>"""

new_headline_jsx = """                  <h2 className="font-headline-md text-headline-md text-on-surface">
                    {activeTrackingUnit === 'ambulance'
                      ? (incidentData?.status === 'completed' ? 'Medical Ambulance Arrived - On Site' : 'Medical Ambulance Unit En Route')
                      : (incidentData?.status === 'completed' 
                          ? `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance'} Arrived - On Site` 
                          : `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance Unit'} En Route`)}
                  </h2>"""

c_content = c_content.replace(old_headline_jsx, new_headline_jsx)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("CitizenDashboard.jsx updated with interactive unit selection tabs")

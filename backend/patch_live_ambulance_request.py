import sys

# 1. Update backend/routers/incident.py to add request_ambulance endpoint
inc_py = "routers/incident.py"
with open(inc_py, "r", encoding="utf-8") as f:
    content = f.read()

req_amb_endpoint = """
@router.post("/{incident_id}/request_ambulance")
async def request_ambulance_backup(incident_id: str):
    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == incident_id:
            inc["include_ambulance_backup"] = True
            if "citizen_view" in inc:
                inc["citizen_view"]["include_ambulance_backup"] = True
            save_db()
            return {"status": "ambulance_requested", "incident_id": incident_id}
    raise HTTPException(status_code=404, detail="Incident not found")
"""

if "request_ambulance_backup" not in content:
    content += req_amb_endpoint
    with open(inc_py, "w", encoding="utf-8") as f:
        f.write(content)


# 2. Update CitizenDashboard.jsx to add "+ REQUEST MEDICAL AMBULANCE BACKUP" button
cit_file = "../frontend/src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

old_backup_render = """                {/* Optional Medical Ambulance Backup (Rendered ONLY if requested) */}
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
                )}"""

new_backup_render = """                {/* Optional Medical Ambulance Backup (Rendered if requested OR triggerable live) */}
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
                ) : (
                  <div className="bg-surface-container/60 p-3 rounded-xl border border-dashed border-tertiary/40 flex flex-col items-center justify-center gap-1 text-center">
                    <span className="text-xs font-mono font-bold text-on-surface-variant">Need Medical Backup for Injury / Burn?</span>
                    <button
                      onClick={async () => {
                        if (!incidentData?.incident_id) return;
                        try {
                          await fetch(`/api/incidents/${incidentData.incident_id}/request_ambulance`, { method: 'POST' });
                          setIncidentData(prev => ({ ...prev, include_ambulance_backup: true }));
                          setCitizenView(prev => ({ ...prev, include_ambulance_backup: true }));
                        } catch (err) {}
                      }}
                      className="px-3 py-1.5 bg-tertiary/20 text-tertiary hover:bg-tertiary/30 rounded-xl text-xs font-mono font-bold border border-tertiary/40 flex items-center gap-1 transition-all"
                    >
                      <span className="material-symbols-outlined text-[16px]">medical_services</span>
                      + DISPATCH AMBULANCE BACKUP NOW
                    </button>
                  </div>
                )}"""

c_content = c_content.replace(old_backup_render, new_backup_render)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("Added + DISPATCH AMBULANCE BACKUP NOW button to CitizenDashboard.jsx and backend endpoint")

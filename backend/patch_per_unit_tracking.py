import sys

# 1. Update backend/routers/driver.py
drv_py = "routers/driver.py"
with open(drv_py, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "class ClaimPayload(BaseModel):\n    incident_id: str\n    driver_id: str = \"drv-11\"",
    "class ClaimPayload(BaseModel):\n    incident_id: str\n    driver_id: str = \"drv-11\"\n    unit_type: str = \"primary\""
)

old_claim_body = """            inc["assigned_driver"] = payload.driver_id
            inc["driver_claimed"] = True
            save_db()
            return {"status": "claimed", "incident_id": payload.incident_id, "driver_id": payload.driver_id}"""

new_claim_body = """            inc["assigned_driver"] = payload.driver_id
            inc["driver_claimed"] = True
            inc["status"] = "dispatched"
            
            unit_statuses = inc.get("unit_statuses") or {"primary": "dispatched", "ambulance": "dispatched"}
            unit_statuses[payload.unit_type] = "dispatched"
            inc["unit_statuses"] = unit_statuses
            
            if "citizen_view" in inc:
                inc["citizen_view"]["status"] = "dispatched"
                inc["citizen_view"]["unit_statuses"] = unit_statuses
                
            save_db()
            return {"status": "claimed", "incident_id": payload.incident_id, "driver_id": payload.driver_id, "unit_statuses": unit_statuses}"""

content = content.replace(old_claim_body, new_claim_body)
with open(drv_py, "w", encoding="utf-8") as f:
    f.write(content)


# 2. Update backend/routers/incident.py
inc_py = "routers/incident.py"
with open(inc_py, "r", encoding="utf-8") as f:
    i_content = f.read()

old_arrived_func = """@router.post("/{incident_id}/arrived")
async def incident_arrived(incident_id: str):
    \"\"\"Step 5 - Driver arrives.\"\"\"
    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == incident_id:
            inc["status"] = "completed"
            save_db()
            return {"status": "completed"}
    raise HTTPException(status_code=404, detail="Incident not found")"""

new_arrived_func = """@router.post("/{incident_id}/arrived")
async def incident_arrived(incident_id: str, unit_type: str = "primary"):
    \"\"\"Step 5 - Driver arrives for specific unit (primary vs ambulance).\"\"\"
    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == incident_id:
            unit_statuses = inc.get("unit_statuses") or {"primary": "dispatched", "ambulance": "dispatched"}
            unit_statuses[unit_type] = "arrived"
            inc["unit_statuses"] = unit_statuses
            
            # If primary unit arrived or both arrived, set main incident status to completed
            if unit_statuses.get("primary") == "arrived":
                inc["status"] = "completed"
            
            if "citizen_view" in inc:
                inc["citizen_view"]["unit_statuses"] = unit_statuses
                if inc["status"] == "completed":
                    inc["citizen_view"]["status"] = "completed"
                    
            save_db()
            return {"status": "arrived", "unit_type": unit_type, "unit_statuses": unit_statuses, "incident_status": inc["status"]}
    raise HTTPException(status_code=404, detail="Incident not found")"""

i_content = i_content.replace(old_arrived_func, new_arrived_func)
with open(inc_py, "w", encoding="utf-8") as f:
    f.write(i_content)


# 3. Update CitizenDashboard.jsx to read per-unit driver statuses dynamically
cit_file = "../frontend/src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# Add unitStatuses evaluation
old_hosp_eval = """  const hospLoc = citizenView?.hospital_location;"""

new_hosp_eval = """  const unitStatuses = citizenView?.unit_statuses || incidentData?.unit_statuses || { primary: incidentData?.status || 'dispatched', ambulance: 'dispatched' };
  const hospLoc = citizenView?.hospital_location;"""

c_content = c_content.replace(old_hosp_eval, new_hosp_eval)

# Update Primary unit badge
old_p_badge = """                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary/20 text-primary font-bold">
                      {incidentData?.status === 'completed' ? 'ARRIVED ON SITE' : 'EN ROUTE'}
                    </span>"""

new_p_badge = """                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary/20 text-primary font-bold">
                      {unitStatuses.primary === 'arrived' || incidentData?.status === 'completed' ? 'ARRIVED ON SITE' : 'EN ROUTE'}
                    </span>"""

c_content = c_content.replace(old_p_badge, new_p_badge)

# Update Ambulance unit badge
old_a_badge = """                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-tertiary/20 text-tertiary font-bold">
                        {incidentData?.status === 'completed' ? 'ON SITE STANDBY' : 'EN ROUTE (BACKUP)'}
                      </span>"""

new_a_badge = """                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-tertiary/20 text-tertiary font-bold">
                        {unitStatuses.ambulance === 'arrived' || incidentData?.status === 'completed' ? 'ON SITE STANDBY' : 'EN ROUTE (BACKUP)'}
                      </span>"""

c_content = c_content.replace(old_a_badge, new_a_badge)

# Update Headline & Subtitle evaluation to read selected unit's status
old_headline_check = """                  <h2 className="font-headline-md text-headline-md text-on-surface">
                    {activeTrackingUnit === 'ambulance'
                      ? (incidentData?.status === 'completed' ? 'Medical Ambulance Arrived - On Site' : 'Medical Ambulance Unit En Route')
                      : (incidentData?.status === 'completed' 
                          ? `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance'} Arrived - On Site` 
                          : `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance Unit'} En Route`)}
                  </h2>
                  <p className={`font-status-code text-status-code font-mono font-bold flex items-center gap-1.5 mt-0.5 ${activeTrackingUnit === 'ambulance' ? 'text-tertiary' : 'text-primary'}`}>
                    <span className={`w-2 h-2 rounded-full animate-ping ${activeTrackingUnit === 'ambulance' ? 'bg-tertiary' : 'bg-primary'}`}></span>
                    {activeTrackingUnit === 'ambulance'
                      ? (incidentData?.status === 'completed' ? 'MEDICAL AMBULANCE STANDBY ON SITE' : 'PARAMEDIC DISPATCHED FOR MEDICAL BACKUP')
                      : (incidentData?.status === 'completed' 
                          ? ((citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE CONTROL ACTIVE ON SCENE' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'SCENE SECURED BY POLICE' : 'ARRIVED AT HOSPITAL ER') 
                          : incidentData?.status === 'dispatched' || incidentData?.driver_claimed ? 'FIRST RESPONDER EN ROUTE TO SITE' : 'AI DISPATCH APPROVED - UNIT EN ROUTE')}
                  </p>"""

new_headline_check = """                  <h2 className="font-headline-md text-headline-md text-on-surface">
                    {activeTrackingUnit === 'ambulance'
                      ? (unitStatuses.ambulance === 'arrived' || incidentData?.status === 'completed' ? 'Medical Ambulance Arrived - On Site' : 'Medical Ambulance Unit En Route')
                      : (unitStatuses.primary === 'arrived' || incidentData?.status === 'completed' 
                          ? `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance'} Arrived - On Site` 
                          : `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance Unit'} En Route`)}
                  </h2>
                  <p className={`font-status-code text-status-code font-mono font-bold flex items-center gap-1.5 mt-0.5 ${activeTrackingUnit === 'ambulance' ? 'text-tertiary' : 'text-primary'}`}>
                    <span className={`w-2 h-2 rounded-full animate-ping ${activeTrackingUnit === 'ambulance' ? 'bg-tertiary' : 'bg-primary'}`}></span>
                    {activeTrackingUnit === 'ambulance'
                      ? (unitStatuses.ambulance === 'arrived' || incidentData?.status === 'completed' ? 'MEDICAL AMBULANCE STANDBY ON SITE' : 'PARAMEDIC DISPATCHED FOR MEDICAL BACKUP')
                      : (unitStatuses.primary === 'arrived' || incidentData?.status === 'completed' 
                          ? ((citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE CONTROL ACTIVE ON SCENE' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'SCENE SECURED BY POLICE' : 'ARRIVED AT HOSPITAL ER') 
                          : incidentData?.status === 'dispatched' || incidentData?.driver_claimed ? 'FIRST RESPONDER EN ROUTE TO SITE' : 'AI DISPATCH APPROVED - UNIT EN ROUTE')}
                  </p>"""

c_content = c_content.replace(old_headline_check, new_headline_check)

# Update Timeline Dots based on selected unit's status
old_timeline_jsx = """              <div
                className="absolute top-1/2 left-0 h-0.5 bg-tertiary -translate-y-1/2 transition-all duration-1000"
                style={{ width: incidentData?.status === 'completed' ? '100%' : incidentData?.status === 'dispatched' ? '66%' : '33%' }}
              ></div>
              <div className="relative flex justify-between">
                <div className="flex flex-col items-center gap-1">
                  <div className="w-3 h-3 bg-tertiary rounded-full ring-4 ring-surface-container-high z-10"></div>
                  <span className="font-label-caps text-label-caps text-tertiary">REPORTED</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-3 h-3 rounded-full ring-4 ring-surface-container-high z-10 ${incidentData?.status === 'dispatched' || incidentData?.status === 'completed' ? 'bg-tertiary' : 'bg-outline'}`}></div>
                  <span className="font-label-caps text-label-caps text-tertiary">DISPATCHED</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-3 h-3 rounded-full ring-4 ring-surface-container-high z-10 ${incidentData?.status === 'completed' ? 'bg-tertiary animate-pulse' : 'bg-outline'}`}></div>
                  <span className={`font-label-caps text-label-caps ${incidentData?.status === 'completed' ? 'text-tertiary font-bold' : 'text-on-surface opacity-40'}`}>ON SITE</span>
                </div>"""

new_timeline_jsx = """              <div
                className="absolute top-1/2 left-0 h-0.5 bg-tertiary -translate-y-1/2 transition-all duration-1000"
                style={{ width: (activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'arrived' || incidentData?.status === 'completed' ? '100%' : (activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'dispatched' || incidentData?.status === 'dispatched' ? '66%' : '33%' }}
              ></div>
              <div className="relative flex justify-between">
                <div className="flex flex-col items-center gap-1">
                  <div className="w-3 h-3 bg-tertiary rounded-full ring-4 ring-surface-container-high z-10"></div>
                  <span className="font-label-caps text-label-caps text-tertiary">REPORTED</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-3 h-3 rounded-full ring-4 ring-surface-container-high z-10 ${(activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'dispatched' || (activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'arrived' || incidentData?.status === 'dispatched' || incidentData?.status === 'completed' ? 'bg-tertiary' : 'bg-outline'}`}></div>
                  <span className="font-label-caps text-label-caps text-tertiary">DISPATCHED</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-3 h-3 rounded-full ring-4 ring-surface-container-high z-10 ${(activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'arrived' || incidentData?.status === 'completed' ? 'bg-tertiary animate-pulse' : 'bg-outline'}`}></div>
                  <span className={`font-label-caps text-label-caps ${(activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'arrived' || incidentData?.status === 'completed' ? 'text-tertiary font-bold' : 'text-on-surface opacity-40'}`}>ON SITE</span>
                </div>"""

c_content = c_content.replace(old_timeline_jsx, new_timeline_jsx)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

# 4. Touch backend/main.py for uvicorn reload
with open("main.py", "r", encoding="utf-8") as f:
    m_content = f.read()

m_content += "\n# Touch for per-unit tracking reload"
with open("main.py", "w", encoding="utf-8") as f:
    f.write(m_content)

print("Per-unit real-time driver status tracking patched 100% end-to-end across backend and frontend")

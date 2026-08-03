import sys

# 1. Update backend/routers/hospital.py to only show Medical Ambulance cases to Hospital ER
hosp_py = "routers/hospital.py"
with open(hosp_py, "r", encoding="utf-8") as f:
    content = f.read()

old_hosp_loop = """            if matches:
                incoming.append({"""

new_hosp_loop = """            # Fire and Police incidents without hospital transport do not clutter Hospital ER Desk
            veh_req = inc.get("vehicle_required") or "Ambulance"
            if matches and veh_req in ("Ambulance", "Medical"):
                incoming.append({"""

if "veh_req in (\"Ambulance\"" not in content:
    content = content.replace(old_hosp_loop, new_hosp_loop)

with open(hosp_py, "w", encoding="utf-8") as f:
    f.write(content)


# 2. Update CitizenDashboard.jsx for Logical Vehicle Destinations
cit_file = "../frontend/src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

old_cit_headline = """                <div>
                  <h2 className="font-headline-md text-headline-md text-on-surface">
                    {incidentData?.status === 'completed' ? 'Ambulance Arrived - On Site' : 'Ambulance En Route'}
                  </h2>
                  <p className="font-status-code text-status-code text-primary">
                    {incidentData?.status === 'completed' ? 'Arrived at Destination Hospital' : incidentData?.status === 'dispatched' ? 'Driver Assigned - En Route' : 'Awaiting Dispatcher'}
                  </p>
                </div>"""

new_cit_headline = """                <div>
                  <h2 className="font-headline-md text-headline-md text-on-surface">
                    {incidentData?.status === 'completed' 
                      ? `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Unit' : 'Ambulance'} Arrived - On Site` 
                      : `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol Unit' : 'Ambulance Unit'} En Route`}
                  </h2>
                  <p className="font-status-code text-status-code text-primary">
                    {incidentData?.status === 'completed' 
                      ? ((citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Control Active on Scene' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Scene Secured by Police' : 'Arrived at Hospital ER') 
                      : incidentData?.status === 'dispatched' ? 'Emergency Driver En Route to Site' : 'Awaiting Dispatcher'}
                  </p>
                </div>"""

c_content = c_content.replace(old_cit_headline, new_cit_headline)

# Update destination card title in Citizen App
old_dest_card = """          {/* Hospital info */}
          <div className="bg-surface-container rounded-xl p-stack-md flex items-center gap-stack-md">
            <div className="w-10 h-10 bg-secondary-container rounded-xl flex items-center justify-center">
              <span className="material-symbols-outlined text-on-secondary-container" style={{ fontVariationSettings: "'FILL' 1" }}>local_hospital</span>
            </div>
            <div>
              <div className="font-label-caps text-label-caps text-on-surface-variant">DESTINATION HOSPITAL</div>
              <div className="font-headline-md text-headline-md text-on-surface">{hospitalName}</div>"""

new_dest_card = """          {/* Destination info (Hospital vs Fire Scene vs Incident Site) */}
          <div className="bg-surface-container rounded-xl p-stack-md flex items-center gap-stack-md">
            <div className="w-10 h-10 bg-secondary-container rounded-xl flex items-center justify-center">
              <span className="material-symbols-outlined text-on-secondary-container" style={{ fontVariationSettings: "'FILL' 1" }}>
                {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'local_fire_department' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'local_police' : 'local_hospital'}
              </span>
            </div>
            <div>
              <div className="font-label-caps text-label-caps text-on-surface-variant">
                {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE EMERGENCY SCENE' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'POLICE INCIDENT SITE' : 'DESTINATION HOSPITAL'}
              </div>
              <div className="font-headline-md text-headline-md text-on-surface">
                {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Incident Structure, Bellary Road' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Incident Site, MG Road' : hospitalName}
              </div>"""

c_content = c_content.replace(old_dest_card, new_dest_card)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)


# 3. Update DriverDashboard.jsx for Logical Vehicle Destination Card & Action Button
drv_file = "../frontend/src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

# Update Arrived button text based on vehicle_required
old_arrived_btn = """            <CheckCircle2 size={24} /> MARK AS ARRIVED AT DESTINATION"""

new_arrived_btn = """            <CheckCircle2 size={24} /> {selectedIncident?.vehicle_required === 'Fire Engine' ? 'MARK AS ARRIVED AT FIRE SCENE' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'MARK AS ARRIVED ON SCENE' : 'MARK AS ARRIVED AT DESTINATION HOSPITAL'}"""

d_content = d_content.replace(old_arrived_btn, new_arrived_btn)

# Update Destination Card in Driver Navigation
old_drv_hosp_card = """          <div className="bg-surface-container p-5 rounded-2xl border border-outline-variant/20 space-y-3">
            <h3 className="font-bold text-xs uppercase text-on-surface-variant tracking-wider flex items-center gap-2">
              <MapPin size={16} className="text-secondary" /> Destination Hospital
            </h3>
            <div className="text-lg font-bold text-on-surface">{selectedIncident.hospital_name}</div>"""

new_drv_hosp_card = """          <div className="bg-surface-container p-5 rounded-2xl border border-outline-variant/20 space-y-3">
            <h3 className="font-bold text-xs uppercase text-on-surface-variant tracking-wider flex items-center gap-2">
              <MapPin size={16} className="text-secondary" /> {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Fire Emergency Target' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Police Incident Scene' : 'Destination Hospital'}
            </h3>
            <div className="text-lg font-bold text-on-surface">
              {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Commercial Building Fire, Bellary Rd' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Incident Site, MG Road' : selectedIncident.hospital_name}
            </div>"""

d_content = d_content.replace(old_drv_hosp_card, new_drv_hosp_card)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("Logical emergency vehicle routing patched across Citizen, Driver, and Hospital apps")

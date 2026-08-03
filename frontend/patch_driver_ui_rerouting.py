import sys

drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

# 1. Add driverStage state
d_content = d_content.replace(
    "const [driverVehicleFilter, setDriverVehicleFilter] = useState('All');",
    "const [driverVehicleFilter, setDriverVehicleFilter] = useState('All');\n  const [driverStage, setDriverStage] = useState('pickup'); // 'pickup' | 'hospital'"
)

# 2. Update navigation view header and controls
old_nav_header = """            <div className="flex items-center gap-3">
              <div className="p-3 bg-primary/20 text-primary rounded-xl animate-pulse">
                <Navigation size={24} />
              </div>
              <div>
                <span className="text-xs font-label-caps text-primary uppercase font-bold tracking-wider">EN ROUTE TO EMERGENCY</span>
                <h2 className="font-mono text-xl font-bold text-on-surface">{selectedIncident.incident_id}</h2>
              </div>
            </div>"""

new_nav_header = """            <div className="flex items-center gap-3">
              <div className="p-3 bg-primary/20 text-primary rounded-xl animate-pulse">
                <Navigation size={24} />
              </div>
              <div>
                <span className="text-xs font-label-caps text-primary uppercase font-bold tracking-wider">
                  {driverStage === 'pickup' ? 'STAGE 1: EN ROUTE TO PATIENT PICKUP SPOT' : 'STAGE 2: PATIENT PICKED UP - EN ROUTE TO HOSPITAL'}
                </span>
                <h2 className="font-mono text-xl font-bold text-on-surface">{selectedIncident.incident_id}</h2>
              </div>
            </div>"""

d_content = d_content.replace(old_nav_header, new_nav_header)

# 3. Update action buttons (Mark Arrived Pickup vs Mark Arrived Hospital)
old_arrived_buttons = """          <div className="flex gap-4">
            <button 
              onClick={() => setIsNavigating(false)}
              className="px-4 py-4 bg-surface-container-highest text-on-surface rounded-xl font-semibold text-xs hover:bg-surface-variant"
            >
              Back to Queue
            </button>
            <button
              onClick={handleArrived}
              className="flex-1 bg-tertiary text-on-tertiary font-bold text-lg py-4 rounded-xl flex items-center justify-center gap-2 shadow-xl hover:bg-tertiary/90 transition-all active:scale-[0.98]"
            >
              <CheckCircle2 size={24} /> {selectedIncident?.vehicle_required === 'Fire Engine' ? 'MARK AS ARRIVED AT FIRE SCENE' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'MARK AS ARRIVED ON SCENE' : 'MARK AS ARRIVED AT DESTINATION HOSPITAL'}
            </button>
          </div>"""

new_arrived_buttons = """          <div className="flex gap-4">
            <button 
              onClick={() => setIsNavigating(false)}
              className="px-4 py-4 bg-surface-container-highest text-on-surface rounded-xl font-semibold text-xs hover:bg-surface-variant"
            >
              Back to Queue
            </button>
            {driverStage === 'pickup' ? (
              <button
                onClick={async () => {
                  try {
                    const res = await fetch('/api/driver/arrived_pickup', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ incident_id: selectedIncident.incident_id, driver_id: 'drv-11' })
                    });
                    const data = await res.json();
                    setDriverStage('hospital');
                    if (data.citizen_view) {
                      setSelectedIncident(prev => ({ ...prev, citizen_view: data.citizen_view, route_coordinates: data.citizen_view.route_coordinates }));
                    }
                  } catch (err) {}
                }}
                className="flex-1 bg-primary text-on-primary font-bold text-lg py-4 rounded-xl flex items-center justify-center gap-2 shadow-xl hover:bg-primary/90 transition-all active:scale-[0.98]"
              >
                <CheckCircle2 size={24} /> ?? MARK ARRIVED AT PATIENT SPOT
              </button>
            ) : (
              <button
                onClick={handleArrived}
                className="flex-1 bg-tertiary text-on-tertiary font-bold text-lg py-4 rounded-xl flex items-center justify-center gap-2 shadow-xl hover:bg-tertiary/90 transition-all active:scale-[0.98]"
              >
                <CheckCircle2 size={24} /> {selectedIncident?.vehicle_required === 'Fire Engine' ? 'MARK AS ARRIVED AT FIRE SCENE' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'MARK AS ARRIVED ON SCENE' : '?? MARK ARRIVED AT DESTINATION HOSPITAL'}
              </button>
            )}
          </div>"""

d_content = d_content.replace(old_arrived_buttons, new_arrived_buttons)

# 4. Add Hospital Change Dropdown Selector on Driver Panel
old_hospital_panel = """          <div className="bg-surface-container p-5 rounded-2xl border border-outline-variant/20 space-y-3">
            <h3 className="font-bold text-xs uppercase text-on-surface-variant tracking-wider flex items-center gap-2">
              <MapPin size={16} className="text-secondary" /> {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Fire Emergency Target' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Police Incident Scene' : 'Destination Hospital'}
            </h3>
            <div className="text-lg font-bold text-on-surface">
              {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Commercial Building Fire, Bellary Rd' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Incident Site, MG Road' : selectedIncident.hospital_name}
            </div>"""

new_hospital_panel = """          <div className="bg-surface-container p-5 rounded-2xl border border-outline-variant/20 space-y-3">
            <h3 className="font-bold text-xs uppercase text-on-surface-variant tracking-wider flex items-center gap-2">
              <MapPin size={16} className="text-secondary" /> {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Fire Emergency Target' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Police Incident Scene' : 'Destination Hospital'}
            </h3>
            
            {/* Interactive Hospital Destination Selector & Live Rerouting */}
            <div className="space-y-1.5">
              <div className="text-lg font-bold text-on-surface">
                {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Commercial Building Fire, Bellary Rd' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Incident Site, MG Road' : (selectedIncident?.citizen_view?.hospital_name || selectedIncident.hospital_name)}
              </div>
              <label className="text-[10px] font-mono text-tertiary font-bold block uppercase">
                Change Hospital Destination (Live Uber-Style Reroute):
              </label>
              <select
                value={selectedIncident?.citizen_view?.hospital_name || selectedIncident.hospital_name}
                onChange={async (e) => {
                  const newHosp = e.target.value;
                  try {
                    const res = await fetch('/api/driver/change_hospital', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ incident_id: selectedIncident.incident_id, hospital_name: newHosp })
                    });
                    const data = await res.json();
                    if (data.citizen_view) {
                      setSelectedIncident(prev => ({
                        ...prev,
                        hospital_name: newHosp,
                        citizen_view: data.citizen_view,
                        route_coordinates: data.citizen_view.route_coordinates,
                        eta_minutes: data.citizen_view.eta_minutes
                      }));
                    }
                  } catch (err) {}
                }}
                className="w-full bg-surface-container-high border border-tertiary/40 text-on-surface text-xs font-mono font-bold p-2.5 rounded-xl focus:outline-none focus:border-tertiary shadow-sm"
              >
                {[
                  'Aster CMI Hospital (Hebbal)',
                  'MEDSTAR Speciality Hospital',
                  'Manipal Hospital (Hebbal)',
                  'Victoria Hospital',
                  'Fortis Hospital (Cunningham Rd)',
                  'Apollo Hospital (Seshadripuram)'
                ].map(h => (
                  <option key={h} value={h}>{h}</option>
                ))}
              </select>
            </div>"""

d_content = d_content.replace(old_hospital_panel, new_hospital_panel)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("DriverDashboard.jsx updated with 2-Stage Navigation and Live Hospital Rerouting Dropdown")

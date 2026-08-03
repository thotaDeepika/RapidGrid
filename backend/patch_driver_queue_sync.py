import sys

# 1. Update backend/routers/driver.py to include include_ambulance_backup and sort newest first
drv_py = "routers/driver.py"
with open(drv_py, "r", encoding="utf-8") as f:
    content = f.read()

old_get_active = """            active_list.append({
                "incident_id": inc["incident_id"],
                "status": inc.get("status"),
                "emergency_type": inc.get("emergency_type") or cit_view.get("emergency_type") or "General Emergency",
                "severity": inc.get("severity") or cit_view.get("severity") or 0.7,
                "hospital_name": cit_view.get("hospital_name") or rec_hosp.get("name") or "Nearest Hospital",
                "hospital_location": cit_view.get("hospital_location") or {"lat": 12.9716, "lng": 77.5946},
                "origin": cit_view.get("origin") or {"lat": 12.9756, "lng": 77.6068},
                "eta_minutes": cit_view.get("eta_minutes") or 7,
                "distance_meters": cit_view.get("distance_meters") or 2400,
                "route_coordinates": route_coords,
                "hospital": rec_hosp,
                "details": inc.get("details") or inc.get("citizen_text") or "Emergency reported by citizen.",
                "vehicle_required": inc.get("vehicle_required") or "Ambulance",
                "assigned_driver": inc.get("assigned_driver"),
                "driver_claimed": inc.get("driver_claimed", False)
            })
    return {"dispatches": active_list}"""

new_get_active = """            active_list.append({
                "incident_id": inc["incident_id"],
                "status": inc.get("status"),
                "emergency_type": inc.get("emergency_type") or cit_view.get("emergency_type") or "General Emergency",
                "severity": inc.get("severity") or cit_view.get("severity") or 0.7,
                "hospital_name": cit_view.get("hospital_name") or rec_hosp.get("name") or "Nearest Hospital",
                "hospital_location": cit_view.get("hospital_location") or {"lat": 12.9716, "lng": 77.5946},
                "origin": cit_view.get("origin") or {"lat": 12.9756, "lng": 77.6068},
                "eta_minutes": cit_view.get("eta_minutes") or 7,
                "distance_meters": cit_view.get("distance_meters") or 2400,
                "route_coordinates": route_coords,
                "hospital": rec_hosp,
                "details": inc.get("details") or inc.get("citizen_text") or "Emergency reported by citizen.",
                "vehicle_required": inc.get("vehicle_required") or "Ambulance",
                "include_ambulance_backup": inc.get("include_ambulance_backup") or cit_view.get("include_ambulance_backup") or False,
                "assigned_driver": inc.get("assigned_driver"),
                "driver_claimed": inc.get("driver_claimed", False)
            })
    active_list.reverse() # Newest incidents first
    return {"dispatches": active_list}"""

content = content.replace(old_get_active, new_get_active)
with open(drv_py, "w", encoding="utf-8") as f:
    f.write(content)

# Touch main.py for uvicorn reload
with open("main.py", "r", encoding="utf-8") as f:
    m = f.read()
m += "\n# Reload for driver active backup filter update"
with open("main.py", "w", encoding="utf-8") as f:
    f.write(m)


# 2. Update DriverDashboard.jsx to filter including ambulance backup
drv_file = "../frontend/src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

old_filter_code = """          <h2 className="text-sm font-bold text-on-surface-variant uppercase tracking-wider">
            Available Emergency Calls ({activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter).length})
          </h2>

          {activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter).length === 0 ? (
            <div className="bg-surface-container p-8 rounded-xl text-center border border-outline-variant/20 space-y-2">
              <ShieldAlert size={36} className="mx-auto text-on-surface-variant opacity-40" />
              <div className="font-semibold text-on-surface">No Active Dispatches for {driverVehicleFilter}</div>
              <p className="text-xs text-on-surface-variant">No pending emergency dispatches for this unit type at the moment.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter).map((inc) => ("""

new_filter_code = """  const isMatchFilter = (inc, filter) => {
    if (filter === 'All') return true;
    const req = inc.vehicle_required || 'Ambulance';
    if (req === filter) return true;
    if (filter === 'Ambulance' && inc.include_ambulance_backup) return true;
    return false;
  };

  const filteredDispatches = activeDispatches.filter(i => isMatchFilter(i, driverVehicleFilter));

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] p-4 bg-surface text-on-surface gap-4 overflow-y-auto">
      {/* Rest of JSX... */}"""

# Let's cleanly replace the filter rendering block
d_content = d_content.replace(
    "          <h2 className=\"text-sm font-bold text-on-surface-variant uppercase tracking-wider\">\n            Available Emergency Calls ({activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter).length})\n          </h2>",
    "          <h2 className=\"text-sm font-bold text-on-surface-variant uppercase tracking-wider\">\n            Available Emergency Calls ({activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter || (driverVehicleFilter === 'Ambulance' && i.include_ambulance_backup)).length})\n          </h2>"
)

d_content = d_content.replace(
    "{activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter).length === 0 ? (",
    "{activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter || (driverVehicleFilter === 'Ambulance' && i.include_ambulance_backup)).length === 0 ? ("
)

d_content = d_content.replace(
    "{activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter).map((inc) => (",
    "{activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter || (driverVehicleFilter === 'Ambulance' && i.include_ambulance_backup)).map((inc) => ("
)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("Driver active dispatch filter patched cleanly to include ambulance backup calls and sort newest first")

import sys

# 1. Update backend/routers/driver.py with arrived_pickup & change_hospital endpoints
drv_py = "routers/driver.py"
with open(drv_py, "r", encoding="utf-8") as f:
    content = f.read()

endpoints_code = """
class HospitalChangePayload(BaseModel):
    incident_id: str
    hospital_name: str

BANGALORE_HOSPITAL_COORDS = {
    "Aster CMI Hospital (Hebbal)": {"lat": 13.0473, "lng": 77.5908},
    "MEDSTAR Speciality Hospital": {"lat": 13.0380, "lng": 77.5860},
    "Manipal Hospital (Hebbal)": {"lat": 13.0420, "lng": 77.5920},
    "Victoria Hospital": {"lat": 12.9634, "lng": 77.5746},
    "Fortis Hospital (Cunningham Rd)": {"lat": 12.9880, "lng": 77.5940},
    "Apollo Hospital (Seshadripuram)": {"lat": 12.9940, "lng": 77.5780}
}

@router.post("/arrived_pickup")
async def arrived_pickup(payload: ClaimPayload):
    from routers.incident import route_agent, Coordinate, RouteRequest
    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == payload.incident_id:
            inc["driver_stage"] = "hospital"
            inc["status"] = "patient_picked_up"
            
            # Recompute live route from Patient -> Hospital
            cit_view = inc.get("citizen_view") or {}
            origin = cit_view.get("origin") or inc.get("location") or {"lat": 12.9756, "lng": 77.6068}
            hosp_loc = cit_view.get("hospital_location") or {"lat": 13.0473, "lng": 77.5908}
            
            try:
                p2_route = route_agent.compute_route(RouteRequest(
                    origin=Coordinate(lat=origin["lat"], lng=origin["lng"]),
                    destination=Coordinate(lat=hosp_loc["lat"], lng=hosp_loc["lng"])
                ))
                new_coords = [{"lat": c.lat, "lng": c.lng} for c in p2_route.coordinates]
                eta_mins = max(1, int(p2_route.eta // 60))
                dist_meters = p2_route.distance
            except Exception as e:
                new_coords = [{"lat": origin["lat"], "lng": origin["lng"]}, {"lat": hosp_loc["lat"], "lng": hosp_loc["lng"]}]
                eta_mins = 6
                dist_meters = 2800

            cit_view["route_coordinates"] = new_coords
            cit_view["eta_minutes"] = eta_mins
            cit_view["distance_meters"] = dist_meters
            cit_view["message"] = f"Patient picked up. Transporting to {cit_view.get('hospital_name', 'Hospital ER')}."
            cit_view["status"] = "patient_picked_up"
            inc["citizen_view"] = cit_view
            save_db()
            return {"status": "patient_picked_up", "citizen_view": cit_view}
    raise HTTPException(status_code=404, detail="Incident not found")

@router.post("/change_hospital")
async def change_hospital(payload: HospitalChangePayload):
    from routers.incident import route_agent, Coordinate, RouteRequest
    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == payload.incident_id:
            h_coords = BANGALORE_HOSPITAL_COORDS.get(payload.hospital_name) or {"lat": 13.0473, "lng": 77.5908}
            
            cit_view = inc.get("citizen_view") or {}
            origin = cit_view.get("origin") or inc.get("location") or {"lat": 12.9756, "lng": 77.6068}
            
            # Recompute live Google route from Patient Location -> New Selected Hospital
            try:
                new_route = route_agent.compute_route(RouteRequest(
                    origin=Coordinate(lat=origin["lat"], lng=origin["lng"]),
                    destination=Coordinate(lat=h_coords["lat"], lng=h_coords["lng"])
                ))
                new_coords = [{"lat": c.lat, "lng": c.lng} for c in new_route.coordinates]
                eta_mins = max(1, int(new_route.eta // 60))
                dist_meters = new_route.distance
            except Exception as e:
                new_coords = [{"lat": origin["lat"], "lng": origin["lng"]}, {"lat": h_coords["lat"], "lng": h_coords["lng"]}]
                eta_mins = 7
                dist_meters = 3200

            cit_view["hospital_name"] = payload.hospital_name
            cit_view["hospital_location"] = h_coords
            cit_view["route_coordinates"] = new_coords
            cit_view["eta_minutes"] = eta_mins
            cit_view["distance_meters"] = dist_meters
            cit_view["message"] = f"Rerouted by driver to {payload.hospital_name}."
            
            inc["hospital_name"] = payload.hospital_name
            inc["citizen_view"] = cit_view
            save_db()
            return {"status": "rerouted", "citizen_view": cit_view}
    raise HTTPException(status_code=404, detail="Incident not found")
"""

if "change_hospital" not in content:
    content += endpoints_code
    with open(drv_py, "w", encoding="utf-8") as f:
        f.write(content)

# Touch main.py for uvicorn reload
with open("main.py", "r", encoding="utf-8") as f:
    m = f.read()
m += "\n# Reload for 2-stage driver hospital rerouting endpoints"
with open("main.py", "w", encoding="utf-8") as f:
    f.write(m)

print("Backend driver.py updated with 2-Stage Navigation & Hospital Rerouting endpoints")

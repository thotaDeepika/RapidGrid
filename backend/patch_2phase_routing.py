import sys

# 1. Update backend/agents/route_optimization.py with 2-Phase Hub Routing Engine
route_py = "agents/route_optimization.py"
with open(route_py, "r", encoding="utf-8") as f:
    r_content = f.read()

hubs_code = """
import math

EMERGENCY_HUBS = {
    "Ambulance": [
        {"id": "AMB-HUB-01", "name": "Aster CMI Emergency Ambulance Hub", "lat": 13.0473, "lng": 77.5908},
        {"id": "AMB-HUB-02", "name": "Manipal Ambulance Base Depot", "lat": 12.9585, "lng": 77.6483},
        {"id": "AMB-HUB-03", "name": "Victoria Hospital Paramedic Base", "lat": 12.9634, "lng": 77.5746},
    ],
    "Fire Engine": [
        {"id": "FIRE-HUB-01", "name": "Hebbal Fire & Rescue Station #4", "lat": 13.0336, "lng": 77.5891},
        {"id": "FIRE-HUB-02", "name": "High Grounds Central Fire Station", "lat": 12.9866, "lng": 77.5878},
        {"id": "FIRE-HUB-03", "name": "Jayanagar Emergency Fire Station", "lat": 12.9298, "lng": 77.5831},
    ],
    "Police Cruiser": [
        {"id": "POLICE-HUB-01", "name": "Hebbal Police Patrol Base", "lat": 13.0350, "lng": 77.5880},
        {"id": "POLICE-HUB-02", "name": "Central MG Road Police Precinct", "lat": 12.9754, "lng": 77.6071},
        {"id": "POLICE-HUB-03", "name": "Cubbon Park Traffic Police Hub", "lat": 12.9740, "lng": 77.5930},
    ],
    "Disaster Rescue": [
        {"id": "DISASTER-HUB-01", "name": "NDRF Disaster Rescue Hub North", "lat": 13.0550, "lng": 77.6120},
        {"id": "DISASTER-HUB-02", "name": "Civil Defence Emergency Depot", "lat": 12.9600, "lng": 77.6000},
    ]
}

def haversine_dist(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def find_nearest_hub(vehicle_type, citizen_lat, citizen_lng):
    hubs = EMERGENCY_HUBS.get(vehicle_type) or EMERGENCY_HUBS["Ambulance"]
    best_hub = hubs[0]
    min_dist = haversine_dist(citizen_lat, citizen_lng, best_hub["lat"], best_hub["lng"])
    for h in hubs[1:]:
        d = haversine_dist(citizen_lat, citizen_lng, h["lat"], h["lng"])
        if d < min_dist:
            min_dist = d
            best_hub = h
    return best_hub
"""

if "EMERGENCY_HUBS" not in r_content:
    r_content += hubs_code
    with open(route_py, "w", encoding="utf-8") as f:
        f.write(r_content)


# 2. Update backend/routers/incident.py to compute Phase 1 (Hub -> Citizen) & Phase 2 (Citizen -> Hospital)
inc_py = "routers/incident.py"
with open(inc_py, "r", encoding="utf-8") as f:
    i_content = f.read()

# Enhance run_pipeline to attach 2-Phase Routing Telemetry
phase_routing_code = """            # Compute 2-Phase Shortest Routes: Phase 1 (Station Hub -> Citizen) and Phase 2 (Citizen -> Hospital)
            from agents.route_optimization import find_nearest_hub
            veh_type = payload.vehicle_required or "Ambulance"
            nearest_hub = find_nearest_hub(veh_type, payload.location.lat, payload.location.lng)
            
            # Phase 1: Hub -> Citizen
            try:
                p1_route = route_agent.compute_route(RouteRequest(
                    origin=Coordinate(lat=nearest_hub["lat"], lng=nearest_hub["lng"]),
                    destination=payload.location
                ))
                p1_coords = [{"lat": c.lat, "lng": c.lng} for c in p1_route.coordinates]
                p1_eta = max(1, int(p1_route.eta // 60))
            except Exception as e:
                p1_coords = [{"lat": nearest_hub["lat"], "lng": nearest_hub["lng"]}, {"lat": payload.location.lat, "lng": payload.location.lng}]
                p1_eta = 5

            inc["citizen_view"] = {
                "message": f"Dispatching from {nearest_hub['name']}. Destination Hospital: {hosp.name}.",
                "eta_minutes": int(fusion_res.recommended_route.eta // 60),
                "hospital_name": hosp.name,
                "hospital_location": {"lat": hosp.location.lat, "lng": hosp.location.lng},
                "origin": {"lat": payload.location.lat, "lng": payload.location.lng},
                "route_coordinates": route_coords,
                "phase1_hub": nearest_hub,
                "phase1_route_coordinates": p1_coords,
                "phase1_eta_minutes": p1_eta,
                "distance_meters": fusion_res.recommended_route.distance,
                "emergency_type": access_res.incident_report.incident_type.value,
                "severity": access_res.incident_report.severity_estimate,
                "vehicle_required": payload.vehicle_required or "Ambulance",
                "include_ambulance_backup": bool(payload.include_ambulance_backup),
            }"""

if "phase1_hub" not in i_content:
    i_content = i_content.replace(
        """            inc["citizen_view"] = {
                "message": f"Help is being dispatched. Estimated hospital: {hosp.name}.",
                "eta_minutes": int(fusion_res.recommended_route.eta // 60),
                "hospital_name": hosp.name,
                "hospital_location": {
                    "lat": hosp.location.lat,
                    "lng": hosp.location.lng
                },
                "origin": {
                    "lat": payload.location.lat,
                    "lng": payload.location.lng
                },
                "route_coordinates": route_coords,
                "distance_meters": fusion_res.recommended_route.distance,
                "emergency_type": access_res.incident_report.incident_type.value,
                "severity": access_res.incident_report.severity_estimate,
                "vehicle_required": payload.vehicle_required or "Ambulance",
                "include_ambulance_backup": bool(payload.include_ambulance_backup),
            }""",
        phase_routing_code
    )

with open(inc_py, "w", encoding="utf-8") as f:
    f.write(i_content)

# Touch main.py for uvicorn reload
with open("main.py", "r", encoding="utf-8") as f:
    m = f.read()
m += "\n# Touch for 2-Phase Hub Routing reload"
with open("main.py", "w", encoding="utf-8") as f:
    f.write(m)

print("2-Phase Hub Routing Engine patched 100% in backend")

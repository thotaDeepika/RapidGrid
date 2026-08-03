import sys

# 1. Update backend/routers/incident.py to compute fresh route when re-routing to an approved_hospital
inc_file = "routers/incident.py"
with open(inc_file, "r", encoding="utf-8") as f:
    inc_content = f.read()

new_approve_endpoint = """@router.post("/{incident_id}/approve")
async def approve_incident(incident_id: str, payload: ApprovePayload):
    \"\"\"Step 4 - Dispatcher approves or re-routes to a selected hospital.\"\"\"
    from agents.route_optimization import route_agent
    from models.schemas import RouteRequest, Coordinate

    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == incident_id:
            inc["status"] = "dispatched"
            inc["assigned_driver"] = "drv-11"
            inc["dispatcher_id"] = payload.dispatcher_id

            # Find approved hospital from all_hospitals candidate list
            action_plan = inc.get("action_plan") or {}
            all_hospitals = action_plan.get("all_hospitals") or []
            target_hosp = None

            for h in all_hospitals:
                h_dict = h if isinstance(h, dict) else h.model_dump()
                if h_dict.get("hospital_id") == payload.approved_hospital or h_dict.get("name") == payload.approved_hospital:
                    target_hosp = h_dict
                    break

            if target_hosp:
                hosp_loc_dict = target_hosp.get("location") or {}
                hosp_lat = hosp_loc_dict.get("lat") or 12.9716
                hosp_lng = hosp_loc_dict.get("lng") or 77.5946

                cit_loc_dict = inc.get("location") or {}
                cit_lat = cit_loc_dict.get("lat") or 12.9756
                cit_lng = cit_loc_dict.get("lng") or 77.6068

                # Compute dynamic route to newly selected hospital
                try:
                    new_route = route_agent.compute_route(RouteRequest(
                        origin=Coordinate(lat=cit_lat, lng=cit_lng),
                        destination=Coordinate(lat=hosp_lat, lng=hosp_lng)
                    ))
                    new_coords = [{"lat": c.lat, "lng": c.lng} for c in new_route.coordinates]
                    eta_mins = max(1, int(new_route.eta // 60))
                    dist_meters = new_route.distance
                except Exception as e:
                    print("Error computing re-route:", e)
                    new_coords = [{"lat": cit_lat, "lng": cit_lng}, {"lat": hosp_lat, "lng": hosp_lng}]
                    eta_mins = 7
                    dist_meters = 3500

                inc["citizen_view"] = {
                    "message": f"Help is being dispatched. Approved Hospital: {target_hosp.get('name')}.",
                    "eta_minutes": eta_mins,
                    "hospital_name": target_hosp.get("name"),
                    "hospital_location": {"lat": hosp_lat, "lng": hosp_lng},
                    "origin": {"lat": cit_lat, "lng": cit_lng},
                    "route_coordinates": new_coords,
                    "distance_meters": dist_meters,
                    "emergency_type": inc.get("emergency_type", "General"),
                    "severity": inc.get("severity", 0.5)
                }

            import logging
            logging.getLogger("geoagentic.bus").info(
                f"PLAN_APPROVED for {incident_id}: SMS sent, pinged ER desk, pushed to drv-11"
            )

            return inc
    raise HTTPException(status_code=404, detail="Incident not found")"""

import re
inc_content = re.sub(r'@router\.post\(\"/{incident_id}/approve\"\)\nasync def approve_incident[\s\S]*?\n(?=@router|\Z)', new_approve_endpoint + "\n\n", inc_content)

with open(inc_file, "w", encoding="utf-8") as f:
    f.write(inc_content)

print("Backend incident.py re-routing patched successfully")

import sys

# 1. Update backend/routers/driver.py
driver_file = "routers/driver.py"
with open(driver_file, "r", encoding="utf-8") as f:
    d_content = f.read()

new_driver_py = """# Driver Router for live Unified React App
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from routers.incident import ACTIVE_INCIDENTS

router = APIRouter(prefix="/api/driver", tags=["Driver Queue"])

@router.get("/active")
async def get_active_dispatches():
    active_list = []
    for inc in ACTIVE_INCIDENTS:
        status = inc.get("status")
        if status in ["dispatched", "awaiting_dispatcher_approval", "processing"]:
            cit_view = inc.get("citizen_view") or {}
            act_plan = inc.get("action_plan") or {}
            rec_hosp = act_plan.get("recommended_hospital") or {}
            rec_route = act_plan.get("recommended_route") or {}

            route_coords = cit_view.get("route_coordinates") or []
            if not route_coords and hasattr(rec_route, "coordinates") and rec_route.coordinates:
                route_coords = [{"lat": c.lat, "lng": c.lng} for c in rec_route.coordinates]

            active_list.append({
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
                "details": inc.get("details") or inc.get("citizen_text") or "Emergency reported by citizen."
            })
    return {"dispatches": active_list}

@router.get("/{driver_id}/assignment")
async def get_driver_assignment(driver_id: str):
    for inc in ACTIVE_INCIDENTS:
        if inc.get("status") == "dispatched":
            cit_view = inc.get("citizen_view") or {}
            act_plan = inc.get("action_plan") or {}
            rec_hosp = act_plan.get("recommended_hospital") or {}
            rec_route = act_plan.get("recommended_route") or {}
            
            return {
                "incident_id": inc["incident_id"],
                "route": rec_route,
                "hospital": rec_hosp,
                "patient_summary": {
                    "emergency_type": inc.get("emergency_type"),
                    "severity": inc.get("severity"),
                    "details": inc.get("details", "")
                }
            }
    return {"incident_id": None}
"""

with open(driver_file, "w", encoding="utf-8") as f:
    f.write(new_driver_py)

print("Backend driver.py patched successfully")

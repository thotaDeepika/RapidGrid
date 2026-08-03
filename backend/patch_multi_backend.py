import sys

# 1. Update backend/routers/driver.py to add /api/driver/claim endpoint
driver_file = "routers/driver.py"

driver_py_code = """# Driver Router for live Unified React App
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from routers.incident import ACTIVE_INCIDENTS, save_db

router = APIRouter(prefix="/api/driver", tags=["Driver Queue"])

class ClaimPayload(BaseModel):
    incident_id: str
    driver_id: str = "drv-11"

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
                "details": inc.get("details") or inc.get("citizen_text") or "Emergency reported by citizen.",
                "assigned_driver": inc.get("assigned_driver"),
                "driver_claimed": inc.get("driver_claimed", False)
            })
    return {"dispatches": active_list}

@router.post("/claim")
async def claim_dispatch(payload: ClaimPayload):
    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == payload.incident_id:
            existing_driver = inc.get("assigned_driver")
            if existing_driver and existing_driver != payload.driver_id and inc.get("driver_claimed"):
                raise HTTPException(status_code=409, detail=f"Already claimed by {existing_driver}")
            
            inc["assigned_driver"] = payload.driver_id
            inc["driver_claimed"] = True
            save_db()
            return {"status": "claimed", "incident_id": payload.incident_id, "driver_id": payload.driver_id}
    raise HTTPException(status_code=404, detail="Incident not found")
"""

with open(driver_file, "w", encoding="utf-8") as f:
    f.write(driver_py_code)

# 2. Update backend/routers/hospital.py to support filtering by hospital_id or hospital_name
hosp_file = "routers/hospital.py"
with open(hosp_file, "r", encoding="utf-8") as f:
    h_content = f.read()

new_get_incoming = """@router.get("/{hospital_id}/incoming")
async def get_incoming_cases(hospital_id: str):
    \"\"\"Hospital dashboard polls for incoming cases assigned specifically to this hospital.\"\"\"
    incoming = []
    for inc in ACTIVE_INCIDENTS:
        if inc.get("status") in ("dispatched", "awaiting_dispatcher_approval", "processing"):
            cit_view = inc.get("citizen_view") or {}
            action_plan = inc.get("action_plan") or {}
            rec_hosp = action_plan.get("recommended_hospital") or {}
            hosp_name = cit_view.get("hospital_name") or (rec_hosp.get("name") if isinstance(rec_hosp, dict) else "")

            # Match by hospital_id, hospital_name, or if hospital_id == 'all'
            matches = (
                hospital_id == 'all' or
                (isinstance(rec_hosp, dict) and rec_hosp.get("hospital_id") == hospital_id) or
                (isinstance(rec_hosp, str) and rec_hosp == hospital_id) or
                (hosp_name and hospital_id.lower() in hosp_name.lower())
            )

            if matches:
                incoming.append({
                    "incident_id": inc["incident_id"],
                    "status": inc.get("status"),
                    "emergency_type": inc.get("emergency_type") or cit_view.get("emergency_type") or "General Emergency",
                    "severity": inc.get("severity") or cit_view.get("severity") or 0.7,
                    "hospital_name": hosp_name or "Assigned Hospital",
                    "eta_minutes": cit_view.get("eta_minutes") or 7,
                    "patient_summary": inc.get("details") or inc.get("citizen_text") or "Emergency reported by citizen.",
                    "assigned_driver": inc.get("assigned_driver", "AMB-IND-04")
                })
    return {"incoming": incoming}"""

import re
h_content = re.sub(r'@router\.get\(\"/{hospital_id}/incoming\"\)\nasync def get_incoming_cases[\s\S]*?\n(?=@|\Z)', new_get_incoming + "\n\n", h_content)

with open(hosp_file, "w", encoding="utf-8") as f:
    f.write(h_content)

print("Backend driver.py and hospital.py updated for multi-patient and hospital-specific tracking")

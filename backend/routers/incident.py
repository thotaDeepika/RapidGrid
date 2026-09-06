"""
Incident Router for live Unified React App.
Matches the event-driven async flow described in the trace.
"""
from __future__ import annotations

import uuid
import asyncio
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Response, status, HTTPException
from pydantic import BaseModel

from models.schemas import (
    Coordinate,
    AccessibilityRequest,
    AccessibilityInputModality,
    FusionRequest,
    RouteRequest,
)
from agents.accessibility import accessibility_agent
from agents.decision_fusion import fusion_engine
from agents.route_optimization import route_agent, find_nearest_hub

logger = logging.getLogger("geoagentic.incident")

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])

# In-memory queue of active incidents
ACTIVE_INCIDENTS: List[Dict[str, Any]] = []

import json
from pathlib import Path

DB_FILE = Path(__file__).parent.parent / "data" / "incidents_db.json"

def save_db():
    try:
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(ACTIVE_INCIDENTS, f, indent=2)
    except Exception as e:
        print("DB save error:", e)

def load_db():
    global ACTIVE_INCIDENTS
    try:
        if DB_FILE.exists():
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    ACTIVE_INCIDENTS.clear()
                    ACTIVE_INCIDENTS.extend(data)
    except Exception as e:
        print("DB load error:", e)

load_db()


class IncidentReportPayload(BaseModel):
    citizen_text: str
    citizen_name: Optional[str] = None
    citizen_phone: Optional[str] = None
    vehicle_required: Optional[str] = "Ambulance"
    include_ambulance_backup: Optional[bool] = False
    location: Coordinate
    input_modality: str = "text"
    timestamp: Optional[str] = None

class ApprovePayload(BaseModel):
    dispatcher_id: str
    approved_hospital: str
    approved_route: str

async def run_pipeline(incident_id: str, payload: IncidentReportPayload):
    """Background task simulating the event-driven bus pipeline."""
    # Step 2a: Accessibility Agent
    access_req = AccessibilityRequest(
        raw_input=payload.citizen_text,
        location=payload.location,
        modality=AccessibilityInputModality.TEXT
    )
    access_res = await accessibility_agent.process_input(access_req)
    
    # Update incident with classification details
    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == incident_id:
            inc["emergency_type"] = access_res.incident_report.incident_type.value
            inc["severity"] = access_res.incident_report.severity_estimate
            inc["details"] = access_res.incident_report.extracted_details
            break
            
    # Step 2b: Decision Fusion Engine (which coordinates Traffic, Route, Hospital, Prediction)
    # Use citizen's location for hospital search + route origin (nearest ambulance station)
    # In production this would be the nearest dispatched ambulance's real-time GPS
    fusion_req = FusionRequest(
        incident_id=incident_id,
        incident_location=payload.location,
        emergency_type=access_res.incident_report.incident_type,
        severity=access_res.incident_report.severity_estimate,
        vehicle_location=payload.location,  # Nearest ambulance dispatches from citizen area
        accessibility_needs=access_res.citizen_accessibility_profile.model_dump()
    )
    
    # Run the fusion engine to generate action plan
    fusion_res = await fusion_engine.fuse(fusion_req)
    
    # Attach plan and update status to awaiting_dispatcher_approval
    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == incident_id:
            inc["action_plan"] = fusion_res.model_dump(mode="json")
            inc["status"] = "awaiting_dispatcher_approval"
            # Build route polyline for map rendering
            route_coords = [
                {"lat": c.lat, "lng": c.lng}
                for c in fusion_res.recommended_route.coordinates
            ]
            hosp = fusion_res.recommended_hospital
            # Compute 2-Phase Shortest Routes: Phase 1 (Station Hub -> Citizen) and Phase 2 (Citizen -> Hospital)
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
            }
            save_db()
            break

@router.post("")
async def report_incident(payload: IncidentReportPayload, response: Response):
    """Step 1 - Citizen raises emergency. Returns 202 immediately."""
    incident_id = f"INC-{uuid.uuid4().hex[:4]}"
    
    incident = {
        "incident_id": incident_id,
        "location": payload.location.model_dump(),
        "citizen_text": payload.citizen_text,
        "citizen_name": payload.citizen_name or "Anonymous Citizen",
        "citizen_phone": payload.citizen_phone or "Unregistered",
        "vehicle_required": payload.vehicle_required or "Ambulance",
        "include_ambulance_backup": bool(payload.include_ambulance_backup),
        "status": "processing",
        "action_plan": None
    }
    ACTIVE_INCIDENTS.append(incident)
    save_db()
    
    # Start background processing pipeline
    asyncio.create_task(run_pipeline(incident_id, payload))
    
    response.status_code = status.HTTP_202_ACCEPTED
    return {
        "incident_id": incident_id,
        "status": "processing",
        "poll_url": f"/api/incidents/{incident_id}"
    }

@router.get("/{incident_id}")
async def get_incident(incident_id: str):
    """Step 3 - Citizen screen polls."""
    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] == incident_id:
            return inc
    raise HTTPException(status_code=404, detail="Incident not found")

@router.get("/")
async def get_all_incidents():
    """For Dispatcher to see all active incidents."""
    # Ensure they have severity for sorting
    for inc in ACTIVE_INCIDENTS:
        if "severity" not in inc:
            inc["severity"] = 0.5
    return {"incidents": ACTIVE_INCIDENTS}

@router.post("/{incident_id}/approve")
async def approve_incident(incident_id: str, payload: ApprovePayload):
    """Step 4 - Dispatcher approves the AI plan, or overrides the hospital."""

    for inc in ACTIVE_INCIDENTS:
        if inc["incident_id"] != incident_id:
            continue

        action_plan = inc.get("action_plan") or {}
        all_hospitals = action_plan.get("all_hospitals") or []

        # Resolve the approved hospital by id or name.
        target_hosp = None
        for h in all_hospitals:
            h_dict = h if isinstance(h, dict) else h.model_dump()
            if payload.approved_hospital in (
                h_dict.get("hospital_id"), h_dict.get("name")
            ):
                target_hosp = h_dict
                break

        # BUG: the dispatcher UI sends sentinel ids ('HOSP-DEFAULT', 'HOSP-AUTO')
        # whenever the plan is still loading, and the old code then dereferenced
        # target_hosp=None -> HTTP 500. Fall back to the AI recommendation.
        if target_hosp is None:
            recommended = action_plan.get("recommended_hospital")
            if isinstance(recommended, dict):
                target_hosp = recommended
                logger.warning(
                    "Approve for %s: '%s' not in candidate list — falling back "
                    "to the recommended hospital '%s'.",
                    incident_id, payload.approved_hospital,
                    target_hosp.get("name"),
                )
            else:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Cannot approve {incident_id}: no action plan is ready "
                        f"yet and '{payload.approved_hospital}' matched no "
                        f"candidate hospital."
                    ),
                )

        inc["status"] = "dispatched"
        inc["assigned_driver"] = "drv-11"
        inc["dispatcher_id"] = payload.dispatcher_id

        hosp_loc = target_hosp.get("location") or {}
        hosp_lat = hosp_loc.get("lat") or 12.9716
        hosp_lng = hosp_loc.get("lng") or 77.5946

        cit_loc = inc.get("location") or {}
        cit_lat = cit_loc.get("lat") or 12.9756
        cit_lng = cit_loc.get("lng") or 77.6068

        # Recompute Phase 2 (citizen -> approved hospital).
        route_ok = True
        try:
            new_route = route_agent.compute_route(RouteRequest(
                origin=Coordinate(lat=cit_lat, lng=cit_lng),
                destination=Coordinate(lat=hosp_lat, lng=hosp_lng),
            ))
            route_ok = new_route.confidence > 0 and len(new_route.coordinates) >= 2
            new_coords = [{"lat": c.lat, "lng": c.lng} for c in new_route.coordinates]
            eta_mins = max(1, int(new_route.eta // 60))
            dist_meters = new_route.distance
        except Exception:
            logger.exception("Re-route failed for %s", incident_id)
            route_ok = False
            new_coords = [
                {"lat": cit_lat, "lng": cit_lng},
                {"lat": hosp_lat, "lng": hosp_lng},
            ]
            eta_mins = 0
            dist_meters = 0.0

        # MERGE into citizen_view rather than replacing it. The old code
        # rebuilt the dict from scratch and silently dropped phase1_hub,
        # phase1_route_coordinates, phase1_eta_minutes, vehicle_required and
        # include_ambulance_backup — so approving wiped the 2-phase route off
        # the citizen's map at the exact moment it mattered most.
        citizen_view = dict(inc.get("citizen_view") or {})
        citizen_view.update({
            "message": f"Help is being dispatched. Approved Hospital: {target_hosp.get('name')}.",
            "eta_minutes": eta_mins,
            "hospital_name": target_hosp.get("name"),
            "hospital_location": {"lat": hosp_lat, "lng": hosp_lng},
            "origin": {"lat": cit_lat, "lng": cit_lng},
            "route_coordinates": new_coords,
            "distance_meters": dist_meters,
            "emergency_type": inc.get("emergency_type", "General"),
            "severity": inc.get("severity", 0.5),
            "route_degraded": not route_ok,
        })
        inc["citizen_view"] = citizen_view

        # Persist AFTER the view is built, not before.
        save_db()

        logger.info(
            "PLAN_APPROVED for %s by %s: hospital=%s, ETA=%dmin%s",
            incident_id, payload.dispatcher_id, target_hosp.get("name"),
            eta_mins, "" if route_ok else " (ROUTE DEGRADED)",
        )
        return inc

    raise HTTPException(status_code=404, detail="Incident not found")

@router.post("/{incident_id}/arrived")
async def incident_arrived(incident_id: str, unit_type: str = "primary"):
    """Step 5 - Driver arrives for specific unit (primary vs ambulance)."""
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
    raise HTTPException(status_code=404, detail="Incident not found")


@router.post("/clear")
async def clear_incidents():
    ACTIVE_INCIDENTS.clear()
    save_db()
    return {"status": "cleared"}
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

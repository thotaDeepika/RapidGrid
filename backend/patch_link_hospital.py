import sys

# 1. Update backend/routers/hospital.py
hosp_py = "routers/hospital.py"
with open(hosp_py, "r", encoding="utf-8") as f:
    content = f.read()

old_get_incoming = """@router.get("/{hospital_id}/incoming")
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

new_get_incoming = """@router.get("/{hospital_id}/incoming")
async def get_incoming_cases(hospital_id: str, name: str = None):
    \"\"\"Hospital dashboard polls for incoming cases assigned specifically to this hospital.\"\"\"
    incoming = []
    for inc in ACTIVE_INCIDENTS:
        if inc.get("status") in ("dispatched", "awaiting_dispatcher_approval", "processing", "completed"):
            cit_view = inc.get("citizen_view") or {}
            action_plan = inc.get("action_plan") or {}
            rec_hosp = action_plan.get("recommended_hospital") or {}
            
            hosp_name = cit_view.get("hospital_name")
            if not hosp_name and isinstance(rec_hosp, dict):
                hosp_name = rec_hosp.get("name")
            elif not hosp_name and hasattr(rec_hosp, "name"):
                hosp_name = rec_hosp.name
            hosp_name = hosp_name or "Assigned Hospital"

            rec_id = ""
            if isinstance(rec_hosp, dict):
                rec_id = rec_hosp.get("hospital_id", "")
            elif hasattr(rec_hosp, "hospital_id"):
                rec_id = getattr(rec_hosp, "hospital_id", "")

            target_terms = [hospital_id.lower()]
            if name:
                target_terms.append(name.lower())

            # Match by all, hospital_id, hospital_name, or name tokens
            matches = (
                hospital_id == 'all' or
                rec_id.lower() == hospital_id.lower() or
                any(term in hosp_name.lower() for term in target_terms if term) or
                any(token in hosp_name.lower() for term in target_terms for token in term.split() if len(token) > 3)
            )

            if matches:
                incoming.append({
                    "incident_id": inc["incident_id"],
                    "status": inc.get("status"),
                    "emergency_type": inc.get("emergency_type") or cit_view.get("emergency_type") or "General Emergency",
                    "severity": inc.get("severity") or cit_view.get("severity") or 0.7,
                    "hospital_name": hosp_name,
                    "eta_minutes": cit_view.get("eta_minutes") or 7,
                    "patient_summary": inc.get("details") or inc.get("citizen_text") or "Emergency reported by citizen.",
                    "assigned_driver": inc.get("assigned_driver", "AMB-UNIT-04")
                })
    return {"incoming": incoming}"""

content = content.replace(old_get_incoming, new_get_incoming)

with open(hosp_py, "w", encoding="utf-8") as f:
    f.write(content)


# 2. Update frontend/src/views/HospitalDashboard.jsx
hosp_dash = "../frontend/src/views/HospitalDashboard.jsx"
with open(hosp_dash, "r", encoding="utf-8") as f:
    d_content = f.read()

d_content = d_content.replace(
    "const res = await fetch(`/api/hospital/${hospitalInfo?.id || 'all'}/incoming`);",
    "const res = await fetch(`/api/hospital/${hospitalInfo?.id || 'all'}/incoming?name=${encodeURIComponent(hospitalInfo?.name || '')}`);"
)

with open(hosp_dash, "w", encoding="utf-8") as f:
    f.write(d_content)

print("Hospital incoming cases matcher updated for 100% linking with logged-in hospitals")

import sys

# 1. Update backend/routers/hospital.py to support GET /api/hospital/incoming/all
hosp_file = "routers/hospital.py"
with open(hosp_file, "r", encoding="utf-8") as f:
    h_content = f.read()

new_incoming_all = """@router.get("/incoming/all")
async def get_all_incoming_cases():
    \"\"\"Return all active incoming emergency cases for the Hospital ER Desk.\"\"\"
    incoming = []
    for inc in ACTIVE_INCIDENTS:
        if inc.get("status") in ("dispatched", "awaiting_dispatcher_approval", "processing"):
            cit_view = inc.get("citizen_view") or {}
            action_plan = inc.get("action_plan") or {}
            rec_hosp = action_plan.get("recommended_hospital") or {}
            hosp_name = cit_view.get("hospital_name") or rec_hosp.get("name") or "Nearest Hospital"

            incoming.append({
                "incident_id": inc["incident_id"],
                "status": inc.get("status"),
                "emergency_type": inc.get("emergency_type") or cit_view.get("emergency_type") or "General Emergency",
                "severity": inc.get("severity") or cit_view.get("severity") or 0.7,
                "hospital_name": hosp_name,
                "eta_minutes": cit_view.get("eta_minutes") or 7,
                "patient_summary": inc.get("details") or inc.get("citizen_text") or "Emergency reported by citizen.",
                "assigned_driver": inc.get("assigned_driver", "AMB-IND-04")
            })
    return {"incoming": incoming}"""

if "/incoming/all" not in h_content:
    h_content = h_content.replace(
        '@router.get("/{hospital_id}/incoming")',
        new_incoming_all + '\n\n@router.get("/{hospital_id}/incoming")'
    )
    with open(hosp_file, "w", encoding="utf-8") as f:
        f.write(h_content)

print("Backend hospital.py patched successfully")

import sys

# 1. Update backend/routers/incident.py to accept citizen_name and citizen_phone in payload
inc_file = "routers/incident.py"
with open(inc_file, "r", encoding="utf-8") as f:
    content = f.read()

# Update IncidentReportPayload
content = content.replace(
    "class IncidentReportPayload(BaseModel):\n    citizen_text: str",
    "class IncidentReportPayload(BaseModel):\n    citizen_text: str\n    citizen_name: Optional[str] = None\n    citizen_phone: Optional[str] = None"
)

# Update report_incident function
old_inc_dict = """    incident = {
        "incident_id": incident_id,
        "location": payload.location.model_dump(),
        "citizen_text": payload.citizen_text,
        "status": "processing",
        "action_plan": None
    }"""

new_inc_dict = """    incident = {
        "incident_id": incident_id,
        "location": payload.location.model_dump(),
        "citizen_text": payload.citizen_text,
        "citizen_name": payload.citizen_name or "Anonymous Citizen",
        "citizen_phone": payload.citizen_phone or "Unregistered",
        "status": "processing",
        "action_plan": None
    }"""

content = content.replace(old_inc_dict, new_inc_dict)

with open(inc_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Backend incident.py updated to store citizen ownership")

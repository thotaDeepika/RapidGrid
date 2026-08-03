import sys

# 1. Update backend/routers/incident.py
inc_file = "routers/incident.py"
with open(inc_file, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "class IncidentReportPayload(BaseModel):\n    citizen_text: str\n    citizen_name: Optional[str] = None\n    citizen_phone: Optional[str] = None\n    vehicle_required: Optional[str] = \"Ambulance\"",
    "class IncidentReportPayload(BaseModel):\n    citizen_text: str\n    citizen_name: Optional[str] = None\n    citizen_phone: Optional[str] = None\n    vehicle_required: Optional[str] = \"Ambulance\"\n    include_ambulance_backup: Optional[bool] = False"
)

content = content.replace(
    '"vehicle_required": payload.vehicle_required or "Ambulance",\n        "status": "processing",',
    '"vehicle_required": payload.vehicle_required or "Ambulance",\n        "include_ambulance_backup": bool(payload.include_ambulance_backup),\n        "status": "processing",'
)

content = content.replace(
    '"emergency_type": access_res.incident_report.incident_type.value,\n                "severity": access_res.incident_report.severity_estimate,',
    '"emergency_type": access_res.incident_report.incident_type.value,\n                "severity": access_res.incident_report.severity_estimate,\n                "vehicle_required": payload.vehicle_required or "Ambulance",\n                "include_ambulance_backup": bool(payload.include_ambulance_backup),'
)

with open(inc_file, "w", encoding="utf-8") as f:
    f.write(content)

# Touch main.py for uvicorn reload
with open("main.py", "r", encoding="utf-8") as f:
    m = f.read()
m += "\n# Reload for include_ambulance_backup schema update"
with open("main.py", "w", encoding="utf-8") as f:
    f.write(m)

print("Backend incident.py updated to persist include_ambulance_backup in citizen_view")

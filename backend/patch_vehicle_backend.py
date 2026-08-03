import sys

# 1. Update backend/routers/incident.py
inc_file = "routers/incident.py"
with open(inc_file, "r", encoding="utf-8") as f:
    content = f.read()

# Add vehicle_required to payload
content = content.replace(
    "class IncidentReportPayload(BaseModel):\n    citizen_text: str\n    citizen_name: str | None = \"Anonymous Citizen\"\n    citizen_phone: str | None = \"Unregistered\"",
    "class IncidentReportPayload(BaseModel):\n    citizen_text: str\n    citizen_name: str | None = \"Anonymous Citizen\"\n    citizen_phone: str | None = \"Unregistered\"\n    vehicle_required: str | None = \"Ambulance\""
)

# Attach vehicle_required to incident dict
content = content.replace(
    '        "citizen_phone": payload.citizen_phone or "Unregistered",\n        "status": "processing",',
    '        "citizen_phone": payload.citizen_phone or "Unregistered",\n        "vehicle_required": payload.vehicle_required or "Ambulance",\n        "status": "processing",'
)

with open(inc_file, "w", encoding="utf-8") as f:
    f.write(content)


# 2. Update backend/routers/driver.py
drv_file = "routers/driver.py"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

d_content = d_content.replace(
    '"assigned_driver": inc.get("assigned_driver"),',
    '"vehicle_required": inc.get("vehicle_required") or "Ambulance",\n                "assigned_driver": inc.get("assigned_driver"),'
)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("Backend incident.py and driver.py updated for multi-vehicle emergency dispatches")

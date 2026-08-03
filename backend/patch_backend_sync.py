import sys

# 1. Update FusionRequest schema to accept incident_id
schemas_file = "models/schemas.py"
with open(schemas_file, "r", encoding="utf-8") as f:
    s_content = f.read()

if "incident_id: Optional[str] = None" not in s_content:
    s_content = s_content.replace(
        "class FusionRequest(BaseModel):",
        "class FusionRequest(BaseModel):\n    incident_id: Optional[str] = None"
    )
    with open(schemas_file, "w", encoding="utf-8") as f:
        f.write(s_content)

# 2. Update decision_fusion.py to use request.incident_id if present
fusion_file = "agents/decision_fusion.py"
with open(fusion_file, "r", encoding="utf-8") as f:
    df_content = f.read()

df_content = df_content.replace(
    'incident_id = f"INC-{uuid.uuid4().hex[:8]}"',
    'incident_id = request.incident_id or f"INC-{uuid.uuid4().hex[:4]}"'
)

with open(fusion_file, "w", encoding="utf-8") as f:
    f.write(df_content)

# 3. Update incident.py to pass incident_id into FusionRequest
incident_file = "routers/incident.py"
with open(incident_file, "r", encoding="utf-8") as f:
    inc_content = f.read()

inc_content = inc_content.replace(
    "fusion_req = FusionRequest(",
    "fusion_req = FusionRequest(\n        incident_id=incident_id,"
)

with open(incident_file, "w", encoding="utf-8") as f:
    f.write(inc_content)

print("Backend incident ID synchronization patched successfully")

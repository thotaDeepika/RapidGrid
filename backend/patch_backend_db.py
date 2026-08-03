import sys

inc_file = "routers/incident.py"
with open(inc_file, "r", encoding="utf-8") as f:
    content = f.read()

# Add JSON disk persistence helpers
persistence_code = """import json
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
"""

if "incidents_db.json" not in content:
    content = content.replace(
        "ACTIVE_INCIDENTS: List[Dict[str, Any]] = []",
        "ACTIVE_INCIDENTS: List[Dict[str, Any]] = []\n\n" + persistence_code
    )

# Add clear endpoint
clear_endpoint = """@router.post("/clear")
async def clear_incidents():
    ACTIVE_INCIDENTS.clear()
    save_db()
    return {"status": "cleared"}"""

if "/clear" not in content:
    content += "\n\n" + clear_endpoint

# Call save_db() after pipeline runs, after report_incident, after approve_incident, after incident_arrived
content = content.replace("ACTIVE_INCIDENTS.append(incident)", "ACTIVE_INCIDENTS.append(incident)\n    save_db()")
content = content.replace("inc[\"status\"] = \"completed\"", "inc[\"status\"] = \"completed\"\n            save_db()")

# In run_pipeline and approve_incident, call save_db()
content = content.replace("inc[\"citizen_view\"] = {", "save_db()\n            inc[\"citizen_view\"] = {")

with open(inc_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Backend incident.py data persistence (JSON DB) patched successfully")

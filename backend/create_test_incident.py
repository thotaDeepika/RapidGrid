import json
import os

db_file = "data/incidents_db.json"

test_incidents = [
    {
        "incident_id": "INC-FIRE-99",
        "status": "dispatched",
        "citizen_text": "Commercial building fire near Bellary Road! Heavy smoke. Need Fire Engine Rescue Unit immediately.",
        "citizen_name": "Deepika",
        "citizen_phone": "+91 98765 43210",
        "vehicle_required": "Fire Engine",
        "emergency_type": "trauma",
        "severity": 0.85,
        "location": {"lat": 13.0325, "lng": 77.5836},
        "assigned_driver": "FIRE-ENGINE-09",
        "driver_claimed": True,
        "citizen_view": {
            "message": "Help is being dispatched. Approved Hospital: Aster CMI Hospital (Hebbal).",
            "eta_minutes": 5,
            "hospital_name": "Aster CMI Hospital (Hebbal)",
            "hospital_location": {"lat": 13.0473, "lng": 77.5908},
            "origin": {"lat": 13.0325, "lng": 77.5836},
            "route_coordinates": [
                {"lat": 13.0325, "lng": 77.5836},
                {"lat": 13.0380, "lng": 77.5860},
                {"lat": 13.0473, "lng": 77.5908}
            ],
            "distance_meters": 1800,
            "emergency_type": "trauma",
            "severity": 0.85,
            "vehicle_required": "Fire Engine"
        },
        "action_plan": {
            "recommended_hospital": {
                "hospital_id": "blr-007",
                "name": "Aster CMI Hospital (Hebbal)"
            }
        }
    }
]

with open(db_file, "w", encoding="utf-8") as f:
    json.dump(test_incidents, f, indent=2)

print("Created live test incident INC-FIRE-99 in data/incidents_db.json")

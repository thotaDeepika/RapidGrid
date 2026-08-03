import requests
import json

payload = {
  "incident_location": {
    "lat": 13.058869651460116,
    "lng": 77.60157338750626
  },
  "emergency_type": "trauma",
  "severity": 0.8,
  "vehicle_location": {"lat": 12.9716, "lng": 77.5946}
}

try:
    res = requests.post('http://localhost:8000/api/fusion/combine', json=payload)
    print("STATUS:", res.status_code)
    print("BODY:", json.dumps(res.json(), indent=2))
except Exception as e:
    print("Error:", e)

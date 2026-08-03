import httpx
import json
import asyncio

async def seed_test_incident():
    url = "http://localhost:8000/api/incidents"
    payload = {
        "citizen_text": "Commercial building electrical fire near Bellary Road! Heavy smoke. Need Fire Engine Rescue & Ambulance Unit standby.",
        "citizen_name": "Deepika",
        "citizen_phone": "+91 98765 43210",
        "vehicle_required": "Fire Engine",
        "location": {"lat": 13.0325, "lng": 77.5836},
        "input_modality": "text",
        "timestamp": "2026-08-03T18:24:00Z"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=payload)
        print("Test Incident API Response:", res.status_code, res.json())

asyncio.run(seed_test_incident())

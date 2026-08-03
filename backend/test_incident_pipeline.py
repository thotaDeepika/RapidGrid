import asyncio
from models.schemas import Coordinate
from routers.incident import IncidentReportPayload, run_pipeline, report_incident, Response

async def test_run():
    payload = IncidentReportPayload(
        citizen_text="burns and fire off help",
        citizen_name="Deepika",
        citizen_phone="1236547891",
        vehicle_required="Fire Engine",
        location=Coordinate(lat=12.9756, lng=77.6068)
    )
    resp = Response()
    res = await report_incident(payload, resp)
    print("Report incident success:", res)

try:
    asyncio.run(test_run())
except Exception as e:
    import traceback
    traceback.print_exc()

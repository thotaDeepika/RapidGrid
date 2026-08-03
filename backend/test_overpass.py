"""
Quick end-to-end test of the hospital agent + fusion engine
without needing the full FastAPI server.
"""
import asyncio
import sys
sys.path.insert(0, '.')

async def main():
    from models.schemas import Coordinate, EmergencyType, HospitalRequest
    from agents.hospital_intelligence import hospital_agent

    print("=== Testing Hospital Intelligence Agent ===")
    print("Location: MG Road, Bangalore (12.9756, 77.6068)")
    print("Emergency: CARDIAC\n")

    req = HospitalRequest(
        incident_location=Coordinate(lat=12.9756, lng=77.6068),
        emergency_type=EmergencyType.CARDIAC,
    )

    result = await hospital_agent.rank_hospitals(req)
    print(f"Ranked {len(result.ranked_hospitals)} hospitals (weights: {result.weights_used}):\n")
    for i, h in enumerate(result.ranked_hospitals, 1):
        print(f"{i}. {h.name}")
        print(f"   Score: {h.score:.3f} | ICU: {h.icu_available} beds")
        print(f"   Location: ({h.location.lat:.4f}, {h.location.lng:.4f})")
        print(f"   {h.reasoning[:120]}...")
        print()

asyncio.run(main())

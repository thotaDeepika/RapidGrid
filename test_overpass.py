import asyncio
import httpx

async def run():
    query = """
    [out:json];
    node(around:7000, 13.058869, 77.601573)["amenity"="hospital"];
    out;
    """
    res = await httpx.AsyncClient().post('https://overpass-api.de/api/interpreter', data={"data": query})
    print("STATUS:", res.status_code)
    try:
        data = res.json()
        print("COUNT:", len(data.get("elements", [])))
    except:
        print("TEXT:", res.text)

asyncio.run(run())

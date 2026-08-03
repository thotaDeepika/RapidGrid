"""
Route Optimization Agent for GeoAgentic (Live Version).

Contract (from agent-contracts.md):
  Input:  {origin, destination, vehicle_type, blocked_segments[],
           traffic_snapshot}
  Output: {route_id, coordinates[], distance, eta, delay_probability,
           alternate_routes[], selection_reason, confidence}

Implementation:
  - Calls Google Routes API (v2) for live traffic-aware routing.
  - Decodes GeoJSON linestring into Coordinates.
"""

from __future__ import annotations

import logging
import os
import uuid
import httpx
from typing import Any

from bus.event_bus import ROUTE_COMPUTED, ROUTE_REQUEST, bus
from models.schemas import (
    Coordinate,
    DataFreshness,
    Event,
    RouteRequest,
    RouteResponse,
)

logger = logging.getLogger("geoagentic.agent.route")

AGENT_NAME = "route_optimization"


class RouteOptimizationAgent:
    """Live routing via Google Routes API."""

    def __init__(self) -> None:
        self._loaded = True
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_ROUTES_API_KEY")

    def load_network(
        self,
        nodes: dict[str, dict[str, Any]],
        edges: list[dict[str, Any]],
    ) -> None:
        """No-op for live API."""
        pass

    def register_on_bus(self) -> None:
        """No-op for live API. We no longer listen to local traffic events."""
        pass

    def compute_route(self, request: RouteRequest) -> RouteResponse:
        """
        Compute the optimal route using Google Routes API.
        """
        if not self.api_key:
            logger.error("Missing GOOGLE_ROUTES_API_KEY")
            return self._fallback_route(request)

        url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.geoJsonLinestring"
        }
        
        payload = {
            "origin": {
                "location": {
                    "latLng": {
                        "latitude": request.origin.lat,
                        "longitude": request.origin.lng
                    }
                }
            },
            "destination": {
                "location": {
                    "latLng": {
                        "latitude": request.destination.lat,
                        "longitude": request.destination.lng
                    }
                }
            },
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
            "polylineEncoding": "GEO_JSON_LINESTRING"
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                resp = client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Google API HTTP error: {e.response.text}")
            return self._fallback_route(request)
        except Exception as e:
            logger.error(f"Failed to fetch route from Google: {e}")
            return self._fallback_route(request)

        routes = data.get("routes", [])
        if not routes:
            return self._fallback_route(request)
            
        route_data = routes[0]
        
        duration_str = route_data.get("duration", "0s").replace("s", "")
        eta = float(duration_str)
        
        distance = float(route_data.get("distanceMeters", 0))
        
        geojson = route_data.get("polyline", {}).get("geoJsonLinestring", {}).get("coordinates", [])
        coords = [Coordinate(lat=c[1], lng=c[0]) for c in geojson]
        
        reason = (
            f"Primary route via Google Maps Live Traffic. "
            f"Estimated travel time: {eta:.0f}s, distance: {distance:.0f}m."
        )

        return RouteResponse(
            route_id=f"R-{uuid.uuid4().hex[:8]}",
            coordinates=coords,
            distance=round(distance, 1),
            eta=round(eta, 1),
            delay_probability=0.1,
            alternate_routes=[],
            selection_reason=reason,
            data_freshness=DataFreshness.LIVE,
            confidence=0.95,
            node_ids=[],
            edge_ids=[],
        )

    def _fallback_route(self, request: RouteRequest) -> RouteResponse:
        """Fallback if API fails."""
        return RouteResponse(
            route_id=f"R-{uuid.uuid4().hex[:8]}",
            coordinates=[request.origin, request.destination],
            distance=0.0,
            eta=0.0,
            delay_probability=1.0,
            alternate_routes=[],
            selection_reason="Failed to compute route via Google Maps.",
            data_freshness=DataFreshness.CACHED,
            confidence=0.0,
            node_ids=[],
            edge_ids=[]
        )

route_agent = RouteOptimizationAgent()

import math

EMERGENCY_HUBS = {
    "Ambulance": [
        {"id": "AMB-HUB-01", "name": "Aster CMI Emergency Ambulance Hub", "lat": 13.0473, "lng": 77.5908},
        {"id": "AMB-HUB-02", "name": "Manipal Ambulance Base Depot", "lat": 12.9585, "lng": 77.6483},
        {"id": "AMB-HUB-03", "name": "Victoria Hospital Paramedic Base", "lat": 12.9634, "lng": 77.5746},
    ],
    "Fire Engine": [
        {"id": "FIRE-HUB-01", "name": "Hebbal Fire & Rescue Station #4", "lat": 13.0336, "lng": 77.5891},
        {"id": "FIRE-HUB-02", "name": "High Grounds Central Fire Station", "lat": 12.9866, "lng": 77.5878},
        {"id": "FIRE-HUB-03", "name": "Jayanagar Emergency Fire Station", "lat": 12.9298, "lng": 77.5831},
    ],
    "Police Cruiser": [
        {"id": "POLICE-HUB-01", "name": "Hebbal Police Patrol Base", "lat": 13.0350, "lng": 77.5880},
        {"id": "POLICE-HUB-02", "name": "Central MG Road Police Precinct", "lat": 12.9754, "lng": 77.6071},
        {"id": "POLICE-HUB-03", "name": "Cubbon Park Traffic Police Hub", "lat": 12.9740, "lng": 77.5930},
    ],
    "Disaster Rescue": [
        {"id": "DISASTER-HUB-01", "name": "NDRF Disaster Rescue Hub North", "lat": 13.0550, "lng": 77.6120},
        {"id": "DISASTER-HUB-02", "name": "Civil Defence Emergency Depot", "lat": 12.9600, "lng": 77.6000},
    ]
}

def haversine_dist(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def find_nearest_hub(vehicle_type, citizen_lat, citizen_lng):
    hubs = EMERGENCY_HUBS.get(vehicle_type) or EMERGENCY_HUBS["Ambulance"]
    best_hub = hubs[0]
    min_dist = haversine_dist(citizen_lat, citizen_lng, best_hub["lat"], best_hub["lng"])
    for h in hubs[1:]:
        d = haversine_dist(citizen_lat, citizen_lng, h["lat"], h["lng"])
        if d < min_dist:
            min_dist = d
            best_hub = h
    return best_hub

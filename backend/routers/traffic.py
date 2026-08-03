"""
Traffic Intelligence API router.

Endpoints:
  GET  /api/traffic/status              — current traffic for all segments
  POST /api/traffic/analyse             — trigger analysis for a bounding box
  GET  /api/traffic/segment/{segment_id} — traffic for a specific segment
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from agents.traffic_intelligence import traffic_agent
from models.schemas import TrafficRequest, TrafficSegment, TrafficSnapshot

router = APIRouter(prefix="/api/traffic", tags=["Traffic Intelligence"])


@router.get(
    "/status",
    response_model=TrafficSnapshot,
    summary="Get current traffic status for all road segments",
)
async def get_traffic_status() -> TrafficSnapshot:
    """
    Returns the latest traffic snapshot for the entire loaded network.

    In production this would serve the most recent snapshot from the
    event bus cache; here it runs a fresh analysis on each call.
    """
    return traffic_agent.get_snapshot()


@router.post(
    "/analyse",
    response_model=TrafficSnapshot,
    summary="Trigger a traffic analysis (optionally scoped to a bounding box)",
)
async def analyse_traffic(request: TrafficRequest) -> TrafficSnapshot:
    """
    Analyse traffic conditions and publish a TRAFFIC_UPDATE event.

    Optionally scope the analysis to a geographic bounding box.
    """
    bbox = request.bounding_box
    await traffic_agent.publish_snapshot(bbox)
    return traffic_agent.get_snapshot(bbox)


@router.get(
    "/segment/{segment_id}",
    response_model=TrafficSegment,
    summary="Get traffic status for a specific road segment",
)
async def get_segment(segment_id: str) -> TrafficSegment:
    """Return traffic data for a single road segment by ID."""
    snapshot = traffic_agent.get_snapshot()
    for segment in snapshot.segments:
        if segment.segment_id == segment_id:
            return segment
    raise HTTPException(
        status_code=404,
        detail=f"Segment '{segment_id}' not found in the loaded network.",
    )

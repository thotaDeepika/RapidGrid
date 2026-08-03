"""
Emergency Coordinator API router.

Endpoints:
  POST /api/coordinator/coordinate — Orchestrate an incident
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from agents.coordinator import coordinator_agent
from models.schemas import CoordinatorRequest, CoordinatorResponse

router = APIRouter(prefix="/api/coordinator", tags=["Emergency Coordinator"])


@router.post(
    "/coordinate",
    response_model=CoordinatorResponse,
    summary="Coordinate an incident and determine agent activation",
)
async def coordinate_incident(request: CoordinatorRequest) -> CoordinatorResponse:
    """
    Acts as the entrypoint for an incident. Evaluates severity and determines
    which agents to activate (e.g. skips Hospital Intelligence for minor incidents).
    """
    try:
        return await coordinator_agent.coordinate(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

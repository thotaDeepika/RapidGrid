"""
Accessibility Agent API router.

Endpoints:
  POST /api/accessibility/report  — submit an emergency report via any modality
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from agents.accessibility import accessibility_agent
from models.schemas import AccessibilityRequest, AccessibilityResponse

router = APIRouter(prefix="/api/accessibility", tags=["Accessibility Agent"])


@router.post(
    "/report",
    response_model=AccessibilityResponse,
    summary="Report an emergency using any input modality",
)
async def report_emergency(request: AccessibilityRequest) -> AccessibilityResponse:
    """
    Submit an emergency report using raw input from any modality (e.g. text,
    voice transcript, mocked sign language descriptor, or SOS button tap).

    The Accessibility Agent normalizes the input into a standard IncidentReport
    structure that the Decision Fusion Engine can consume, ensuring that
    accessible input methods are fully integrated, not second-class citizens.
    """
    try:
        return await accessibility_agent.process_input(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

"""
Decision Fusion Engine for GeoAgentic.

Contract (from agent-contracts.md):
  Input:  all active agents' latest outputs for one incident.
  Output: {recommended_route, recommended_hospital, factor_breakdown:
           {response_time_weight, traffic_weight, hospital_weight,
            severity_weight, accessibility_weight},
           explanation, overall_confidence}

  factor_breakdown and explanation are NOT optional — this is what makes
  the system explainable rather than a black box.

The five fusion dimensions (from geoagentic-architecture SKILL.md):
  1. Response time   — from Route Optimization Agent (ETA, delay probability)
  2. Traffic          — from Traffic Intelligence Agent (congestion, incidents)
  3. Hospital         — from Hospital Intelligence Agent (resource score)
  4. Severity         — from the incident's classified severity
  5. Accessibility    — from the Accessibility Agent (placeholder for now)

Weights are tunable per emergency type.  Never collapse fusion into a
single opaque score with no per-agent breakdown in the output.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from agents.hospital_intelligence import hospital_agent
from agents.prediction import prediction_agent
from agents.route_optimization import route_agent
from agents.traffic_intelligence import traffic_agent
from bus.event_bus import FUSION_COMPLETE, bus
from models.schemas import (
    Coordinate,
    DataFreshness,
    EmergencyType,
    FactorWeight,
    FusionRequest,
    FusionResponse,
    HospitalRequest,
    RouteRequest,
)

logger = logging.getLogger("geoagentic.fusion")

AGENT_NAME = "decision_fusion_engine"


# ---------------------------------------------------------------------------
# Fusion weight tables — tunable per emergency type
# ---------------------------------------------------------------------------
# These are the *fusion-level* weights (combining agents' outputs), distinct
# from the hospital-scoring weights (which are internal to Hospital
# Intelligence).  Higher severity → more weight on response time.

FUSION_WEIGHTS: dict[str, dict[str, float]] = {
    "general": {
        "response_time": 0.30,
        "traffic":       0.20,
        "hospital":      0.25,
        "severity":      0.15,
        "accessibility": 0.10,
    },
    "cardiac": {
        "response_time": 0.25,
        "traffic":       0.15,
        "hospital":      0.35,  # hospital capability critical for cardiac
        "severity":      0.15,
        "accessibility": 0.10,
    },
    "trauma": {
        "response_time": 0.35,  # time-critical
        "traffic":       0.20,
        "hospital":      0.25,
        "severity":      0.10,
        "accessibility": 0.10,
    },
    "stroke": {
        "response_time": 0.30,  # very time-sensitive
        "traffic":       0.15,
        "hospital":      0.30,  # neurology/imaging availability
        "severity":      0.15,
        "accessibility": 0.10,
    },
}


# ---------------------------------------------------------------------------
# DecisionFusionEngine
# ---------------------------------------------------------------------------

class DecisionFusionEngine:
    """
    Combines each agent's independent recommendation into one explainable
    action plan along five weighted dimensions.
    """

    def async_fuse(self):
        """Placeholder for bus-driven fusion — not used in REST flow."""
        pass

    async def fuse(self, request: FusionRequest) -> FusionResponse:
        """
        Orchestrate all three agents and fuse their outputs.

        Steps:
          1. Run Traffic Intelligence for the incident area.
          2. Run Hospital Intelligence to rank hospitals.
          3. Pick the top hospital's node as the routing destination.
          4. Run Route Optimization from vehicle to hospital.
          5. Score each of the five fusion dimensions.
          6. Build factor_breakdown and explanation.
          7. Publish FUSION_COMPLETE to the bus.
        """
        incident_id = request.incident_id or f"INC-{uuid.uuid4().hex[:4]}"
        etype = request.emergency_type.value
        weights = FUSION_WEIGHTS.get(etype, FUSION_WEIGHTS["general"])

        logger.info(
            "Fusion started for %s — %s emergency, severity=%.2f",
            incident_id, etype, request.severity,
        )

        # -- 1. Traffic Intelligence ------------------------------------------
        traffic_snapshot = traffic_agent.get_snapshot()
        traffic_segments = traffic_snapshot.segments

        # Aggregate traffic score: average congestion across all segments
        # 0 = all clear, 1 = all gridlocked
        avg_congestion = (
            sum(s.congestion_score for s in traffic_segments) / len(traffic_segments)
            if traffic_segments else 0.0
        )
        # Invert: high congestion → low traffic score (bad conditions)
        traffic_score = round(1.0 - avg_congestion, 3)
        traffic_confidence = (
            sum(s.confidence for s in traffic_segments) / len(traffic_segments)
            if traffic_segments else 0.5
        )

        # Count active incidents and closures for the explanation
        total_incidents = sum(len(s.incidents) for s in traffic_segments)
        total_closures = sum(len(s.closures) for s in traffic_segments)

        logger.info(
            "Traffic: avg_congestion=%.3f, score=%.3f, incidents=%d, closures=%d",
            avg_congestion, traffic_score, total_incidents, total_closures,
        )

        # -- 2. Hospital Intelligence ----------------------------------------
        hospital_request = HospitalRequest(
            incident_location=request.incident_location,
            emergency_type=request.emergency_type,
            patient_info=request.patient_info,
        )
        hospital_result = await hospital_agent.rank_hospitals(hospital_request)
        top_hospital = hospital_result.ranked_hospitals[0]

        # Hospital score for fusion = the top hospital's weighted score
        hospital_score = round(top_hospital.score, 3)
        hospital_confidence = top_hospital.confidence

        logger.info(
            "Hospital: top=%s (score=%.3f), %d candidates ranked",
            top_hospital.hospital_id, hospital_score,
            len(hospital_result.ranked_hospitals),
        )

        # -- 3. Determine routing destination ---------------------------------
        # We now use the exact hospital coordinates directly
        destination_node = top_hospital.location

        # -- 4. Route Optimization --------------------------------------------
        route_request = RouteRequest(
            origin=request.vehicle_location,
            destination=destination_node,
            vehicle_type=request.vehicle_type,
        )
        route_result = route_agent.compute_route(route_request)

        # Track this route in the Prediction Agent to receive live ETA updates
        prediction_agent.track_route(route_result)
        
        # Pull live weather impact on the ETA
        from models.schemas import PredictionRequest
        pred_req = PredictionRequest(target_id=route_result.route_id, route_details=route_result)
        pred_res = await prediction_agent.predict_on_demand(pred_req)
        
        # Override ETA with the weather-adjusted ETA
        route_result.eta = pred_res.eta_estimate

        # Response time score: inverse of ETA, normalised
        # Lower ETA → higher score.  Max reasonable = 1800s (30 min).
        max_eta = 1800.0
        response_time_score = round(
            max(0.0, min(1.0, 1.0 - (route_result.eta / max_eta))), 3
        )
        route_confidence = route_result.confidence

        logger.info(
            "Route: %s, ETA=%.0fs, response_time_score=%.3f",
            route_result.route_id, route_result.eta, response_time_score,
        )

        # -- 5. Severity score ------------------------------------------------
        # Directly from the classified severity — higher severity means the
        # situation demands faster action (already 0–1).
        severity_score = round(request.severity, 3)

        # -- 6. Accessibility score -------------------------------------------
        # Placeholder until the Accessibility Agent is implemented.
        # Default to 0.8 (assume standard accessibility met).
        if request.accessibility_needs:
            # If needs are specified, score lower to flag that extra
            # accommodation is required in the action plan
            accessibility_score = 0.6
            accessibility_confidence = 0.7
        else:
            accessibility_score = 0.8
            accessibility_confidence = 0.85

        # -- 7. Build factor breakdown ----------------------------------------
        factor_data = [
            {
                "factor": "response_time",
                "label": "Response Time",
                "weight": weights["response_time"],
                "score": response_time_score,
                "agent": "route_optimization",
                "confidence": route_confidence,
            },
            {
                "factor": "traffic",
                "label": "Traffic Conditions",
                "weight": weights["traffic"],
                "score": traffic_score,
                "agent": "traffic_intelligence",
                "confidence": traffic_confidence,
            },
            {
                "factor": "hospital",
                "label": "Hospital Availability",
                "weight": weights["hospital"],
                "score": hospital_score,
                "agent": "hospital_intelligence",
                "confidence": hospital_confidence,
            },
            {
                "factor": "severity",
                "label": "Emergency Severity",
                "weight": weights["severity"],
                "score": severity_score,
                "agent": "emergency_coordinator",
                "confidence": 0.90,  # severity classification confidence
            },
            {
                "factor": "accessibility",
                "label": "Accessibility",
                "weight": weights["accessibility"],
                "score": accessibility_score,
                "agent": "accessibility",
                "confidence": accessibility_confidence,
            },
        ]

        factor_breakdown: list[FactorWeight] = []
        weighted_total = 0.0
        confidence_weighted_sum = 0.0

        for fd in factor_data:
            weighted = round(fd["weight"] * fd["score"], 4)
            weighted_total += weighted
            confidence_weighted_sum += fd["weight"] * fd["confidence"]

            factor_breakdown.append(FactorWeight(
                factor=fd["label"],
                weight=fd["weight"],
                score=fd["score"],
                weighted_score=weighted,
                contributing_agent=fd["agent"],
                agent_confidence=fd["confidence"],
            ))

        overall_confidence = round(confidence_weighted_sum, 3)

        # -- 8. Build explanation ---------------------------------------------
        explanation = self._build_explanation(
            incident_id=incident_id,
            etype=etype,
            severity=request.severity,
            top_hospital=top_hospital,
            route=route_result,
            factor_breakdown=factor_breakdown,
            weighted_total=weighted_total,
            traffic_score=traffic_score,
            total_incidents=total_incidents,
            total_closures=total_closures,
        )

        # -- 9. Assemble response ---------------------------------------------
        response = FusionResponse(
            incident_id=incident_id,
            recommended_route=route_result,
            recommended_hospital=top_hospital,
            factor_breakdown=factor_breakdown,
            explanation=explanation,
            overall_confidence=min(overall_confidence, 1.0),
            emergency_type=request.emergency_type,
            severity=request.severity,
            data_freshness=DataFreshness.LIVE,
            all_hospitals=hospital_result.ranked_hospitals,
            alternate_routes=route_result.alternate_routes,
        )

        # -- 10. Publish to bus -----------------------------------------------
        await bus.publish(
            topic=FUSION_COMPLETE,
            payload=response.model_dump(mode="json"),
            source_agent=AGENT_NAME,
        )

        logger.info(
            "Fusion complete for %s — overall_confidence=%.3f, "
            "route=%s (ETA %.0fs), hospital=%s (%s)",
            incident_id, overall_confidence,
            route_result.route_id, route_result.eta,
            top_hospital.hospital_id, top_hospital.name,
        )

        # Broadcast the final action plan for downstream agents (e.g., Communication)
        await bus.publish(
            topic=FUSION_COMPLETE,
            payload=response.model_dump(mode="json"),
            source_agent=AGENT_NAME,
        )

        return response

    # -- helpers --------------------------------------------------------------


    def _build_explanation(
        self,
        incident_id: str,
        etype: str,
        severity: float,
        top_hospital: Any,
        route: Any,
        factor_breakdown: list[FactorWeight],
        weighted_total: float,
        traffic_score: float,
        total_incidents: int,
        total_closures: int,
    ) -> str:
        """
        Build a plain-language explanation of the fused decision.

        From SKILL.md: "A dispatcher must be able to see WHY a route or
        hospital was chosen, not just WHAT was chosen."
        """
        severity_label = (
            "critical" if severity >= 0.8
            else "high" if severity >= 0.6
            else "moderate" if severity >= 0.4
            else "low"
        )

        # Sort factors by weighted contribution
        sorted_factors = sorted(
            factor_breakdown, key=lambda f: f.weighted_score, reverse=True,
        )
        top_two = sorted_factors[:2]

        parts = [
            f"Action plan for incident {incident_id} "
            f"({etype} emergency, {severity_label} severity).",
        ]

        # Route reasoning
        parts.append(
            f"ROUTE: {route.selection_reason} "
            f"ETA: {route.eta:.0f}s, distance: {route.distance:.0f}m."
        )

        # Hospital reasoning
        parts.append(
            f"HOSPITAL: {top_hospital.name} selected "
            f"(score {top_hospital.score:.3f}). {top_hospital.reasoning}"
        )

        # Traffic conditions
        if total_incidents > 0 or total_closures > 0:
            parts.append(
                f"TRAFFIC: {total_incidents} active incident(s), "
                f"{total_closures} road closure(s). "
                f"Overall traffic score: {traffic_score:.2f}/1.00."
            )
        else:
            parts.append(
                f"TRAFFIC: No active incidents or closures. "
                f"Traffic score: {traffic_score:.2f}/1.00."
            )

        # Fusion rationale
        factor_desc = " and ".join(
            f"{f.factor} ({f.weighted_score:.3f})" for f in top_two
        )
        parts.append(
            f"FUSION: Decision driven primarily by {factor_desc}. "
            f"Combined weighted score: {weighted_total:.3f}."
        )

        return " ".join(parts)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

fusion_engine = DecisionFusionEngine()

# Agent Contracts

Every agent communicates only through the event bus using these contracts.
Never have one agent call another agent's internals directly — publish an
event, let the Decision Fusion Engine (or Coordinator) consume it.

## Emergency Coordinator
**Input**: incident report (raw, from any citizen channel), timestamp.
**Output**: `{incident_id, severity, activated_agents[], status}`.
Responsibility: classify severity, decide which agents to activate (not
every incident needs every agent — e.g. a minor incident may skip
Hospital Intelligence), compile the final action plan once fusion
completes.

## Traffic Intelligence
**Input**: geographic bounding box, time window.
**Output**: `{segment_id, congestion_score, incidents[], closures[],
weather_risk, data_freshness, confidence}`.
Must run continuously, not just once per incident — Route Optimization and
Prediction subscribe to updates.

## Route Optimization
**Input**: `{origin, destination, vehicle_type, blocked_segments[],
traffic_snapshot}`.
**Output**: `{route_id, coordinates[], distance, eta, delay_probability,
alternate_routes[], selection_reason, confidence}`.
Must always return at least one alternate route. Must never return a
blocked or legally restricted segment. See `emergency-routing` skill for
implementation detail.

## Prediction
**Input**: `{route_id or segment_id, historical_data, current_traffic}`.
**Output**: `{eta_estimate, delay_probability, confidence_interval,
model_version}`.
Refreshes continuously as conditions change — treat ETA as a live stream,
not a one-time calculation.

## Hospital Intelligence
**Input**: `{incident_location, emergency_type, patient_info?}`.
**Output**: `{ranked_hospitals: [{hospital_id, score, reasoning,
icu_available, specialists[], blood_availability}], data_freshness}`.
Never rank by distance alone. See `hospital-intelligence` skill.

## Accessibility
**Input**: raw citizen input via any modality (voice, sign-language video,
text, SOS button, symbol tap).
**Output**: normalised `{incident_report, citizen_accessibility_profile,
input_modality, confidence}` — this feeds the Emergency Coordinator like
any other report, plus the accessibility profile feeds Decision Fusion.
See `accessibility-first` skill.

## Communication
**Input**: approved action plan.
**Output**: delivery receipts per channel `{recipient, channel, status,
timestamp}` (hospital, driver, police, family, traffic control).
Never blocks the critical path — dispatch proceeds even if a notification
channel fails; log and retry failures separately.

## Learning
**Input**: closed-case outcomes (actual vs predicted ETA, actual vs
recommended hospital/route, dispatcher overrides).
**Output**: model update proposals / retrained model artifacts — never
auto-deploys a new model without a review/approval step in a demo build.

## Decision Fusion Engine
**Input**: all active agents' latest outputs for one incident.
**Output**: `{recommended_route, recommended_hospital, factor_breakdown:
{response_time_weight, traffic_weight, hospital_weight, severity_weight,
accessibility_weight}, explanation, overall_confidence}`.
`factor_breakdown` and `explanation` are not optional — this is what makes
the system explainable rather than a black box. See
`hospital-intelligence/references/hospital-scoring.md` for a worked
weighting example to model the pattern on.

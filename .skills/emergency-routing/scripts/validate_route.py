"""
validate_route.py

Lightweight, dependency-free validator for a Route Optimization Agent's
output shape (see emergency-routing/SKILL.md "Output contract" and
geoagentic-architecture/references/agent-contracts.md).

Usage:
    from validate_route import validate_route_response
    errors = validate_route_response(response_dict)
    assert not errors, errors

This does NOT validate routing correctness (shortest path, blocked-road
avoidance) — it only checks the output contract shape, so it's cheap to
run in unit tests as a first line of defence before deeper scenario tests
(see the geoagentic-testing skill for those).
"""

REQUIRED_FIELDS = {
    "route_id": str,
    "coordinates": list,
    "distance": (int, float),
    "eta": (int, float),
    "delay_probability": (int, float),
    "alternate_routes": list,
    "selection_reason": str,
    "data_freshness": str,
    "confidence": (int, float),
}


def validate_route_response(response: dict) -> list[str]:
    errors = []

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in response:
            errors.append(f"missing required field: {field}")
            continue
        if not isinstance(response[field], expected_type):
            errors.append(
                f"field '{field}' has wrong type: "
                f"expected {expected_type}, got {type(response[field])}"
            )

    if "coordinates" in response and isinstance(response["coordinates"], list):
        if len(response["coordinates"]) < 2:
            errors.append("coordinates must contain at least 2 points (origin + destination)")

    if "alternate_routes" in response and isinstance(response["alternate_routes"], list):
        if len(response["alternate_routes"]) < 1:
            errors.append("must include at least one alternate route")

    if "confidence" in response and isinstance(response["confidence"], (int, float)):
        if not (0 <= response["confidence"] <= 1):
            errors.append("confidence must be between 0 and 1")

    if "delay_probability" in response and isinstance(response["delay_probability"], (int, float)):
        if not (0 <= response["delay_probability"] <= 1):
            errors.append("delay_probability must be between 0 and 1")

    if response.get("data_freshness") not in (None, "live", "cached", "stale"):
        errors.append("data_freshness should be one of: live, cached, stale")

    return errors


if __name__ == "__main__":
    # Smoke test with a deliberately incomplete response
    example = {
        "route_id": "R1",
        "coordinates": [[12.9716, 77.5946], [12.99, 77.62]],
        "distance": 4200,
        "eta": 420,
        # missing delay_probability, alternate_routes, etc. on purpose
        "confidence": 0.82,
    }
    found = validate_route_response(example)
    print(f"Found {len(found)} issue(s):")
    for e in found:
        print(f" - {e}")

---
name: emergency-routing
description: >
  Design, implement, review, and test ambulance/emergency-vehicle routing
  features for GeoAgentic. Use this skill whenever working on route
  optimisation, congestion-aware routing, ETA calculation, road closures,
  alternate routes, dynamic rerouting, or green-corridor recommendations —
  including the Route Optimization Agent and the Prediction Agent's ETA
  logic. Make sure to consult this even for small changes like tweaking an
  edge-cost multiplier or adding a new blocked-road check.
---

# GeoAgentic — Emergency Routing

Implements the Route Optimization Agent (and feeds the Prediction Agent).
Read `geoagentic-architecture`'s `agent-contracts.md` first for the exact
I/O shape this agent must produce.

## Core requirements

1. Optimise for **emergency response time**, not geographical distance alone.
2. Consider live congestion, road closures, accidents, weather, and road risk.
3. Return one recommended route **and at least one valid alternate route**.
4. Recalculate the route whenever a significant road condition changes.
5. Every route includes ETA, distance, delay probability, and a
   plain-language reason for selection.
6. Never recommend a blocked or legally restricted road.
7. Clearly mark simulated/mock data whenever live data is unavailable.
8. Preserve dispatcher approval for high-impact rerouting decisions (see
   architecture skill, workflow step 8) — auto-reroute is fine for minor
   adjustments, but a major detour should surface for dispatcher review.

## Input contract

- vehicle coordinates
- incident coordinates
- selected hospital coordinates
- emergency severity
- live road conditions
- blocked road segments
- vehicle type
- timestamp

## Output contract

- route identifier
- ordered coordinates
- estimated distance
- estimated travel time
- delay probability
- alternate routes
- route-selection explanation
- data freshness
- confidence score

## Implementation guidance

Use a weighted road graph. A starting edge cost:

```
edge_cost = travel_time
          × congestion_multiplier
          × incident_multiplier
          × weather_multiplier
```

Document every assumed multiplier's default value and source (e.g. "1.4x
for rain, from historical average slowdown" — don't leave magic numbers
unexplained). Run A* or time-dependent Dijkstra over the weighted graph;
time-dependent shortest path is preferred once you have more than a
static snapshot of traffic, since edge costs change as the ambulance
moves through the network.

See `references/route-scoring.md` for the full scoring formula and how it
interacts with the Decision Fusion Engine's weighting, and
`references/sample-road-network.json` for a small graph you can develop
and test against without needing live map data.

## Failure handling

When live traffic APIs fail:

1. Use the latest cached traffic snapshot.
2. Mark the result as degraded (`data_freshness: "stale"` /
   `confidence` lowered accordingly).
3. Notify the dispatcher that routing is running on cached data.
4. Continue using static road and historical traffic data rather than
   blocking route generation entirely — a stale route beats no route.

## Validation

Before considering a routing change complete, test:

- an empty/impossible route (no path exists)
- blocked roads (including a case where the only route is blocked)
- API timeout / traffic-source unavailable
- rerouting mid-journey
- multiple equal-cost routes (tie-breaking behaviour)
- invalid coordinates
- unavailable destination hospital (route target changes mid-flight)

Use `scripts/validate_route.py` as a starting point for automating these
checks against a route-generation function's output shape.

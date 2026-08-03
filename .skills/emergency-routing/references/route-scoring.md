# Route Scoring

## Edge cost

```
edge_cost = travel_time
          × congestion_multiplier   (default 1.0–2.5, from live/historical traffic)
          × incident_multiplier     (default 1.0 clear, 3.0+ near an active incident)
          × weather_multiplier      (default 1.0 clear, 1.2–1.6 rain/fog, 2.0+ severe)
```

`congestion_multiplier` and `incident_multiplier` should come from the
Traffic Intelligence Agent's live output when available, falling back to
historical averages (time-of-day, day-of-week) when live data is stale —
mark `data_freshness` accordingly (see SKILL.md failure handling).

## Route selection

1. Compute shortest-cost path (A* or time-dependent Dijkstra) as the
   primary route.
2. Compute at least one alternate: either the next-lowest-cost distinct
   path, or a path that trades a small time penalty for lower variance
   (e.g. avoids a segment with high incident_multiplier volatility) — the
   alternate should be genuinely useful, not a near-duplicate of the
   primary route.
3. `selection_reason` should name the deciding factor in plain language,
   e.g. "Primary route avoids the MG Road closure and current accident on
   Hosur Road; 3 minutes faster than the alternate despite being 1.2km
   longer."

## Interaction with Decision Fusion

Route Optimization's output is one input among several to the Decision
Fusion Engine (see `geoagentic-architecture/references/agent-contracts.md`).
Don't try to fold hospital or accessibility weighting into route scoring
itself — keep this agent's scoring purely about traffic/road-network cost,
and let the fusion engine combine it with the other agents' outputs.

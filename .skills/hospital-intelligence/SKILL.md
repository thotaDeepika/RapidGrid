---
name: hospital-intelligence
description: >
  Design, implement, and review hospital-selection/ranking logic for
  GeoAgentic's Hospital Intelligence Agent. Use this skill whenever
  working on hospital ranking, ICU/ER/bed availability, specialist or
  blood-availability matching, or emergency-type-specific weighting (e.g.
  cardiac vs trauma vs stroke). This is one of GeoAgentic's key
  differentiators — never let generated code fall back to "nearest
  hospital by distance" without the full weighted score.
---

# GeoAgentic — Hospital Intelligence

Implements the Hospital Intelligence Agent. The differentiator this skill
protects: **hospital selection must be based on real medical resource
availability, not proximity alone.** See
`geoagentic-architecture/references/agent-contracts.md` for this agent's
exact I/O contract.

## Core requirement

Never rank or recommend a hospital using distance/travel-time as the sole
factor. Every ranking must combine multiple weighted factors, and every
recommendation must include a `reasoning` string a dispatcher can read
and trust.

## Default scoring formula

```
Hospital Score = 0.30 × travel-time score
               + 0.25 × emergency-resource score
               + 0.20 × specialist-availability score
               + 0.15 × bed-availability score
               + 0.10 × blood-availability score
```

These weights are the **general-emergency default**, not fixed — they
must shift by emergency type. See `references/hospital-scoring.md` for
worked weight tables per emergency type (cardiac, major
accident/trauma, stroke) and for how each sub-score (0–1 scale) should be
computed from raw hospital data.

## Input contract

- incident location
- emergency type (cardiac / trauma / stroke / general / etc.)
- patient info, if available (age, known conditions — treat as optional
  and handle its absence gracefully, don't require it)

## Output contract

- ranked list of hospitals, each with: hospital_id, overall score,
  human-readable reasoning, ICU availability, specialist list, blood
  availability
- data freshness for the underlying hospital-status data

## Implementation guidance

1. Pull the relevant weight table for the given `emergency_type` from
   `references/hospital-scoring.md` (default to the general-emergency
   weights if the type is unrecognised — never crash on an unknown type).
2. Compute each sub-score in the 0–1 range so weights combine cleanly.
3. Sort descending by overall score; return the full ranked list, not
   just the top choice — the Decision Fusion Engine and dispatcher may
   want to see runner-ups, and a runner-up may be chosen if the top
   choice's status changes after dispatch (see geoagentic-testing
   Scenario 7).
4. Always populate `reasoning` from the actual sub-scores that drove the
   result (e.g. "Selected for cardiology availability and bed capacity;
   1.5km further than the nearest hospital, which lacks a cath lab.") —
   never a generic placeholder string.

## Failure handling

If hospital-status data is stale or a hospital's API is unreachable,
mark that hospital's entry with `data_freshness: "stale"` and reduce its
score's confidence rather than excluding it outright — a stale-but-likely
option can still be surfaced to the dispatcher with an appropriate
caveat.

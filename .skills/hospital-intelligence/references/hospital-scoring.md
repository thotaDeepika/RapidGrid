# Hospital Scoring — Weight Tables

## General emergency (default)

| Factor | Weight |
|---|---|
| Travel-time score | 0.30 |
| Emergency-resource score (ER capacity/trauma readiness) | 0.25 |
| Specialist-availability score | 0.20 |
| Bed-availability score | 0.15 |
| Blood-availability score | 0.10 |

## Cardiac emergency

| Factor | Weight | Notes |
|---|---|---|
| Cardiology/cath-lab availability | 0.35 | Highest weight — a further hospital with a cath lab beats a nearer one without |
| Travel-time score | 0.25 | |
| Emergency-resource score | 0.15 | |
| Bed-availability score | 0.15 | |
| Blood-availability score | 0.10 | |

## Major accident / trauma

| Factor | Weight | Notes |
|---|---|---|
| Trauma-centre capability | 0.30 | Level-1 trauma centres score highest |
| Blood-availability score | 0.20 | Elevated — trauma cases are the most likely to need transfusion |
| Surgical-capacity score | 0.20 | OR availability, on-call surgical team |
| Travel-time score | 0.20 | |
| Bed-availability score | 0.10 | |

## Stroke

| Factor | Weight | Notes |
|---|---|---|
| Neurology availability | 0.30 | |
| CT/imaging availability | 0.25 | Time-critical for thrombolysis decision |
| Travel-time score | 0.25 | Stroke is the most time-sensitive category — don't let this drop too low |
| Bed-availability score | 0.10 | |
| Emergency-resource score | 0.10 | |

## Computing sub-scores (0–1 scale)

- **Travel-time score**: `1 - (travel_time / max_reasonable_travel_time)`,
  clamped to [0, 1]. Use the Route Optimization Agent's ETA for this
  hospital as `travel_time`.
- **Resource/specialist/bed/blood scores**: normalise raw
  availability data (e.g. `beds_available / beds_total`, or a binary
  1.0/0.0 for "specialist on call now" vs not) to [0, 1]. Document
  whichever normalisation you pick in code comments — don't leave it
  implicit.

## Worked example (for the pitch/demo)

Incident: cardiac emergency, two candidate hospitals.

| Hospital | Travel-time score | Cardiology score | ER score | Bed score | Blood score | Weighted total |
|---|---|---|---|---|---|---|
| A (nearest, no cath lab) | 0.90 | 0.20 | 0.70 | 0.80 | 0.60 | 0.90×0.25 + 0.20×0.35 + 0.70×0.15 + 0.80×0.15 + 0.60×0.10 = **0.4525** |
| B (2km further, has cath lab) | 0.70 | 0.95 | 0.85 | 0.60 | 0.90 | 0.70×0.25 + 0.95×0.35 + 0.85×0.15 + 0.60×0.15 + 0.90×0.10 = **0.8300** |

Hospital B wins despite being further away — this is the exact
"resource-aware, not proximity-only" story to show judges, and doubles as
a good unit test case.

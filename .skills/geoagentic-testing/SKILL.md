---
name: geoagentic-testing
description: >
  Write and run tests and failure/chaos simulations for GeoAgentic —
  unit, integration, load, fallback, agent-conflict, and accessibility
  tests. Use this skill whenever asked to test a GeoAgentic feature,
  write a simulation scenario, stress-test the Decision Fusion Engine, or
  prepare a demo that needs to survive live failures gracefully (e.g. a
  traffic API going down mid-demo). Also use this when preparing the
  hackathon demo script — the eight scenarios below double as a strong
  live-demo narrative.
---

# GeoAgentic — Testing & Simulation

This skill exists because a multi-agent system's most impressive judge
moment is usually **graceful degradation**, not the happy path. Prioritise
the scenarios below over generic CRUD tests.

## The eight critical scenarios

1. **Primary route becomes blocked while the ambulance is moving.**
   Expect: Route Optimization emits a new route; Prediction updates ETA;
   dispatcher is notified of the reroute; the change is explained, not
   silent.
2. **Nearest hospital has no ICU capacity.**
   Expect: Hospital Intelligence excludes/down-ranks it and surfaces the
   next-best option with reasoning, per `hospital-intelligence` skill.
3. **Traffic API becomes unavailable.**
   Expect: system falls back to cached/historical data, marks results
   degraded, lowers confidence, notifies dispatcher — does not stall or
   crash. See `emergency-routing` failure handling.
4. **Two agents produce conflicting recommendations** (e.g. Route
   Optimization prefers hospital A's route while Hospital Intelligence
   ranks hospital B highest).
   Expect: Decision Fusion Engine resolves via the weighted factors and
   the `factor_breakdown`/`explanation` fields show *why* — this is the
   single best scenario to demo the fusion engine's explainability.
5. **Hundreds of incidents arrive simultaneously.**
   Expect: system stays responsive (load test); verify the event bus and
   Decision Fusion Engine don't serialize into a bottleneck; document the
   actual tested concurrency level honestly in the article rather than
   an unverified number.
6. **A deaf citizen reports an emergency using text or sign input.**
   Expect: Accessibility Agent normalises to the standard incident-report
   shape; downstream agents behave identically to a voice-reported
   incident. See `accessibility-first` skill.
7. **Hospital status changes after dispatch** (e.g. a bed opens up
   elsewhere, or the chosen hospital goes on diversion).
   Expect: system either reroutes to the better option or, if the
   ambulance is already close, explains why it's *not* rerouting
   (sunk-cost tradeoff) — don't just silently ignore the update.
8. **Dispatcher rejects the AI recommendation.**
   Expect: system accepts dispatcher override cleanly, logs the override
   (feeds the Learning Agent), and does not re-suggest the same rejected
   option without new information.

## Test types to produce per feature

- **Unit tests**: individual agent logic in isolation (mock the event bus).
- **Integration tests**: agent → event bus → Decision Fusion Engine, using
  the contracts in `geoagentic-architecture/references/agent-contracts.md`.
- **Load tests**: scenario 5 — concurrent incidents.
- **Fallback tests**: scenario 3 — degraded/stale data paths.
- **Agent-conflict tests**: scenario 4 — verify explainability, not just
  that *a* result comes out.
- **Accessibility tests**: scenario 6 — verify normalised output parity
  across input modalities, and spot-check the `accessibility-first`
  checklist against the actual rendered UI.

## Using the sample road network

`emergency-routing/references/sample-road-network.json` is small enough
to hand-verify expected outcomes — use it as the fixture for scenarios 1
and 3 rather than standing up a live map API for every test run.

## For the hackathon demo specifically

Pick 2–3 of the eight scenarios to actually demo live (scenario 4 and
either 1 or 3 are the strongest for showing off the multi-agent
architecture in under 2 minutes). State clearly which of the remaining
scenarios are tested-but-not-demoed vs. not yet implemented — judges
respond well to honest scoping (see `geoagentic-architecture` demo-scope
guidance).

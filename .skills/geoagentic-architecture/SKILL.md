---
name: geoagentic-architecture
description: >
  The master reference for the GeoAgentic emergency-vehicle-routing platform.
  Use this skill for ANY task that touches system design, service boundaries,
  agent responsibilities, the Decision Fusion Engine, API conventions, data
  models, or the communication bus — including scaffolding new services,
  reviewing pull requests, writing new agent code, or explaining the system
  to a teammate. Load this skill first whenever work spans more than one
  component, to make sure new code doesn't contradict the agreed
  architecture. For deep detail on a single subsystem, this skill points to
  emergency-routing, hospital-intelligence, accessibility-first, and
  geoagentic-testing.
---

# GeoAgentic Architecture

GeoAgentic is a multi-agent AI platform that coordinates emergency vehicle
response. It reframes routing as a **coordination problem**: seven
specialised agents each analyse one dimension of an incident, and a
**Decision Fusion Engine** combines their outputs into one explainable
action plan — rather than one model trying to do everything.

Team: Code Clan (Varsha Anand, T Deepika, Likhitha R, Praneel S, Harsh
Tiwari), Girl Geeks 2026, Case 02.

## When to use the other skills instead

- Writing/reviewing routing logic, A*/Dijkstra, ETA, rerouting → `emergency-routing`
- Hospital ranking/scoring logic → `hospital-intelligence`
- Citizen app, SOS flow, screen-reader/voice/sign-language UI → `accessibility-first`
- Writing tests, failure/chaos scenarios, simulations → `geoagentic-testing`

This skill is for anything cross-cutting: new services, the event bus,
data models, API conventions, or onboarding a new contributor.

## The seven runtime agents

| Agent | Responsibility | Output |
|---|---|---|
| Emergency Coordinator | Classifies severity, activates the right agents, compiles final plan | Action plan |
| Traffic Intelligence | Ingests traffic APIs/CCTV/IoT/citizen reports, scores road status | Traffic status + severity score |
| Route Optimization | Graph-based routing (A*/Dijkstra/time-dependent), alternates, rerouting | Optimal route(s) + ETA |
| Prediction | Forecasts congestion, delay probability, ETA (XGBoost/LSTM) | ETA + delay probability (continuous) |
| Hospital Intelligence | Ranks hospitals by resource availability, not just distance | Best hospital recommendation |
| Accessibility | Voice/sign-language/SOS/large-UI reporting paths | Accessible interaction + emergency data |
| Communication | Notifies hospital, driver, police, family; green-corridor requests | Notifications + updates |
| Learning | Learns from past cases to improve the other agents' models | Improved models + insights |

Read `references/agent-contracts.md` before implementing or modifying any
agent — it defines each agent's exact input/output contract so agents stay
interchangeable and testable in isolation.

## Decision Fusion Engine

Combines each agent's independent recommendation along five weighted
factors: response time, current traffic conditions, hospital availability,
emergency severity, and the reporting citizen's accessibility requirements.
The output must always be **explainable** — a dispatcher must be able to
see *why* a route or hospital was chosen, not just *what* was chosen.
Weights should be tunable per emergency type (see
`hospital-intelligence/references/hospital-scoring.md` for a worked
example). Never collapse fusion into a single opaque score with no
per-agent breakdown in the output.

## System workflow (canonical order — do not reorder without discussion)

1. Citizen reports an emergency (voice, app, SOS, sign-language, text).
2. Emergency Coordinator activates and classifies severity.
3. Traffic Intelligence analyses roads/congestion/accidents.
4. Prediction calculates ETA and delay probability.
5. Hospital Intelligence identifies the best-suited hospital.
6. Route Optimization generates the route to that hospital.
7. Decision Fusion Engine combines outputs into one action plan.
8. Dispatcher reviews and approves on the Dispatcher Dashboard.
9. Ambulance departs, guided by the Driver App.
10. System monitors conditions continuously and reroutes if needed.

Dispatcher approval (step 8) is a hard requirement for high-impact
decisions — never let an agent auto-dispatch without it, even in a demo
build, unless explicitly told the scenario is fully autonomous.

## Technology stack

See `references/technology-stack.md` for the full stack and conventions
(frontend, backend, data layer, AI/agents, maps, deployment). Default to
these choices unless the task explicitly calls for a substitution — don't
introduce a new framework or database without flagging it first.

## Communication bus

Agents communicate asynchronously through an event bus (message
queue/event stream), not direct function calls between agents. This keeps
agents independently deployable/testable and lets the Decision Fusion
Engine subscribe to all agent outputs without tight coupling. When adding
a new agent or event type, document the event schema in
`references/agent-contracts.md`.

## Cross-cutting requirements (apply everywhere)

- **Explainability**: every recommendation (route, hospital, fused plan)
  must ship with a human-readable reason, not just a score.
- **Degraded-data honesty**: if live data is stale/unavailable, mark the
  output as degraded/simulated and lower its confidence score — never
  silently present mock data as live.
- **Accessibility by default**: any citizen-facing surface must satisfy
  `accessibility-first` requirements, not just the dedicated Accessibility
  Agent's own UI.
- **Dispatcher-in-the-loop**: high-impact actions require approval (see
  workflow step 8).

## Full reference index

- `references/architecture.md` — five-layer system architecture, data flow, external integrations
- `references/agent-contracts.md` — input/output contract for every agent + the fusion engine
- `references/technology-stack.md` — frontend/backend/data/AI/maps/deployment stack and conventions

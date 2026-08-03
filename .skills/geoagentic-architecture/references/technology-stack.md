# Technology Stack & Conventions

| Layer | Choice | Notes |
|---|---|---|
| Frontend | Flutter or React.js + Tailwind CSS | Citizen app, Dispatcher dashboard, Driver app |
| Backend | FastAPI (Python), Node.js | FastAPI for AI/ML-heavy services, Node.js acceptable for lighter API/BFF layers |
| Relational + geospatial DB | PostgreSQL + PostGIS | All geospatial queries (routes, segments, hospital locations) live here |
| Document store | MongoDB | Incident reports, unstructured citizen input, logs |
| Cache/queue | Redis | Event bus transport, hot-path caching (live traffic snapshots) |
| Object storage | AWS S3 / MinIO | Images, videos, documents from citizen reports |
| Analytics | Data warehouse (any) | Post-hoc analysis, Learning Agent training data |
| Agent orchestration | LangGraph | Multi-agent orchestration and the event bus contract |
| ML models | XGBoost / LSTM | ETA and delay prediction |
| Accessibility | Whisper (speech-to-text), Coqui TTS (text-to-speech) | Accessibility Agent |
| Maps | Mapbox / OpenStreetMap / HERE Maps | Routing + live visualisation |
| Deployment | Docker, Kubernetes | Local dev may use docker-compose; k8s manifests for the "production-ready" story |

## Conventions for generated code

- All timestamps UTC, ISO 8601.
- All coordinates `[lat, lng]` (not `[lng, lat]`) — be explicit in code
  comments since this is a common source of bugs when mixing GeoJSON
  (`[lng, lat]`) and typical lat/lng APIs.
- Every service exposes a `/health` endpoint for the platform layer's
  monitoring.
- Every agent output includes `confidence` and `data_freshness` fields —
  no exceptions (see `agent-contracts.md`).
- Don't introduce a new database, framework, or cloud service without
  flagging the substitution and why the listed default doesn't fit.

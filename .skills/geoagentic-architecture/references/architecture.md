# GeoAgentic — Five-Layer Architecture

## 1. Users & Stakeholders
Citizens (all users), Accessible Interfaces (voice/blind, sign-language/deaf,
text/symbols, one-tap SOS, haptic/visual alerts), Dispatcher, Driver/Paramedic,
Hospital, Authorities (traffic police, disaster management, smart city).

## 2. Data Sources (real-time)
Traffic APIs, CCTV/cameras, IoT sensors, weather services, road/incident
alerts, citizen reports, hospital systems.

## 3. Agentic AI Layer
Seven agents (Traffic Intelligence, Route Optimization, Prediction, Hospital
Intelligence, Accessibility, Communication, Learning) + Decision Fusion
Engine, connected via an Agent Communication Bus (message queue/event
stream). See `agent-contracts.md` for exact I/O per agent.

## 4. Platform & Service Layer + Data & Storage Layer
- API Gateway (REST/GraphQL)
- Authentication Service (JWT/OAuth2, RBAC)
- Notification Service (SMS/push/email/voice)
- Map & Routing Service (Mapbox/OSM routing engine)
- AI/ML Service (model hosting/inference APIs)
- File & Media Service (images, videos, documents)
- Audit & Logging Service (logs, monitoring, audit trails)
- PostgreSQL + PostGIS (spatial database)
- MongoDB (document store)
- Redis (cache/queue)
- Object Storage (AWS S3/MinIO)
- Data Warehouse (analytics)

## 5. Outputs & Applications
- **Dispatcher Dashboard**: live map/tracking, emergency queue, AI
  recommendations, hospital status, analytics/reports.
- **Driver/Paramedic App**: turn-by-turn navigation, live traffic updates,
  ETA updates, alerts/notifications, hospital info.
- **Citizen App**: raise emergency, track ambulance, live status,
  notifications, accessibility options.
- **Hospital Dashboard**: incoming cases, patient details, ETA prediction,
  resource management, alerts.

## External integrations
Traffic signal controller, emergency hotline (112/108), smart city
platform, police & disaster management.

## Cross-cutting concerns
Security & privacy (encryption, data protection), scalability
(microservices, auto-scaling), high availability (load balancer,
failover), monitoring/observability (Prometheus, Grafana, ELK stack),
backup & disaster recovery (automated backup, geo-redundancy), compliance
(IT Act, HIPAA-equivalent guidelines).

## Mapping to official hackathon objectives

| Official objective | GeoAgentic component |
|---|---|
| Monitor traffic and detect disruptions in real time | Traffic Intelligence Agent |
| Suggest optimal routes for emergency vehicles | Route Optimization Agent |
| Predict delays and estimate arrival times | Prediction Agent |
| Visualise routes on an interactive map | Dispatcher Dashboard + Driver App |

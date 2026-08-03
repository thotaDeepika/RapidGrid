# 🚨 RapidGrid / GeoAgentic — Autonomous Multi-Agent AI Emergency Response Platform

RapidGrid (GeoAgentic) is a next-generation emergency response coordination platform. It integrates a **9-Agent Autonomous AI Network**, an **in-process Async Event Bus**, a **2-Phase Emergency Station Hub Routing Engine**, **Uber-style live hospital rerouting**, **multi-channel WebSockets live chat**, and **role-based portals** for Citizens, City Dispatchers, Paramedic First Responders, and Hospital ER Terminals.

---

## 🌟 Key System Capabilities

### 1. 🤖 9-Agent Autonomous AI Network
The platform decomposes emergency routing and coordination into nine decoupled micro-agents operating asynchronously over an event bus:
* **Traffic Intelligence Agent**: Monitors real-time road segment congestion, incidents, road closures, and weather risk.
* **Route Optimization Agent**: Interoperates with Google Routes API (v2) for live traffic-aware routing and computes 2-Phase shortest paths from Station Hub bases.
* **Hospital Intelligence Agent**: Evaluates and ranks nearby hospitals using weighted multi-factor criteria (ICU bed availability, emergency specialization, blood readiness, and travel distance).
* **Decision Fusion Engine**: Synthesizes agent inputs into a single explainable action plan with per-dimension factor scoring (Response Time, Traffic, Hospital, Severity, Accessibility).
* **Prediction Agent**: Provides ETA estimations with confidence intervals and weather/delay risk adjustments.
* **Accessibility Agent**: Normalizes multi-modal citizen reports (text, voice, sign language, SOS button, symbols) into standardized incident contracts.
* **Communication Agent**: Manages multi-channel dispatch notifications (SMS, WebSockets, Hospital API).
* **Emergency Coordinator Agent**: Assesses incident severity, categorizes medical/fire/police requirements, and activates targeted agent workflows.
* **Learning Agent**: Logs historical response metrics for continuous routing and dispatch optimization.

### 2. 🏬 2-Phase Station Hub Routing Engine
* **Phase 1 (Station Hub $\rightarrow$ Citizen Pickup)**: Computes the optimal response path from the nearest pre-configured service hub (*Aster Ambulance Hub, Hebbal Fire Station #4, Hebbal Police Base, NDRF Disaster Hub*) to the citizen's location.
* **Phase 2 (Citizen Pickup $\rightarrow$ Hospital ER)**: Computes live traffic-aware shortest route from patient pickup location to the selected hospital ER entrance.

### 3. 🚗 2-Stage Field Navigation & Uber-Style Live Hospital Rerouting
* **Stage 1 (En Route to Patient)**: First responder navigates response route to citizen's GPS coordinates. Upon marking arrival (`[📍 MARK ARRIVED AT PATIENT SPOT]`), the incident advances to Stage 2.
* **Stage 2 (En Route to Hospital ER)**: Navigation recomputes the route to destination ER.
* **Uber-Style Live Rerouting**: The driver can change the destination hospital on the fly. The system recomputes the route via Google Routes API and updates **both the Driver field app and Citizen view in real time**.

### 4. 🚑 Multi-Vehicle Selection & Mid-Incident Paramedic Standby Backup
* **Emergency Options**: Medical Ambulance, Fire Engine Rescue, Police Patrol Unit, Disaster Search & Rescue.
* **Mid-Incident Backup**: Tapping `+ DISPATCH AMBULANCE BACKUP NOW` dynamically dispatches a secondary paramedic unit to the scene without cancelling primary response.

### 5. 💬 Multi-Channel WebSocket Live Chat
* **Dynamic Direct Channels**: Renders isolated chat tabs for dispatched units (`[ 🚒 FIRE DRIVER CHAT ]`, `[ 🚔 POLICE CHAT ]`, `[ 🚑 AMBULANCE BACKUP CHAT ]`, `[ 🏥 HOSPITAL ER DESK CHAT ]`).
* Real-time WebSocket streaming with HTTP fallback.

---

## 🏗️ System Architecture & Data Flow

```
[ Citizen SOS Report ]
        │
        ▼
[ Accessibility Agent ] ──> [ Emergency Coordinator ]
                                     │
                                     ▼
                        [ Decision Fusion Engine ]
                        ┌────────────┼────────────┐
                        ▼            ▼            ▼
                   [ Traffic ]   [ Route ]   [ Hospital ]
                   [   Agent  ]  [ Agent ]   [  Agent   ]
                        └────────────┬────────────┘
                                     ▼
                        [ Dispatcher Approval ]
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
    [ Driver Field App (Stage 1 & 2) ]       [ Hospital ER Terminal ]
                 │                                       │
                 └──────────────[ Live Chat WS ]─────────┘
```

---

## 🛠️ Technology Stack

* **Frontend**: React 18, Vite, Tailwind CSS, Leaflet.js (`react-leaflet`), Lucide Icons.
* **Backend**: FastAPI, Asyncio, Pydantic v2, WebSockets, Uvicorn, Google Routes API (v2).
* **Event Bus**: Async In-Process Pub/Sub (`EventBus`).
* **Database**: JSON-based persistent state engine with atomic writes (`incidents_db.json`).

---

## 📁 Repository Structure

```
RapidGrid/
├── backend/
│   ├── main.py                  # FastAPI entry point & WebSocket endpoints
│   ├── agents/                  # 9 Autonomous AI Agents
│   │   ├── accessibility.py     # Multi-modal input translation agent
│   │   ├── communication.py     # Multi-channel notification agent
│   │   ├── coordinator.py       # Incident classification agent
│   │   ├── decision_fusion.py   # 5-factor explainable fusion engine
│   │   ├── hospital_intelligence.py # Hospital ranking agent
│   │   ├── learning.py          # Continuous performance learning agent
│   │   ├── prediction.py        # Delay & ETA estimation agent
│   │   ├── route_optimization.py# Live Google Routes & 2-phase hub router
│   │   └── traffic_intelligence.py # Traffic congestion agent
│   ├── bus/                     # Event Bus implementation
│   │   └── event_bus.py         # Async Pub/Sub event stream engine
│   ├── models/                  # Pydantic schemas & data models
│   │   └── schemas.py           # Shared data contracts across agents
│   ├── routers/                 # FastAPI Router endpoints
│   │   ├── chat.py              # WebSocket & HTTP chat handler
│   │   ├── driver.py            # Responder queue & reroute API
│   │   ├── hospital.py          # ER bed capacity & hospital management
│   │   ├── incident.py          # Citizen SOS & dispatcher approval API
│   │   └── ...                  # Agent-specific REST routers
│   ├── data/
│   │   ├── incidents_db.json    # Persistent incident database
│   │   └── sample_road_network.json
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # React router & role protection
│   │   ├── context/
│   │   │   └── AuthContext.jsx  # Role-based user authentication
│   │   ├── views/               # Portals for 4 user roles
│   │   │   ├── CitizenDashboard.jsx    # Citizen SOS & live tracking
│   │   │   ├── DispatcherDashboard.jsx # City Command Center & AI rationale
│   │   │   ├── DriverDashboard.jsx     # Paramedic field app & live reroute
│   │   │   ├── HospitalDashboard.jsx   # ER desk & bed availability terminal
│   │   │   └── Login.jsx               # Hub-wise & role selection screen
│   │   ├── components/
│   │   │   ├── AIRationale.jsx         # Fused AI factor breakdown modal
│   │   │   ├── LiveEmergencyChat.jsx   # Multi-channel WebSocket chat
│   │   │   ├── MapOverlay.jsx          # Leaflet map visualization component
│   │   │   └── SharedShell.jsx         # Header & navigation wrapper
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 👥 Role-Based Portals

| Portal | URL Path | Key Responsibilities |
| :--- | :--- | :--- |
| **Citizen Mobile App** | `/citizen` | One-tap SOS, 2-Phase live map tracking, standby paramedic backup request, live Chat. |
| **City Dispatch Control** | `/dispatcher` | Real-time incident list, AI Decision Rationale breakdown, hospital override & approval. |
| **Paramedic Field App** | `/driver` | Hub unit login (`AMB-UNIT-04`, etc.), Stage 1/2 navigation, Uber-style live hospital rerouting. |
| **Hospital ER Terminal** | `/hospital` | Hospital selection (Aster CMI, Manipal, Fortis, etc.), ER bed tracking, incoming patient triage. |

---

## 🛰️ API Endpoints Reference

### Incident Management (`/api/incidents`)
* `POST /api/incidents` — Submit citizen SOS emergency report.
* `GET /api/incidents/{incident_id}` — Poll incident status, hospital ER details, & 2-phase route telemetry.
* `GET /api/incidents` — Dispatcher list of all active incidents.
* `POST /api/incidents/{incident_id}/approve` — Approve AI action plan or override hospital assignment.
* `POST /api/incidents/{incident_id}/arrived` — Mark arrival at patient pickup or hospital ER.
* `POST /api/incidents/{incident_id}/request_ambulance` — Request mid-incident paramedic backup.

### Driver & Responder API (`/api/driver`)
* `GET /api/driver/active` — Fetch active dispatches filtered by vehicle service & hub.
* `POST /api/driver/claim` — First responder claims emergency dispatch.
* `POST /api/driver/arrived_pickup` — Mark Stage 1 arrival (Patient Picked Up $\rightarrow$ transition to Stage 2 hospital route).
* `POST /api/driver/change_hospital` — Driver live hospital reroute (recomputes Google route & syncs PWA).

### Multi-Channel Live Chat (`/api/chat` & `/ws/chat`)
* `GET /api/chat/{incident_id}/messages` — Fetch chat history for an incident.
* `POST /api/chat/{incident_id}/send` — Send message to chat channel.
* `WebSocket /ws/chat/{incident_id}` — Real-time WebSockets communication stream.

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.9+**
* **Node.js 18+**

### 1. Backend Setup
```bash
cd backend
python -m venv venv

# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# (Optional) Set Google Routes API key for live turn-by-turn routing:
# export GOOGLE_ROUTES_API_KEY="your_api_key_here"

uvicorn main:app --reload --port 8000
```
* Backend REST API & WebSockets will run at `http://localhost:8000`.
* API documentation available at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
* Frontend PWA will run at `http://localhost:5173` (or `http://localhost:5174`).

---

## 📄 License
Developed for RapidGrid / GeoAgentic AI Emergency Response Platform.

# 🚨 GeoAgentic - Autonomous Multi-Agent AI Emergency Response System

GeoAgentic is a next-generation Progressive Web Application (PWA) and FastAPI backend platform designed for intelligent emergency response coordination, 2-phase station hub routing, live multi-channel driver/hospital communication, and Uber-style real-time hospital rerouting.

---

## 🌟 Key Features

### 1. 🚑 Multi-Vehicle Emergency Selection & Standby Backups
* **Interactive Emergency Options**:
  * 🚑 **Medical Ambulance** (Direct Hospital ER Transport)
  * 🚒 **Fire Engine Rescue** (Fire Scene Control + Optional Medical Standby Backup)
  * 🚔 **Police Patrol Unit** (Law Enforcement Scene Control + Optional Injury Backup)
  * 🚁 **Disaster Search & Rescue** (Hazard Zone Evacuation + Optional Medical Backup)
* **Mid-Incident Backup Dispatch**: Tapping `+ DISPATCH AMBULANCE BACKUP NOW` dynamically dispatches a secondary paramedic unit to the scene.

### 2. 🏬 2-Phase Emergency Station Hub Routing Engine
* **Phase 1: Hub Base $\rightarrow$ Patient Pickup Location (Response Traversal)**
  * AI finds the nearest station hub (*Aster Ambulance Hub, Hebbal Fire Station #4, Hebbal Police Base, NDRF Disaster Hub*) and computes the shortest dispatch route (**Gold Dotted Line on Map**).
* **Phase 2: Patient Pickup Location $\rightarrow$ Destination Hospital ER (Transport Traversal)**
  * Computes the live traffic-aware shortest path to the destination hospital ER (**Red Solid Line on Map**).

### 3. 🚗 Uber-Style 2-Stage Navigation & Live Hospital Rerouting
* **Stage 1 (En Route to Patient Pickup)**: Driver follows response route from station base hub to citizen's GPS coordinates. Tapping `[ 📍 MARK ARRIVED AT PATIENT SPOT ]` advances incident to Stage 2.
* **Stage 2 (En Route to Hospital ER)**: Navigation recomputes live Google traffic route to the hospital ER entrance.
* **Live Driver Hospital Rerouting**: Driver can select any hospital from the dropdown. The system recomputes the new shortest path via Google Routes API and updates **both the Driver and Citizen maps in real-time like Uber**!

### 4. 💬 Multi-Channel WebSockets Live Chat
* **Isolated Channels**: Dynamically renders direct chat tabs for dispatched units:
  * `[ 🚒 FIRE DRIVER CHAT ]` / `[ 🚔 POLICE CHAT ]` / `[ 🚁 DISASTER CHAT ]`
  * `[ 🚑 AMBULANCE BACKUP CHAT ]`
  * `[ 🏥 HOSPITAL ER DESK CHAT ]`
* Live real-time WebSocket communication with fallback HTTP polling.

### 5. 🎯 Hub-Wise & Unit-Wise Driver Logins
* Pre-configured station hub credentials (`AMB-UNIT-04`, `FIRE-UNIT-09`, `POLICE-UNIT-02`, `RESCUE-UNIT-01`) or custom driver/hub logins.
* Driver dashboard automatically pre-selects emergency filters and displays assigned station hub badges.

---

## 🛠️ Technology Stack

* **Frontend**: React 18, Vite, TailwindCSS, Leaflet.js (`react-leaflet`), Lucide Vector Icons.
* **Backend**: FastAPI, Asyncio, Pydantic v2, WebSockets, Uvicorn, Google Routes API v2, Overpass OSM.
* **Database**: JSON-based persistent state engine with atomic writes (`incidents_db.json`).

---

## 🚀 Getting Started

### Prerequisites
* Python 3.9+
* Node.js 18+

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Backend API will be running on `http://localhost:8000`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend PWA will be running on `http://localhost:5173` (or `5174`).

---

## 🛰️ API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/incidents` | Trigger citizen emergency SOS report |
| `GET` | `/api/incidents/{id}` | Poll incident status, hospital ER info, & 2-phase route telemetry |
| `GET` | `/api/driver/active` | Get active emergency calls filtered by vehicle service & hub |
| `POST` | `/api/driver/claim` | First responder accepts emergency dispatch |
| `POST` | `/api/driver/arrived_pickup` | Stage 1 arrival (Patient Picked Up -> Recompute Hospital Route) |
| `POST` | `/api/driver/change_hospital` | Stage 2 Uber-style driver hospital reroute (Live PWA Sync) |
| `POST` | `/api/incidents/{id}/arrived` | Final Stage 2 arrival at Hospital ER / Incident Site |
| `POST` | `/api/incidents/{id}/request_ambulance` | Dynamic mid-incident ambulance backup dispatch |
| `GET` | `/api/chat/{id}/messages` | Get chat history for specific incident |
| `POST` | `/api/chat/{id}/send` | Broadcast message to active driver/hospital channel |

---

## 📄 License
Developed for GeoAgentic AI Emergency Response Platform.

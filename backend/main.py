"""
GeoAgentic — FastAPI Application Entry Point.

Starts the backend server with:
  - /health endpoint (required by technology-stack.md conventions)
  - Traffic Intelligence router (/api/traffic/*)
  - Route Optimization router (/api/route/*)
  - Hospital Intelligence router (/api/hospital/*)
  - Decision Fusion Engine router (/api/fusion/*)
  - Prediction Agent router (/api/prediction/*)
  - Accessibility Agent router (/api/accessibility/*)
  - Communication Agent router (/api/communication/*)
  - Emergency Coordinator router (/api/coordinator/*)
  - Learning Agent router (/api/learning/*)
  - Event bus initialisation and agent registration on startup
  - CORS middleware for frontend development

Run with:
  uvicorn main:app --reload --port 8000
"""

from __future__ import annotations

# Uvicorn Reload Trigger
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.accessibility import accessibility_agent
from agents.communication import communication_agent
from agents.coordinator import coordinator_agent
from agents.learning import learning_agent
from agents.prediction import prediction_agent
from agents.route_optimization import route_agent
from agents.traffic_intelligence import traffic_agent
from routers import chat, accessibility, communication, coordinator, fusion, hospital, learning, prediction, routing, traffic, incident, driver

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-30s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("geoagentic")


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup:
      1. Traffic Intelligence loads the road network.
      2. Route Optimization builds its graph from the same data.
      3. Route Optimization subscribes to ROUTE_REQUEST on the bus.
      4. Traffic Intelligence publishes an initial snapshot.
    """
    logger.info("GeoAgentic backend starting up …")

    # 1. Load road network into Traffic Intelligence
    traffic_agent.load_network()

    # 2. Share the loaded data with Route Optimization (single source of truth)
    route_agent.load_network(
        nodes=traffic_agent.nodes,
        edges=traffic_agent.edges,
    )

    # 3. Register agents on the event bus
    route_agent.register_on_bus()
    prediction_agent.register_on_bus()
    communication_agent.register_on_bus()
    coordinator_agent.register_on_bus()
    learning_agent.register_on_bus()

    # 4. Publish initial traffic snapshot
    await traffic_agent.publish_snapshot()

    logger.info("All agents initialised and registered ✓")
    yield  # ← app runs
    logger.info("GeoAgentic backend shutting down …")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="GeoAgentic API",
    description=(
        "Multi-agent AI platform for emergency vehicle routing. "
        "Coordinates Traffic Intelligence, Route Optimization, and more "
        "through a Decision Fusion Engine."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow all origins for local dev (tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(traffic.router)
app.include_router(routing.router)
app.include_router(hospital.router)
app.include_router(fusion.router)
app.include_router(prediction.router)
app.include_router(accessibility.router)
app.include_router(communication.router)
app.include_router(coordinator.router)
app.include_router(learning.router)
app.include_router(incident.router)
app.include_router(driver.router)
app.include_router(chat.router)


# ---------------------------------------------------------------------------
# Health endpoint — required by technology-stack.md
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Platform"])
async def health():
    """
    Health check endpoint.

    Every service exposes /health for the platform layer's monitoring
    (see technology-stack.md conventions).
    """
    return {
        "status": "healthy",
        "service": "geoagentic-backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agents": {
            "traffic_intelligence": "active",
            "route_optimization": "active",
            "hospital_intelligence": "active",
            "decision_fusion_engine": "active",
            "prediction_agent": "active",
            "accessibility_agent": "active",
            "communication_agent": "active",
            "emergency_coordinator": "active",
            "learning_agent": "stub_active",
        },
    }


from fastapi import WebSocket, WebSocketDisconnect
@app.websocket("/ws/chat/{incident_id}")
async def websocket_chat_endpoint(websocket: WebSocket, incident_id: str):
    await chat.manager.connect(websocket, incident_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                msg_data = {
                    "incident_id": incident_id,
                    "sender_role": payload.get("sender_role", "citizen"),
                    "sender_name": payload.get("sender_name", "Anonymous"),
                    "message": payload.get("message", ""),
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                await chat.manager.broadcast(incident_id, msg_data)
            except Exception as e:
                print("WS Error:", e)
    except WebSocketDisconnect:
        chat.manager.disconnect(websocket, incident_id)

# Touch for per-unit tracking reload
# Reload for include_ambulance_backup schema update
# Touch for 2-Phase Hub Routing reload
# Reload for 2-stage driver hospital rerouting endpoints
# Reload for driver active backup filter update
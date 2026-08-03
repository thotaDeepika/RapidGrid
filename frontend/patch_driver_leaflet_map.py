import sys

drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

# Replace MapOverlay import with react-leaflet components
d_content = d_content.replace(
    "import MapOverlay from '../components/MapOverlay';",
    "import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';\nimport 'leaflet/dist/leaflet.css';"
)

# Replace MapOverlay render with full Leaflet Map matching CitizenDashboard
old_map_render = """          <div className="relative flex-1 min-h-[260px] rounded-xl overflow-hidden border border-outline-variant/30">
            {routeCoords.length > 0 ? (
              <MapOverlay routeCoordinates={routeCoords} height="100%" />
            ) : (
              <div className="absolute inset-0 flex items-center justify-center bg-surface-container-low text-on-surface-variant text-sm">
                Loading Route Map...
              </div>
            )}
            <div className="absolute top-4 right-4 bg-surface-container-highest/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10 text-xs font-mono font-bold">
              <span className="w-2 h-2 bg-tertiary rounded-full animate-pulse"></span>
              LIVE TURN-BY-TURN NAV
            </div>
          </div>"""

new_map_render = """          <div className="relative flex-1 min-h-[280px] rounded-xl overflow-hidden border border-outline-variant/30">
            <MapContainer center={[origin.lat, origin.lng]} zoom={13} style={{ height: '100%', width: '100%' }} zoomControl={false} attributionControl={false}>
              <TileLayer url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png" />
              {/* Patient Pickup Marker */}
              <Marker position={[origin.lat, origin.lng]} />
              {/* Destination Hospital Marker */}
              <Marker position={[hospLoc.lat, hospLoc.lng]} />
              {/* Base Station Hub Marker if available */}
              {selectedIncident?.citizen_view?.phase1_hub && (
                <Marker position={[selectedIncident.citizen_view.phase1_hub.lat, selectedIncident.citizen_view.phase1_hub.lng]} />
              )}
              {/* Phase 1 Route: Station Hub -> Patient Pickup (Gold Dotted Line) */}
              {selectedIncident?.citizen_view?.phase1_route_coordinates && selectedIncident.citizen_view.phase1_route_coordinates.length > 0 && (
                <Polyline 
                  positions={selectedIncident.citizen_view.phase1_route_coordinates.map(c => [c.lat, c.lng])} 
                  pathOptions={{ color: '#FFB900', weight: 4, opacity: 0.9, dashArray: '8, 8' }} 
                />
              )}
              {/* Phase 2 Route: Patient Pickup -> Destination Hospital (Red Solid Line) */}
              {routeCoords.length > 0 && (
                <Polyline 
                  positions={routeCoords.map(c => [c.lat, c.lng])} 
                  pathOptions={{ color: '#FF5451', weight: 5, opacity: 0.9 }} 
                />
              )}
            </MapContainer>

            {/* Station Base Hub Badge Overlay */}
            {selectedIncident?.citizen_view?.phase1_hub && (
              <div className="absolute top-4 left-4 bg-surface-container-highest/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10 font-mono text-[10px] font-bold text-[#FFB900]">
                <span className="material-symbols-outlined text-[14px]">local_convenience_store</span>
                <span>BASE: {selectedIncident.citizen_view.phase1_hub.name} ({selectedIncident.citizen_view.phase1_eta_minutes || 5}m)</span>
              </div>
            )}

            <div className="absolute top-4 right-4 bg-surface-container-highest/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10 text-xs font-mono font-bold">
              <span className="w-2 h-2 bg-tertiary rounded-full animate-pulse"></span>
              LIVE TURN-BY-TURN NAV
            </div>
          </div>"""

d_content = d_content.replace(old_map_render, new_map_render)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("DriverDashboard.jsx updated to render exact same Leaflet map and 2-phase routes as CitizenDashboard.jsx")

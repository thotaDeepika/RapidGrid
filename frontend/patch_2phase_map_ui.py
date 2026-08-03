import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# Update Map rendering block to draw Phase 1 (Hub -> Citizen) and Phase 2 (Citizen -> Hospital)
old_map_jsx = """            <MapContainer center={[mapCenter.lat, mapCenter.lng]} zoom={14} style={mapContainerStyle} zoomControl={false} attributionControl={false}>
              <TileLayer url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png" />
              <Marker position={[origin.lat, origin.lng]} />
              <Marker position={[hospLoc.lat, hospLoc.lng]} />
              {routeCoords.length > 0 && <Polyline positions={routeCoords.map(c => [c.lat, c.lng])} pathOptions={{ color: '#FF5451', weight: 5, opacity: 0.8 }} />}
            </MapContainer>"""

new_map_jsx = """            <MapContainer center={[mapCenter.lat, mapCenter.lng]} zoom={13} style={mapContainerStyle} zoomControl={false} attributionControl={false}>
              <TileLayer url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png" />
              {/* Pickup Point Marker */}
              <Marker position={[origin.lat, origin.lng]} />
              {/* Destination Hospital Marker */}
              <Marker position={[hospLoc.lat, hospLoc.lng]} />
              {/* Base Station Hub Marker if available */}
              {citizenView?.phase1_hub && (
                <Marker position={[citizenView.phase1_hub.lat, citizenView.phase1_hub.lng]} />
              )}
              {/* Phase 1 Route: Base Hub -> Citizen Pickup Location (Cyan/Gold Dotted Line) */}
              {citizenView?.phase1_route_coordinates && citizenView.phase1_route_coordinates.length > 0 && (
                <Polyline 
                  positions={citizenView.phase1_route_coordinates.map(c => [c.lat, c.lng])} 
                  pathOptions={{ color: '#FFB900', weight: 4, opacity: 0.9, dashArray: '8, 8' }} 
                />
              )}
              {/* Phase 2 Route: Citizen Pickup -> Destination Hospital (Red Solid Line) */}
              {routeCoords.length > 0 && (
                <Polyline 
                  positions={routeCoords.map(c => [c.lat, c.lng])} 
                  pathOptions={{ color: '#FF5451', weight: 5, opacity: 0.9 }} 
                />
              )}
            </MapContainer>"""

c_content = c_content.replace(old_map_jsx, new_map_jsx)

# Add Base Station Hub Overlay on top of Map
old_hub_overlay = """          {/* Live tracking badge */}
          <div className="absolute top-4 right-4 bg-surface-container-highest/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10">
            <span className="w-2 h-2 bg-tertiary rounded-full animate-pulse"></span>
            <span className="font-label-caps text-label-caps text-on-surface">LIVE TRACKING</span>
          </div>"""

new_hub_overlay = """          {/* Station Base Hub Badge Overlay */}
          {citizenView?.phase1_hub && (
            <div className="absolute top-4 left-4 bg-surface-container-highest/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10 font-mono text-[10px] font-bold text-[#FFB900]">
              <span className="material-symbols-outlined text-[14px]">local_convenience_store</span>
              <span>BASE: {citizenView.phase1_hub.name} ({citizenView.phase1_eta_minutes || 5}m to pickup)</span>
            </div>
          )}

          {/* Live tracking badge */}
          <div className="absolute top-4 right-4 bg-surface-container-highest/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10">
            <span className="w-2 h-2 bg-tertiary rounded-full animate-pulse"></span>
            <span className="font-label-caps text-label-caps text-on-surface">LIVE TRACKING</span>
          </div>"""

c_content = c_content.replace(old_hub_overlay, new_hub_overlay)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("CitizenDashboard.jsx updated to display Phase 1 Station Hub dispatch & Phase 2 Hospital transport routes")

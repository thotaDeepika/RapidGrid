import sys

file_path = "src/views/CitizenDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "import { GoogleMap, useJsApiLoader, Marker, Polyline } from '@react-google-maps/api';",
    "import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';"
)

loader_old = """  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: 'AIzaSyAVLkE1rv3CV0bnOZYJkDvtRir8DlAbS7k'
  });"""
content = content.replace(loader_old, "  const isLoaded = true;")

map_old = """            <GoogleMap
              mapContainerStyle={mapContainerStyle}
              center={mapCenter}
              zoom={14}
              options={{ disableDefaultUI: true, gestureHandling: 'greedy' }}
            >
              <Marker position={origin} label="SOS" />
              <Marker position={hospLoc} icon={{ url: 'https://maps.google.com/mapfiles/ms/icons/hospital.png' }} />
              {routeCoords.length > 0 && (
                <Polyline
                  path={routeCoords}
                  options={{ strokeColor: '#FF5451', strokeOpacity: 0.8, strokeWeight: 5 }}
                />
              )}
            </GoogleMap>"""

map_new = """            <MapContainer center={[mapCenter.lat, mapCenter.lng]} zoom={14} style={mapContainerStyle} zoomControl={false} attributionControl={false}>
              <TileLayer url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png" />
              <Marker position={[origin.lat, origin.lng]} />
              <Marker position={[hospLoc.lat, hospLoc.lng]} />
              {routeCoords.length > 0 && <Polyline positions={routeCoords.map(c => [c.lat, c.lng])} pathOptions={{ color: '#FF5451', weight: 5, opacity: 0.8 }} />}
            </MapContainer>"""

content = content.replace(map_old, map_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

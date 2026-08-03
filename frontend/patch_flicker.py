import sys

# 1. Update DispatcherDashboard.jsx
file_path = "src/views/DispatcherDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_state_logic = """export default function DispatcherDashboard() {
  const [incidents, setIncidents] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [autoDispatch, setAutoDispatch] = useState(false);

  // Poll for active incidents every 2 seconds
  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await fetch('/api/incidents/');
        if (!res.ok) return;
        const data = await res.json();
        const incList = data.incidents || [];
        setIncidents(incList);

        // Auto-select first incident if none selected
        if (incList.length > 0 && !selectedIncident) {
          setSelectedIncident(incList[0]);
        } else if (selectedIncident) {
          // Update currently selected incident data
          const updated = incList.find(i => i.incident_id === selectedIncident.incident_id);
          if (updated) setSelectedIncident(updated);
        }
      } catch (err) {
        console.error('Failed to fetch incidents:', err);
      }
    };

    fetchIncidents();
    const interval = setInterval(fetchIncidents, 2000);
    return () => clearInterval(interval);
  }, [selectedIncident]);"""

new_state_logic = """export default function DispatcherDashboard() {
  const [incidents, setIncidents] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [autoDispatch, setAutoDispatch] = useState(false);

  // Poll for active incidents every 2.5 seconds (runs once, no re-triggering loops)
  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await fetch('/api/incidents/');
        if (!res.ok) return;
        const data = await res.json();
        const incList = data.incidents || [];
        setIncidents(incList);
      } catch (err) {
        console.error('Failed to fetch incidents:', err);
      }
    };

    fetchIncidents();
    const interval = setInterval(fetchIncidents, 2500);
    return () => clearInterval(interval);
  }, []);

  // Derive selected incident cleanly without causing state re-renders
  const selectedIncident = incidents.find(i => i.incident_id === selectedId) || incidents[0] || null;"""

content = content.replace(old_state_logic, new_state_logic)

# Replace remaining references to setSelectedIncident(inc) with setSelectedId(inc.incident_id)
content = content.replace("onClick={() => setSelectedIncident(inc)}", "onClick={() => setSelectedId(inc.incident_id)}")
content = content.replace("setSelectedIncident(null);", "setSelectedId(null);")
content = content.replace("setSelectedIncident(updatedInc);", "")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

# 2. Update MapOverlay.jsx so Leaflet doesn't flash when switching routes
map_file = "src/components/MapOverlay.jsx"
with open(map_file, "r", encoding="utf-8") as f:
    map_content = f.read()

old_map_effect = """    if (mapInstance.current && routeCoordinates && routeCoordinates.length > 0) {
      if (routeLayer.current) {
        mapInstance.current.removeLayer(routeLayer.current);
      }

      const latlngs = routeCoordinates.map(c => [c.lat, c.lng]);
      
      routeLayer.current = L.polyline(latlngs, {
        color: '#3b82f6',
        weight: 6,
        opacity: 0.8,
        lineCap: 'round',
        lineJoin: 'round'
      }).addTo(mapInstance.current);

      mapInstance.current.fitBounds(routeLayer.current.getBounds(), { padding: [50, 50] });
    }"""

new_map_effect = """    if (mapInstance.current && routeCoordinates && routeCoordinates.length > 0) {
      const routeKey = JSON.stringify(routeCoordinates);
      if (mapInstance.current._lastRouteKey === routeKey) return;
      mapInstance.current._lastRouteKey = routeKey;

      if (routeLayer.current) {
        mapInstance.current.removeLayer(routeLayer.current);
      }

      const latlngs = routeCoordinates.map(c => [c.lat, c.lng]);
      
      routeLayer.current = L.polyline(latlngs, {
        color: '#3b82f6',
        weight: 6,
        opacity: 0.8,
        lineCap: 'round',
        lineJoin: 'round'
      }).addTo(mapInstance.current);

      try {
        mapInstance.current.fitBounds(routeLayer.current.getBounds(), { padding: [50, 50] });
      } catch (e) {}
    }"""

map_content = map_content.replace(old_map_effect, new_map_effect)

with open(map_file, "w", encoding="utf-8") as f:
    f.write(map_content)

print("Flicker fix applied successfully to DispatcherDashboard and MapOverlay")

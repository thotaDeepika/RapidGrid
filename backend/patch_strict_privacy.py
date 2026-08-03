import sys
import json
import os

# 1. Clear old incidents DB file so lingering test data without strict phone ownership is wiped
db_file = "data/incidents_db.json"
if os.path.exists(db_file):
    with open(db_file, "w", encoding="utf-8") as f:
        json.dump([], f)
    print("Cleared old incidents_db.json")

# 2. Update CitizenDashboard.jsx with strict phone number matching
cit_file = "../frontend/src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    content = f.read()

# Add citizen_name and citizen_phone to SOS payload
old_payload = """    const payload = {
      citizen_text: details.trim() || 'Emergency reported via SOS button.',
      location: locationCoords || { lat: 12.9756, lng: 77.6068 },
      input_modality: 'text',
      timestamp: new Date().toISOString()
    };"""

new_payload = """    const payload = {
      citizen_text: details.trim() || 'Emergency reported via SOS button.',
      citizen_name: citizenInfo?.name || 'Anonymous Citizen',
      citizen_phone: citizenInfo?.phone || 'Unregistered',
      location: locationCoords || { lat: 12.9756, lng: 77.6068 },
      input_modality: 'text',
      timestamp: new Date().toISOString()
    };"""

content = content.replace(old_payload, new_payload)

# Replace polling logic with strict phone matching
old_polling = """  // Fetch all active incidents to allow tracking past patient emergencies
  useEffect(() => {
    const fetchAllIncidents = async () => {
      try {
        const res = await fetch('/api/incidents/');
        if (!res.ok) return;
        const data = await res.json();
        const incs = data.incidents || [];
        setAllCitizenIncidents(incs);

        // If user is on home and there are active incidents, auto-load latest active incident
        if (appState === 'home' && incs.length > 0 && !incidentData) {
          const latest = incs[incs.length - 1];
          if (latest.citizen_view) {
            setIncidentData(latest);
            setCitizenView(latest.citizen_view);
            setPollUrl(`/api/incidents/${latest.incident_id}`);
            setAppState('tracking');
          }
        }
      } catch (err) {}
    };
    fetchAllIncidents();
    const interval = setInterval(fetchAllIncidents, 2500);
    return () => clearInterval(interval);
  }, [appState, incidentData]);"""

new_polling = """  // Fetch active incidents belonging strictly to THIS logged-in citizen account
  useEffect(() => {
    const fetchAllIncidents = async () => {
      try {
        const res = await fetch('/api/incidents/');
        if (!res.ok) return;
        const data = await res.json();
        const incs = data.incidents || [];
        
        // STRICT PRIVACY FILTER: Unique account identifier is phone number
        const myIncidents = incs.filter(i => {
          if (!citizenInfo?.phone) return false;
          return i.citizen_phone && i.citizen_phone.trim() === citizenInfo.phone.trim();
        });

        setAllCitizenIncidents(myIncidents);

        // If logged-in citizen has active incidents, auto-load THEIR latest active incident
        if (appState === 'home' && myIncidents.length > 0 && !incidentData) {
          const latest = myIncidents[myIncidents.length - 1];
          if (latest.citizen_view) {
            setIncidentData(latest);
            setCitizenView(latest.citizen_view);
            setPollUrl(`/api/incidents/${latest.incident_id}`);
            setAppState('tracking');
          }
        }
      } catch (err) {}
    };
    fetchAllIncidents();
    const interval = setInterval(fetchAllIncidents, 2500);
    return () => clearInterval(interval);
  }, [appState, incidentData, citizenInfo]);"""

content = content.replace(old_polling, new_polling)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(content)

print("CitizenDashboard.jsx patched with strict phone-number unique account matching")

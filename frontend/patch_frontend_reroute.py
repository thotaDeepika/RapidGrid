import sys

file_path = "src/views/DispatcherDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_res_ok = """      if (res.ok) {
        const updatedInc = {
          ...selectedIncident,
          status: 'dispatched',
          citizen_view: {
            ...selectedIncident.citizen_view,
            hospital_name: hospName,
            message: `Help is being dispatched. Approved Hospital: ${hospName}.`
          }
        };
        
        setIncidents(prev => prev.map(i => i.incident_id === selectedIncident.incident_id ? updatedInc : i));
        setShowOverrideModal(false);
      }"""

new_res_ok = """      if (res.ok) {
        const updatedBackendInc = await res.json();
        setIncidents(prev => prev.map(i => i.incident_id === selectedIncident.incident_id ? updatedBackendInc : i));
        setShowOverrideModal(false);
      }"""

content = content.replace(old_res_ok, new_res_ok)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("DispatcherDashboard response parsing patched successfully")

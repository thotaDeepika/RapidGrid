import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# 1. Update quick option chips handler to set appropriate vehicle and backup defaults
old_chip_handler = """  const addDetail = (text) => {
    setDetails(prev => prev ? `${prev}, ${text}` : text);
  };"""

new_chip_handler = """  const addDetail = (text) => {
    setDetails(prev => prev ? `${prev}, ${text}` : text);
    if (text.includes('MEDICAL') || text.includes('BREATHING')) {
      setSelectedVehicle('Ambulance');
      setIncludeAmbulanceBackup(true);
    } else if (text.includes('FIRE')) {
      setSelectedVehicle('Fire Engine');
    } else if (text.includes('POLICE')) {
      setSelectedVehicle('Police Cruiser');
    } else if (text.includes('ACCIDENT')) {
      setSelectedVehicle('Police Cruiser');
      setIncludeAmbulanceBackup(true);
    }
  };"""

c_content = c_content.replace(old_chip_handler, new_chip_handler)

# 2. Add useEffect to auto-default activeTrackingUnit according to incident's vehicle_required
old_eff_hook = """  // Polling for status updates when incident created
  useEffect(() => {"""

new_eff_hook = """  // Auto-default active tracking unit tab according to incident's vehicle_required
  useEffect(() => {
    const vReq = citizenView?.vehicle_required || incidentData?.vehicle_required;
    if (vReq === 'Ambulance') {
      setActiveTrackingUnit('ambulance');
    } else {
      setActiveTrackingUnit('primary');
    }
  }, [citizenView?.vehicle_required, incidentData?.vehicle_required]);

  // Polling for status updates when incident created
  useEffect(() => {"""

c_content = c_content.replace(old_eff_hook, new_eff_hook)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("CitizenDashboard.jsx updated with responsive SOS option presets and auto-tab selection")

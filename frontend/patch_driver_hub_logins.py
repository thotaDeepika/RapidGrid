import sys

# 1. Update Login.jsx to add Hub-Wise Driver Selector Modal
login_file = "src/views/Login.jsx"
with open(login_file, "r", encoding="utf-8") as f:
    l_content = f.read()

driver_units_code = """
  const [showDriverModal, setShowDriverModal] = useState(false);
  const [customDriverName, setCustomDriverName] = useState('');
  const [customUnitId, setCustomUnitId] = useState('');
  const [customHubName, setCustomHubName] = useState('');
  const [customVehicleType, setCustomVehicleType] = useState('Ambulance');

  const emergencyDriverUnits = [
    { unitId: 'AMB-UNIT-04', vehicleType: 'Ambulance', driverName: 'Suresh Kumar', hubName: 'Aster CMI Emergency Ambulance Hub', phone: '+91 98765 43210' },
    { unitId: 'AMB-UNIT-01', vehicleType: 'Ambulance', driverName: 'Ramesh Gowda', hubName: 'Manipal Ambulance Base Depot', phone: '+91 98765 43211' },
    { unitId: 'AMB-UNIT-02', vehicleType: 'Ambulance', driverName: 'Vijay Naik', hubName: 'Victoria Hospital Paramedic Base', phone: '+91 98765 43212' },
    { unitId: 'FIRE-UNIT-09', vehicleType: 'Fire Engine', driverName: 'Capt. Rajesh Rao', hubName: 'Hebbal Fire & Rescue Station #4', phone: '+91 98765 43220' },
    { unitId: 'FIRE-UNIT-01', vehicleType: 'Fire Engine', driverName: 'Sub-Officer Praveen', hubName: 'High Grounds Central Fire Station', phone: '+91 98765 43221' },
    { unitId: 'POLICE-UNIT-02', vehicleType: 'Police Cruiser', driverName: 'Insp. Vikram Singh', hubName: 'Hebbal Police Patrol Base', phone: '+91 98765 43230' },
    { unitId: 'RESCUE-UNIT-01', vehicleType: 'Disaster Rescue', driverName: 'Cmdr. Arjun Reddy', hubName: 'NDRF Disaster Rescue Hub North', phone: '+91 98765 43240' }
  ];
"""

l_content = l_content.replace(
    "  const [showHospModal, setShowHospModal] = useState(false);",
    driver_units_code + "\n  const [showHospModal, setShowHospModal] = useState(false);"
)

l_content = l_content.replace(
    "    if (roleId === 'hospital' && !extraData) {",
    "    if (roleId === 'driver' && !extraData) {\n      setShowDriverModal(true);\n      return;\n    }\n    if (roleId === 'hospital' && !extraData) {"
)

# Render Driver Hub Modal before closing </div> in Login.jsx
old_modal_end = "      {/* Hospital Selection Modal */}"
driver_modal_jsx = """      {/* Driver Hub-Wise Login Modal */}
      {showDriverModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="bg-surface-container-high border border-outline-variant/30 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <div className="flex justify-between items-center border-b border-outline-variant/20 pb-3">
              <div className="flex items-center gap-2">
                <Truck className="text-[#FFB900]" size={22} />
                <h3 className="font-mono font-bold text-lg text-on-surface">Emergency Driver Hub Login</h3>
              </div>
              <button 
                onClick={() => setShowDriverModal(false)}
                className="text-on-surface-variant hover:text-on-surface text-xl font-bold px-2"
              >
                &times;
              </button>
            </div>

            <p className="text-xs text-on-surface-variant font-mono">
              Select your assigned Base Station Hub & Emergency Unit, or enter custom unit credentials:
            </p>

            {/* Pre-configured Hub Units List */}
            <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
              {emergencyDriverUnits.map((u) => (
                <button
                  key={u.unitId}
                  onClick={() => {
                    setShowDriverModal(false);
                    handleRoleLogin('driver', u);
                  }}
                  className="w-full bg-surface-container hover:bg-surface-container-highest border border-outline-variant/20 rounded-xl p-3 text-left transition-all flex items-center justify-between group"
                >
                  <div>
                    <div className="font-mono text-sm font-bold text-on-surface group-hover:text-[#FFB900] flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded-md bg-[#FFB900]/20 text-[#FFB900] text-xs font-mono">{u.unitId}</span>
                      <span>{u.driverName}</span>
                    </div>
                    <div className="text-xs text-on-surface-variant mt-0.5 flex items-center gap-1 font-mono">
                      <span>Base: {u.hubName}</span>
                    </div>
                  </div>
                  <ChevronRight size={16} className="text-on-surface-variant group-hover:text-[#FFB900]" />
                </button>
              ))}
            </div>

            {/* Custom Unit Entry Form */}
            <div className="border-t border-outline-variant/20 pt-3 space-y-2">
              <span className="text-[10px] font-mono text-tertiary uppercase font-bold block">Or Login as Custom Driver & Station Hub:</span>
              <div className="grid grid-cols-2 gap-2">
                <input
                  type="text"
                  placeholder="Driver Name (e.g. Ramesh)"
                  value={customDriverName}
                  onChange={(e) => setCustomDriverName(e.target.value)}
                  className="bg-surface-container border border-outline-variant/30 text-on-surface px-3 py-2 rounded-xl text-xs font-mono focus:outline-none focus:border-primary"
                />
                <input
                  type="text"
                  placeholder="Unit ID (e.g. AMB-UNIT-99)"
                  value={customUnitId}
                  onChange={(e) => setCustomUnitId(e.target.value)}
                  className="bg-surface-container border border-outline-variant/30 text-on-surface px-3 py-2 rounded-xl text-xs font-mono focus:outline-none focus:border-primary"
                />
              </div>
              <input
                type="text"
                placeholder="Station Hub Name (e.g. Hebbal Base Depot)"
                value={customHubName}
                onChange={(e) => setCustomHubName(e.target.value)}
                className="w-full bg-surface-container border border-outline-variant/30 text-on-surface px-3 py-2 rounded-xl text-xs font-mono focus:outline-none focus:border-primary"
              />
              <button
                onClick={() => {
                  if (!customDriverName || !customUnitId) return;
                  setShowDriverModal(false);
                  handleRoleLogin('driver', {
                    unitId: customUnitId,
                    driverName: customDriverName,
                    hubName: customHubName || 'Central Base Depot',
                    vehicleType: customVehicleType
                  });
                }}
                className="w-full py-2.5 bg-[#FFB900] text-black font-bold font-mono rounded-xl text-xs hover:bg-[#FFB900]/90 transition-all shadow-md"
              >
                Login to Assigned Station Hub
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Hospital Selection Modal */}"""

l_content = l_content.replace(old_modal_end, driver_modal_jsx)
with open(login_file, "w", encoding="utf-8") as f:
    f.write(l_content)

# 2. Update DriverDashboard.jsx header to display Hub & Unit credentials
drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

old_drv_header = """  return (
    <div className="flex flex-col h-[calc(100vh-80px)] p-4 bg-surface text-on-surface gap-4 overflow-y-auto">
      {/* Top Header Controls */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-surface-container p-4 rounded-2xl border border-outline-variant/20 shadow-md">
        <div>
          <h1 className="font-mono text-xl font-bold text-on-surface flex items-center gap-2">
            <Truck className="text-[#FFB900]" /> Paramedic Driver Dispatch Queue
          </h1>
          <p className="text-xs text-on-surface-variant font-mono">
            Active emergency calls pending first responder acceptance
          </p>
        </div>"""

new_drv_header = """  const driverUnitId = driverData?.unitId || 'AMB-UNIT-04';
  const driverName = driverData?.driverName || 'Suresh Kumar';
  const hubName = driverData?.hubName || 'Aster CMI Emergency Ambulance Hub';

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] p-4 bg-surface text-on-surface gap-4 overflow-y-auto">
      {/* Top Header Controls with Hub Station Badge */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-surface-container p-4 rounded-2xl border border-outline-variant/20 shadow-md">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded-md bg-[#FFB900]/20 text-[#FFB900] font-mono text-xs font-bold">{driverUnitId}</span>
            <h1 className="font-mono text-lg font-bold text-on-surface flex items-center gap-2">
              <Truck className="text-[#FFB900]" size={20} /> {driverName}
            </h1>
          </div>
          <p className="text-xs text-tertiary font-mono font-bold mt-0.5 flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px]">local_convenience_store</span>
            Base Hub: {hubName}
          </p>
        </div>"""

d_content = d_content.replace(old_drv_header, new_drv_header)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("Login.jsx and DriverDashboard.jsx updated with Hub-Wise Driver Logins")

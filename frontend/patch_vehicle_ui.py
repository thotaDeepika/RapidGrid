import sys

# 1. Update CitizenDashboard.jsx
cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

# Add selectedVehicle state
c_content = c_content.replace(
    "const [details, setDetails] = useState('');",
    "const [details, setDetails] = useState('');\n  const [selectedVehicle, setSelectedVehicle] = useState('Ambulance');"
)

# Add vehicle_required to payload
c_content = c_content.replace(
    "citizen_phone: citizenInfo?.phone || 'Unregistered',",
    "citizen_phone: citizenInfo?.phone || 'Unregistered',\n      vehicle_required: selectedVehicle,"
)

# Add vehicle selector UI right above SOS button area
vehicle_selector_ui = """
          {/* Emergency Vehicle Type Selector */}
          <div className="space-y-2">
            <span className="text-xs font-mono font-bold text-tertiary uppercase block text-center">Select Required Emergency Service</span>
            <div className="grid grid-cols-2 gap-2">
              {[
                { id: 'Ambulance', label: 'Ambulance', icon: 'ambulance', color: 'border-error text-error bg-error/10' },
                { id: 'Fire Engine', label: 'Fire Engine', icon: 'local_fire_department', color: 'border-primary text-primary bg-primary/10' },
                { id: 'Police Cruiser', label: 'Police Unit', icon: 'local_police', color: 'border-secondary text-secondary bg-secondary/10' },
                { id: 'Disaster Rescue', label: 'Disaster Rescue', icon: 'helicopter', color: 'border-tertiary text-tertiary bg-tertiary/10' },
              ].map(v => (
                <button
                  key={v.id}
                  type="button"
                  onClick={() => setSelectedVehicle(v.id)}
                  className={`p-3 rounded-xl border flex items-center gap-2 text-xs font-bold font-mono transition-all ${
                    selectedVehicle === v.id
                      ? `${v.color} shadow-md ring-2 ring-primary/50`
                      : 'border-outline-variant/30 bg-surface-container-high text-on-surface-variant hover:bg-surface-container-highest'
                  }`}
                >
                  <span className="material-symbols-outlined text-[20px]">{v.icon}</span>
                  <span>{v.label}</span>
                </button>
              ))}
            </div>
          </div>"""

c_content = c_content.replace(
    "{/* Location display */}",
    vehicle_selector_ui + "\n\n          {/* Location display */}"
)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)


# 2. Update DriverDashboard.jsx
drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

# Add selectedDriverUnit state
d_content = d_content.replace(
    "const [selectedIncident, setSelectedIncident] = useState(null);",
    "const [selectedIncident, setSelectedIncident] = useState(null);\n  const [driverVehicleFilter, setDriverVehicleFilter] = useState('All');"
)

# Vehicle unit filter UI
unit_filter_ui = """
        {/* Driver Emergency Vehicle Filter Tabs */}
        <div className="flex gap-2 overflow-x-auto pb-1">
          {['All', 'Ambulance', 'Fire Engine', 'Police Cruiser', 'Disaster Rescue'].map(v => (
            <button
              key={v}
              onClick={() => setDriverVehicleFilter(v)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold font-mono transition-all flex items-center gap-1.5 flex-shrink-0 border ${
                driverVehicleFilter === v
                  ? 'bg-primary text-on-primary border-primary shadow-md'
                  : 'bg-surface-container-high text-on-surface-variant border-outline-variant/20 hover:bg-surface-container-highest'
              }`}
            >
              {v === 'Ambulance' && <Truck size={14} />}
              {v === 'Fire Engine' && <ShieldAlert size={14} className="text-primary" />}
              <span>{v === 'All' ? 'All Units' : v}</span>
            </button>
          ))}
        </div>"""

d_content = d_content.replace(
    '<div className="space-y-3">\n          <h2 className="text-sm font-bold text-on-surface-variant uppercase tracking-wider">',
    unit_filter_ui + '\n\n        <div className="space-y-3">\n          <h2 className="text-sm font-bold text-on-surface-variant uppercase tracking-wider">'
)

# Filter activeDispatches by driverVehicleFilter
d_content = d_content.replace(
    'activeDispatches.map((inc) => (',
    'activeDispatches.filter(i => driverVehicleFilter === "All" || i.vehicle_required === driverVehicleFilter).map((inc) => ('
)

# Display vehicle_required badge on dispatch card
card_badge = """                    <div className="flex justify-between items-start">
                      <span className="bg-primary/20 text-primary font-mono font-bold text-xs px-2.5 py-1 rounded-lg">
                        {inc.incident_id}
                      </span>
                      <span className="bg-tertiary/20 text-tertiary font-mono text-xs px-2.5 py-1 rounded-lg font-bold uppercase">
                        UNIT REQ: {inc.vehicle_required || 'Ambulance'}
                      </span>
                    </div>"""

d_content = d_content.replace(
    """                    <div className="flex justify-between items-start">
                      <span className="bg-primary/20 text-primary font-mono font-bold text-xs px-2.5 py-1 rounded-lg">
                        {inc.incident_id}
                      </span>
                      <span className="bg-error/20 text-error font-mono text-xs px-2.5 py-1 rounded-lg font-bold uppercase">
                        {inc.emergency_type} • {Math.round(inc.severity * 100)}%
                      </span>
                    </div>""",
    card_badge
)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("Emergency vehicle options added to Citizen and Driver apps successfully")

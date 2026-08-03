import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    content = f.read()

# Add active incidents fetch & selection logic
old_states = """  // Backend state
  const [pollUrl, setPollUrl] = useState(null);
  const [citizenView, setCitizenView] = useState(null);
  const [incidentData, setIncidentData] = useState(null);"""

new_states = """  // Backend state & Multi-patient incident history
  const [pollUrl, setPollUrl] = useState(null);
  const [citizenView, setCitizenView] = useState(null);
  const [incidentData, setIncidentData] = useState(null);
  const [allCitizenIncidents, setAllCitizenIncidents] = useState([]);

  // Fetch all active incidents to allow tracking past patient emergencies
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

content = content.replace(old_states, new_states)

# Add incident tracker selector in TopHeader
old_header_buttons = """          <button
            onClick={handleLogout}
            className="flex items-center gap-1 px-3 py-1.5 rounded-full bg-surface-container-highest text-on-surface hover:bg-surface-variant transition-colors text-xs font-semibold ml-auto"
            title="Return to Main Role Dashboard"
          >
            <span className="material-symbols-outlined text-[18px]">logout</span>
            <span>Switch Role</span>
          </button>"""

new_header_buttons = """          {allCitizenIncidents.length > 0 && (
            <div className="flex items-center gap-2 ml-auto">
              <select
                value={incidentData?.incident_id || ''}
                onChange={(e) => {
                  if (e.target.value === 'new') {
                    setAppState('home');
                    setIncidentData(null);
                    setCitizenView(null);
                  } else {
                    const sel = allCitizenIncidents.find(i => i.incident_id === e.target.value);
                    if (sel) {
                      setIncidentData(sel);
                      setCitizenView(sel.citizen_view || null);
                      setPollUrl(`/api/incidents/${sel.incident_id}`);
                      setAppState(sel.citizen_view ? 'tracking' : 'loading');
                    }
                  }
                }}
                className="bg-surface-container-highest border border-outline-variant/30 text-on-surface text-xs font-mono font-bold px-2 py-1.5 rounded-full focus:outline-none"
              >
                <option value="new">+ New SOS Emergency</option>
                {allCitizenIncidents.map(inc => (
                  <option key={inc.incident_id} value={inc.incident_id}>
                    Track {inc.incident_id} ({inc.emergency_type || 'Emergency'})
                  </option>
                ))}
              </select>
            </div>
          )}

          <button
            onClick={handleLogout}
            className="flex items-center gap-1 px-3 py-1.5 rounded-full bg-surface-container-highest text-on-surface hover:bg-surface-variant transition-colors text-xs font-semibold ml-2"
            title="Return to Main Role Dashboard"
          >
            <span className="material-symbols-outlined text-[18px]">logout</span>
            <span>Switch Role</span>
          </button>"""

content = content.replace(old_header_buttons, new_header_buttons)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(content)

print("CitizenDashboard.jsx updated for multi-patient tracking & incident switching")

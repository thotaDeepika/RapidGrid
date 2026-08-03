import LiveEmergencyChat from '../components/LiveEmergencyChat';
import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';

const mapContainerStyle = { width: '100%', height: '100%', zIndex: 0 };
const LOADER_STATUSES = [
  { main: "Establishing Secure Connection...", sub: "SIGNAL STRENGTH: STRONG", step2: "Verifying Location..." },
  { main: "Triangulating GPS Coordinates...", sub: "ACCURACY: 5 METERS", step2: "Syncing Profile..." },
  { main: "Relaying Emergency Data...", sub: "PRIORITY: HIGH", step2: "Alerting Nearby Responders..." },
  { main: "Awaiting Dispatcher...", sub: "CONNECTING TO CONTROL ROOM", step2: "Finalizing Connection..." }
];

export default function CitizenDashboard() {
  const { citizenInfo, logout } = useAuth();
  const navigate = useNavigate();
  const handleLogout = () => { logout(); navigate('/', { replace: true }); };
  const isLoaded = true;

  const [appState, setAppState] = useState('home'); // home | sos | loading | tracking
  const [details, setDetails] = useState('');
  const [selectedVehicle, setSelectedVehicle] = useState('Ambulance');
  const [includeAmbulanceBackup, setIncludeAmbulanceBackup] = useState(false);
  const [activeTrackingUnit, setActiveTrackingUnit] = useState('primary'); // 'primary' | 'ambulance'
  const [locationStr, setLocationStr] = useState('Fetching location...');
  const [locationCoords, setLocationCoords] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  // Backend state & Multi-patient incident history
  const [pollUrl, setPollUrl] = useState(null);
  const [citizenView, setCitizenView] = useState(null);
  const [incidentData, setIncidentData] = useState(null);
  const [allCitizenIncidents, setAllCitizenIncidents] = useState([]);

  // Fetch active incidents belonging strictly to THIS logged-in citizen account
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
  }, [appState, incidentData, citizenInfo]);

  // Loader animation index — stable, only increments
  const [loaderIndex, setLoaderIndex] = useState(0);
  const loaderStatus = LOADER_STATUSES[loaderIndex % LOADER_STATUSES.length];

  // ─── Loader animation: stable interval, no deps on loaderIndex ──────────
  useEffect(() => {
    if (appState !== 'loading') return;
    const id = setInterval(() => setLoaderIndex(i => i + 1), 3500);
    return () => clearInterval(id);
  }, [appState]);

  // ─── Polling: poll /api/incidents/:id every 2s while loading ────────────
  useEffect(() => {
    if (appState !== 'loading' || !pollUrl) return;

    const poll = async () => {
      try {
        const res = await fetch(pollUrl); // relative URL via Vite proxy
        if (!res.ok) return;
        const data = await res.json();
        console.log('[GeoAgentic] Poll result:', data.status, data);

        if (
          data.status === 'awaiting_dispatcher_approval' ||
          data.status === 'dispatched' ||
          data.status === 'completed'
        ) {
          setIncidentData(data);
          setCitizenView(data.citizen_view || null);
          setAppState('tracking');
        }
      } catch (err) {
        console.error('[GeoAgentic] Poll error:', err);
      }
    };

    poll(); // immediate first poll
    const id = setInterval(poll, 2000);
    return () => clearInterval(id);
  }, [appState, pollUrl]);

  // ─── Get location ────────────────────────────────────────────────────────
  const handleUseLocation = () => {
    if (window.navigator?.vibrate) window.navigator.vibrate(100);
    if (!navigator.geolocation) {
      setLocationStr('GPS not supported');
      setLocationCoords({ lat: 12.9756, lng: 77.6068 }); // Bangalore default
      setAppState('sos');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        setLocationCoords({ lat, lng });
        setLocationStr(`${lat.toFixed(4)}°N, ${lng.toFixed(4)}°E`);
        setAppState('sos');
      },
      () => {
        // Denied — use Bangalore MG Road default for demo
        setLocationCoords({ lat: 12.9756, lng: 77.6068 });
        setLocationStr('12.9756°N, 77.6068°E (Default)');
        setAppState('sos');
      }
    );
  };

  // ─── Fire SOS ────────────────────────────────────────────────────────────
  const handleSOSTrigger = async () => {
    if (window.navigator?.vibrate) window.navigator.vibrate([200, 100, 200]);
    setErrorMsg(null);
    setAppState('loading');
    setLoaderIndex(0);

    const payload = {
      citizen_text: details.trim() || `Emergency reported for ${selectedVehicle}.`,
      citizen_name: citizenInfo?.name || 'Anonymous Citizen',
      citizen_phone: citizenInfo?.phone || 'Unregistered',
      vehicle_required: selectedVehicle,
      include_ambulance_backup: includeAmbulanceBackup,
      location: locationCoords || { lat: 12.9756, lng: 77.6068 },
      input_modality: 'text',
      timestamp: new Date().toISOString()
    };

    console.log('[GeoAgentic] POST /api/incidents', payload);

    try {
      const res = await fetch('/api/incidents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      console.log('[GeoAgentic] Incident created:', data);

      if (res.status === 202 || res.ok) {
        setPollUrl(data.poll_url); // e.g. /api/incidents/INC-xxxx
      } else {
        setErrorMsg('Backend error: ' + (data.detail || res.status));
        setAppState('sos');
      }
    } catch (err) {
      console.error('[GeoAgentic] POST error:', err);
      setErrorMsg('Cannot reach backend. Is the server running?');
      setAppState('sos');
    }
  };

  const addDetail = (text) => {
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
  };

  // ─── Shared header ───────────────────────────────────────────────────────
  const TopHeader = ({ title, onBack }) => (
    <header className="fixed top-0 inset-x-0 z-50 bg-surface/80 backdrop-blur-xl pt-safe shadow-[0_1px_8px_rgba(0,0,0,0.2)]">
      <div className="h-16 px-4 flex items-center gap-stack-sm">
        {onBack && (
          <button
            onClick={onBack}
            className="w-12 h-12 flex items-center justify-center text-on-surface active:bg-surface-container-highest rounded-full transition-colors"
          >
            <span className="material-symbols-outlined">arrow_back</span>
          </button>
        )}
        <div className={`flex items-center gap-stack-xs ${title === 'Home' ? 'w-full justify-between' : ''}`}>
          <div className="flex items-center gap-stack-xs">
            <span className="material-symbols-outlined text-primary text-[28px]" style={{ fontVariationSettings: "'FILL' 1" }}>monitor_heart</span>
            <h1 className="font-headline-md text-headline-md text-on-surface">{title}</h1>
          </div>
          {allCitizenIncidents.length > 0 && (
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

          <div className="hidden sm:flex items-center gap-2 bg-tertiary/10 border border-tertiary/30 px-3 py-1 rounded-full text-xs font-mono text-tertiary font-bold ml-2">
            <span className="material-symbols-outlined text-[16px]">account_circle</span>
            <span>{citizenInfo?.name || "Ananya Sharma"}</span>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-surface-container-highest text-on-surface hover:bg-surface-variant transition-colors text-xs font-semibold ml-2 border border-outline-variant/30"
            title="Sign Out of Citizen App"
          >
            <span className="material-symbols-outlined text-[16px]">logout</span>
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </header>
  );

  // ════════════════════════════════════════════════════════════════════
  // STATE 1 — HOME
  // ════════════════════════════════════════════════════════════════════
  if (appState === 'home') return (
    <div className="bg-surface font-body-md text-on-surface flex flex-col min-h-screen">
      <TopHeader title="Home" />
      <main className="flex-1 flex flex-col relative w-full pt-16 pb-20 bg-surface">
        {/* Ambient glow background */}
        <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-10 w-64 h-64 rounded-full bg-primary/5 blur-3xl"></div>
          <div className="absolute top-40 right-5 w-48 h-48 rounded-full bg-tertiary/5 blur-3xl"></div>
          <div className="absolute inset-0 bg-gradient-to-t from-surface via-surface/80 to-surface/20"></div>
        </div>

        <div className="relative z-10 px-margin-mobile pt-stack-lg">
          <div className="flex justify-between items-start">
            <div className="bg-surface-container/90 backdrop-blur-md rounded-full px-4 py-2 flex items-center gap-2 shadow-xl border-l-4 border-tertiary">
              <span className="flex h-2 w-2 rounded-full bg-tertiary animate-pulse"></span>
              <span className="font-label-caps text-label-caps text-on-surface">SAFETY LEVEL: HIGH</span>
            </div>
            <button className="w-12 h-12 bg-surface-container/90 backdrop-blur-md rounded-full flex items-center justify-center shadow-xl active:scale-95 transition-transform">
              <span className="material-symbols-outlined text-primary">my_location</span>
            </button>
          </div>
        </div>

        <div className="flex-grow min-h-[50vh]"></div>

        <div className="relative z-20 px-margin-mobile pb-stack-xl">
          <div className="bg-surface-container-high rounded-xl p-stack-lg shadow-2xl space-y-stack-md">
            <div className="space-y-stack-xs text-center pb-stack-xs">
              <h2 className="font-headline-md text-headline-md text-on-surface">Stay Protected</h2>
              <p className="font-body-md text-body-md text-on-surface-variant">Real-time safety alerts for your immediate surroundings.</p>
            </div>
            <button
              onClick={handleUseLocation}
              className="w-full h-14 bg-primary-container hover:bg-primary-container/90 text-on-primary-container rounded-lg flex items-center justify-center gap-3 shadow-[0_4px_0_0_rgba(147,0,19,1)] active:shadow-none active:translate-y-1 transition-all duration-75"
            >
              <span className="material-symbols-outlined text-[24px]">near_me</span>
              <span className="font-headline-md text-headline-md">Use Current Location</span>
            </button>
            <button
              onClick={() => { setLocationCoords({ lat: 12.9756, lng: 77.6068 }); setLocationStr('MG Road, Bengaluru'); setAppState('sos'); }}
              className="w-full h-14 bg-surface-container-highest hover:bg-surface-variant text-on-surface rounded-lg flex items-center justify-center gap-3 transition-colors active:scale-[0.98]"
            >
              <span className="material-symbols-outlined text-[24px]">map</span>
              <span className="font-headline-md text-headline-md">Select on Map</span>
            </button>
            <div className="flex items-center justify-center gap-2 pt-stack-sm opacity-60">
              <span className="material-symbols-outlined text-[16px]">verified_user</span>
              <span className="font-label-caps text-label-caps">End-to-End Encrypted Data</span>
            </div>
          </div>
        </div>
      </main>

      <nav className="fixed bottom-0 inset-x-0 z-50 pb-safe bg-surface/90 backdrop-blur-xl shadow-[0_-1px_8px_rgba(0,0,0,0.2)]">
        <div className="flex justify-around items-center h-20 px-gutter">
          <button className="flex flex-col items-center justify-center gap-stack-xs w-16 h-16 transition-all text-primary font-bold">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>home</span>
            <span className="font-label-caps text-label-caps">Home</span>
          </button>
          <button className="flex flex-col items-center justify-center gap-stack-xs w-16 h-16 text-on-surface-variant transition-all hover:text-on-surface">
            <span className="material-symbols-outlined">emergency</span>
            <span className="font-label-caps text-label-caps">Incidents</span>
          </button>
          <button className="flex flex-col items-center justify-center gap-stack-xs w-16 h-16 text-on-surface-variant transition-all hover:text-on-surface">
            <span className="material-symbols-outlined">notifications</span>
            <span className="font-label-caps text-label-caps">Alerts</span>
          </button>
          <button className="flex flex-col items-center justify-center gap-stack-xs w-16 h-16 text-on-surface-variant transition-all hover:text-on-surface">
            <span className="material-symbols-outlined">settings</span>
            <span className="font-label-caps text-label-caps">Settings</span>
          </button>
        </div>
      </nav>
    </div>
  );

  // ════════════════════════════════════════════════════════════════════
  // STATE 2 — SOS TRIGGER
  // ════════════════════════════════════════════════════════════════════
  if (appState === 'sos') return (
    <div className="bg-surface font-body-md text-on-surface flex flex-col min-h-screen">
      <TopHeader title="Sos Trigger" onBack={() => setAppState('home')} />
      <main className="flex-1 flex flex-col w-full pt-16 pb-16 bg-surface overflow-y-auto space-y-4">
        <div className="flex flex-col w-full p-gutter gap-stack-lg">
          {/* GPS status */}
          <div className="flex items-center justify-between bg-surface-container-high p-4 rounded-xl">
            <div className="flex items-center gap-stack-sm">
              <div className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
              </div>
              <span className="font-status-code text-status-code text-on-surface uppercase tracking-wider">Live GPS Active</span>
            </div>
            <span className="font-status-code text-status-code text-primary">100% Signal</span>
          </div>

          {/* Error banner */}
          {errorMsg && (
            <div className="bg-error-container text-on-error-container p-4 rounded-xl flex items-center gap-3">
              <span className="material-symbols-outlined">error</span>
              <span className="font-body-md text-body-md">{errorMsg}</span>
            </div>
          )}

          <div className="space-y-stack-xs">
            <h2 className="font-headline-md text-headline-md text-on-surface">Emergency Details</h2>
            <p className="font-body-md text-body-md text-on-surface-variant">Your location is being shared. Add details for faster dispatch.</p>
          </div>

          {/* Text input */}
          <div className="relative">
            <textarea
              value={details}
              onChange={(e) => setDetails(e.target.value)}
              className="w-full h-40 bg-surface-container text-on-surface p-4 rounded-xl border-none focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200 resize-none text-[18px] placeholder:text-outline"
              placeholder="e.g., 'chest pain', 'fire on 3rd floor', 'road accident'..."
            />
            <div className="absolute bottom-4 right-4 flex gap-stack-sm">
              <button className="bg-surface-container-highest p-2 rounded-full text-on-surface active:scale-95 transition-transform">
                <span className="material-symbols-outlined text-[20px]">mic</span>
              </button>
              <button className="bg-surface-container-highest p-2 rounded-full text-on-surface active:scale-95 transition-transform">
                <span className="material-symbols-outlined text-[20px]">photo_camera</span>
              </button>
            </div>
          </div>

          {/* Quick chips */}
          <div className="flex flex-wrap gap-stack-sm">
            {['Medical Help', 'Fire/Smoke', 'Police/Security', 'Accident', 'Breathing Difficulty'].map(chip => (
              <button
                key={chip}
                onClick={() => addDetail(chip)}
                className="bg-surface-container-low px-4 py-2 rounded-full font-label-caps text-label-caps text-on-surface active:bg-primary-container active:text-on-primary-container transition-colors"
              >
                {chip.toUpperCase()}
              </button>
            ))}
          </div>

          {/* Emergency Service & Vehicle Type Selector */}
          <div className="space-y-2">
            <span className="text-xs font-mono font-bold text-tertiary uppercase block text-center">Select Required Emergency Service</span>
            <div className="grid grid-cols-2 gap-2">
              {[
                { id: 'Ambulance', label: 'Medical Ambulance', icon: 'ambulance', color: 'border-error text-error bg-error/10' },
                { id: 'Fire Engine', label: 'Fire Engine Rescue', icon: 'local_fire_department', color: 'border-primary text-primary bg-primary/10' },
                { id: 'Police Cruiser', label: 'Police Patrol Unit', icon: 'local_police', color: 'border-secondary text-secondary bg-secondary/10' },
                { id: 'Disaster Rescue', label: 'Disaster Search & Rescue', icon: 'helicopter', color: 'border-tertiary text-tertiary bg-tertiary/10' },
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
          </div>

            {/* Dynamic Multi-Vehicle Backup Prompt based on Emergency Service */}
            <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/30 text-xs font-mono space-y-2">
              {selectedVehicle === 'Ambulance' && (
                <div className="flex items-center gap-2 text-tertiary font-bold">
                  <span className="material-symbols-outlined text-[18px]">medical_services</span>
                  <span>Direct Medical Ambulance Dispatch (Patient Hospital Transport)</span>
                </div>
              )}

              {selectedVehicle === 'Fire Engine' && (
                <label className="flex items-center gap-2 cursor-pointer text-on-surface hover:text-primary transition-colors">
                  <input
                    type="checkbox"
                    checked={includeAmbulanceBackup}
                    onChange={(e) => setIncludeAmbulanceBackup(e.target.checked)}
                    className="w-4 h-4 rounded border-outline-variant text-primary focus:ring-primary accent-primary"
                  />
                  <span className="font-bold">Also Request Medical Ambulance Standby (For Burn/Injury Backup)</span>
                </label>
              )}

              {selectedVehicle === 'Police Cruiser' && (
                <label className="flex items-center gap-2 cursor-pointer text-on-surface hover:text-secondary transition-colors">
                  <input
                    type="checkbox"
                    checked={includeAmbulanceBackup}
                    onChange={(e) => setIncludeAmbulanceBackup(e.target.checked)}
                    className="w-4 h-4 rounded border-outline-variant text-secondary focus:ring-secondary accent-secondary"
                  />
                  <span className="font-bold">Also Request Medical Ambulance Backup (For Collision/Victim Injuries)</span>
                </label>
              )}

              {selectedVehicle === 'Disaster Rescue' && (
                <label className="flex items-center gap-2 cursor-pointer text-on-surface hover:text-tertiary transition-colors">
                  <input
                    type="checkbox"
                    checked={includeAmbulanceBackup}
                    onChange={(e) => setIncludeAmbulanceBackup(e.target.checked)}
                    className="w-4 h-4 rounded border-outline-variant text-tertiary focus:ring-tertiary accent-tertiary"
                  />
                  <span className="font-bold">Also Request Medical Ambulance Unit (For Disaster Evacuation Backup)</span>
                </label>
              )}
            </div>

          {/* Location display */}
          <div className="relative h-16 w-full rounded-xl overflow-hidden bg-surface-container-high shadow-xl flex items-center px-4 gap-3">
            <span className="material-symbols-outlined text-primary text-[22px]" style={{ fontVariationSettings: "'FILL' 1" }}>location_on</span>
            <div>
              <div className="font-label-caps text-label-caps text-on-surface-variant">DETECTED LOCATION</div>
              <div className="font-status-code text-status-code text-on-surface">{locationStr}</div>
            </div>
          </div>

          {/* SOS button area */}
          <div className="flex flex-col items-center gap-stack-md pt-stack-md pb-8">
            <div className="relative w-full max-w-[280px] aspect-square flex items-center justify-center">
              <div className="absolute inset-0 rounded-full bg-primary/20 animate-ping" style={{ animationDuration: '2s' }}></div>
              <div className="absolute inset-4 rounded-full bg-primary/30 animate-pulse" style={{ animationDuration: '3s' }}></div>
              <button
                onClick={handleSOSTrigger}
                className="relative w-48 h-48 bg-primary rounded-full flex flex-col items-center justify-center text-on-primary shadow-[0_12px_48px_rgba(255,179,173,0.4),inset_0_4px_4px_rgba(255,255,255,0.4),inset_0_-8px_16px_rgba(0,0,0,0.3)] active:translate-y-2 active:shadow-none transition-all"
              >
                <span className="text-[48px] font-black leading-none tracking-tighter" style={{ fontFamily: 'Inter' }}>SOS</span>
                <span className="font-label-caps text-label-caps opacity-80 mt-1">TAP TO SEND</span>
              </button>
            </div>
            <p className="font-body-md text-body-md text-center text-on-surface-variant max-w-[240px]">
              Tap to immediately alert emergency services. Help will arrive as fast as possible.
            </p>
          </div>
        </div>
      </main>
    </div>
  );

  // ════════════════════════════════════════════════════════════════════
  // STATE 3 — LOADING / PROCESSING
  // ════════════════════════════════════════════════════════════════════
  if (appState === 'loading') return (
    <div className="bg-surface font-body-md text-on-surface flex flex-col min-h-screen">
      <TopHeader title="Incident Details" />
      <main className="flex-1 flex flex-col w-full pt-16 bg-surface">
        {/* Background glow */}
        <div className="fixed inset-0 z-0 pointer-events-none">
          <div className="absolute top-20 left-1/2 -translate-x-1/2 w-96 h-96 rounded-full bg-primary/5 blur-3xl"></div>
          <div className="absolute inset-0 bg-gradient-to-b from-surface/80 via-surface/95 to-surface"></div>
        </div>

        <div className="relative z-10 flex flex-col px-margin-mobile gap-stack-xl pt-stack-xl">
          {/* Central loader */}
          <div className="flex flex-col items-center justify-center py-stack-xl">
            <div className="relative w-48 h-48 flex items-center justify-center">
              <div className="absolute inset-0 rounded-full bg-primary/10 animate-ping" style={{ animationDuration: '3s' }}></div>
              <div className="absolute inset-4 rounded-full bg-primary/20 animate-ping" style={{ animationDuration: '2s' }}></div>
              <svg className="w-full h-full -rotate-90 transform" viewBox="0 0 100 100">
                <circle className="stroke-surface-container-highest" cx="50" cy="50" fill="transparent" r="45" strokeWidth="4" />
                <circle
                  className="stroke-primary"
                  cx="50" cy="50" fill="transparent" r="45"
                  strokeDasharray="283"
                  strokeDashoffset={Math.max(0, 180 - ((loaderIndex % 4) * 45))}
                  strokeLinecap="round" strokeWidth="5"
                  style={{ transition: 'stroke-dashoffset 2s ease-in-out' }}
                />
              </svg>
              <div className="absolute inset-10 bg-primary-container rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(255,84,81,0.4)]">
                <span
                  className="material-symbols-outlined text-on-primary-container text-[40px] animate-pulse"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  shield_with_heart
                </span>
              </div>
            </div>
            <div className="mt-stack-lg text-center flex flex-col gap-stack-xs">
              <h2 className="font-headline-md text-headline-md text-on-surface" style={{ transition: 'opacity 0.3s' }}>
                {loaderStatus.main}
              </h2>
              <p className="font-status-code text-status-code text-primary uppercase tracking-widest">
                {loaderStatus.sub}
              </p>
            </div>
          </div>

          {/* Timeline */}
          <div className="bg-surface-container/60 backdrop-blur-md rounded-xl p-stack-lg flex flex-col gap-stack-md shadow-xl">
            <div className="flex items-center gap-stack-md">
              <div className="w-8 h-8 rounded-full bg-tertiary/20 flex items-center justify-center">
                <span className="material-symbols-outlined text-tertiary text-[20px]">check_circle</span>
              </div>
              <div>
                <span className="font-label-caps text-label-caps text-on-surface block">Step 1</span>
                <span className="font-body-md text-on-surface">SOS Signal Sent</span>
              </div>
            </div>
            <div className="flex items-center gap-stack-md">
              <div className="relative w-8 h-8 flex items-center justify-center">
                <div className="absolute inset-0 bg-primary/20 rounded-full animate-pulse"></div>
                <span className="material-symbols-outlined text-primary text-[20px] animate-spin">sync</span>
              </div>
              <div>
                <span className="font-label-caps text-label-caps text-on-surface opacity-60 block">Step 2</span>
                <span className="font-body-md text-on-surface">{loaderStatus.step2}</span>
              </div>
            </div>
            <div className="flex items-center gap-stack-md opacity-30">
              <div className="w-8 h-8 rounded-full bg-surface-container-highest flex items-center justify-center">
                <span className="material-symbols-outlined text-on-surface text-[20px]">emergency_share</span>
              </div>
              <div>
                <span className="font-label-caps text-label-caps text-on-surface block">Step 3</span>
                <span className="font-body-md text-on-surface">Connecting to Dispatch</span>
              </div>
            </div>
          </div>

          <div className="flex items-start gap-stack-sm bg-surface-container-low p-stack-md rounded-lg">
            <span className="material-symbols-outlined text-secondary flex-shrink-0">info</span>
            <p className="font-body-md text-on-surface-variant text-sm">
              Stay on this screen. Our AI agents are analysing your emergency and routing the nearest ambulance.
              {pollUrl && <span className="text-primary"> Tracking ID: {pollUrl.split('/').pop()}</span>}
            </p>
          </div>
        </div>
      </main>
    </div>
  );

  // ════════════════════════════════════════════════════════════════════
  // STATE 4 — TRACKING (dispatched / awaiting approval)
  // ════════════════════════════════════════════════════════════════════
  // Prefer citizenView (richer, from new backend) over action_plan fields
  const hospitalName = citizenView?.hospital_name
    || incidentData?.action_plan?.recommended_hospital?.name
    || 'Nearest Hospital';
  const etaMinutes = citizenView?.eta_minutes ?? 8;
  const emergencyType = citizenView?.emergency_type
    || incidentData?.emergency_type
    || 'Emergency';
  const severity = citizenView?.severity
    ? Math.round(citizenView.severity * 100)
    : incidentData?.severity
      ? Math.round(incidentData.severity * 100)
      : null;
  const distanceKm = citizenView?.distance_meters
    ? (citizenView.distance_meters / 1000).toFixed(1)
    : null;

  const origin = citizenView?.origin || locationCoords || { lat: 12.9756, lng: 77.6068 };
  const unitStatuses = citizenView?.unit_statuses || incidentData?.unit_statuses || { primary: incidentData?.status || 'dispatched', ambulance: 'dispatched' };
  const hospLoc = citizenView?.hospital_location;
  const routeCoords = citizenView?.route_coordinates || [];
  const mapCenter = hospLoc || origin;

  return (
    <div className="bg-surface font-body-md text-on-surface flex flex-col min-h-screen">
      <TopHeader title="Incident Details" />
      <main className="flex-1 flex flex-col w-full pt-16 pb-16 bg-surface overflow-y-auto space-y-4">
        {/* ── Real Google Maps ── */}
        <div className="relative w-full h-[32vh] overflow-hidden bg-surface-container-low flex-shrink-0">
          {isLoaded && hospLoc ? (
            <MapContainer center={[mapCenter.lat, mapCenter.lng]} zoom={13} style={mapContainerStyle} zoomControl={false} attributionControl={false}>
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
            </MapContainer>
          ) : (
            /* Fallback animated map while route loads */
            <div className="absolute inset-0 flex items-center justify-center bg-surface-container">
              <div className="relative flex items-center justify-center">
                <div className="absolute w-32 h-32 bg-primary/10 rounded-full animate-ping" style={{ animationDuration: '3s' }}></div>
                <div className="absolute w-20 h-20 bg-primary/20 rounded-full animate-ping" style={{ animationDuration: '2s' }}></div>
                <div className="w-5 h-5 bg-primary rounded-full shadow-[0_0_16px_rgba(255,84,81,0.8)]"></div>
              </div>
            </div>
          )}
          {/* Station Base Hub Badge Overlay */}
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
          </div>
          {/* Hospital destination label */}
          <div className="absolute bottom-4 left-4 bg-surface-container/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10 max-w-[60%]">
            <span className="material-symbols-outlined text-secondary text-[16px]">local_hospital</span>
            <span className="font-status-code text-status-code text-on-surface truncate">{hospitalName}</span>
          </div>
          {/* Distance badge */}
          {distanceKm && (
            <div className="absolute bottom-4 right-4 bg-surface-container/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10">
              <span className="material-symbols-outlined text-primary text-[16px]">straighten</span>
              <span className="font-status-code text-status-code text-on-surface">{distanceKm} km</span>
            </div>
          )}
        </div>

        {/* Responder card */}
        <div className="px-margin-mobile mt-4 relative z-10 space-y-stack-md pb-8">
          <div className="bg-surface-container-high rounded-xl p-stack-md shadow-2xl border-l-4 border-primary">
                        {/* Station Base Hub Info Block */}
            <div className="bg-surface-container-low p-3.5 rounded-xl border border-[#FFB900]/30 flex items-center justify-between shadow-md mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#FFB900]/20 text-[#FFB900] flex items-center justify-center font-bold">
                  <span className="material-symbols-outlined text-[22px]">local_convenience_store</span>
                </div>
                <div>
                  <div className="text-[10px] font-mono font-bold text-[#FFB900] uppercase tracking-wider">
                    DISPATCHED FROM STATION HUB
                  </div>
                  <div className="text-xs font-bold text-on-surface font-mono">
                    {citizenView?.phase1_hub?.name || 'Hebbal Emergency Response Station'}
                  </div>
                </div>
              </div>
              <div className="text-right font-mono">
                <div className="text-xs font-bold text-[#FFB900]">{citizenView?.phase1_eta_minutes || 5}m Response</div>
                <div className="text-[9px] text-on-surface-variant uppercase">Phase 1 Route</div>
              </div>
            </div>

            {/* Dynamic Single vs Dual Emergency Unit Status Cards */}
            <div className="bg-surface-container-low p-3.5 rounded-xl border border-outline-variant/30 mb-4 space-y-2">
              <div className="flex justify-between items-center text-[10px] font-mono font-bold uppercase tracking-wider text-tertiary">
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
                  {(citizenView?.include_ambulance_backup || incidentData?.include_ambulance_backup) ? 'Assigned Field Units (Primary + Medical Standby)' : 'Assigned Emergency Field Unit'}
                </span>
                <span className="text-on-surface-variant font-normal">Realtime GPS Telemetry</span>
              </div>

              <div className={`grid grid-cols-1 ${(citizenView?.include_ambulance_backup || incidentData?.include_ambulance_backup) ? 'sm:grid-cols-2' : ''} gap-3 pt-1`}>
                {/* Primary Dispatched Unit (Interactive Click Tab) */}
                <div 
                  onClick={() => setActiveTrackingUnit('primary')}
                  className={`bg-surface-container p-3 rounded-xl border cursor-pointer transition-all space-y-1.5 shadow-md ${
                    activeTrackingUnit === 'primary' 
                      ? 'border-primary ring-2 ring-primary/60 bg-surface-container-highest/50' 
                      : 'border-primary/30 hover:border-primary/70'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-mono font-black text-primary uppercase flex items-center gap-1.5">
                      <span className="material-symbols-outlined text-[16px]">
                        {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'local_fire_department' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'local_police' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'helicopter' : 'ambulance'}
                      </span>
                      {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE-UNIT-09 (Fire Engine)' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'POLICE-UNIT-02 (Police)' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'RESCUE-UNIT-01 (Disaster Rescue)' : 'AMB-UNIT-04 (Medical Ambulance)'}
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary/20 text-primary font-bold">
                      {unitStatuses.primary === 'arrived' || incidentData?.status === 'completed' ? 'ARRIVED ON SITE' : 'EN ROUTE'}
                    </span>
                  </div>
                  <div className="text-[11px] text-on-surface-variant font-mono">
                    Target: <strong className="text-on-surface font-semibold">
                      {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Emergency Scene' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Incident Scene' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Hazard Zone 4' : hospitalName}
                    </strong>
                  </div>
                  <div className="text-[10px] text-primary font-mono font-bold flex justify-between items-center">
                    <span>ETA: {incidentData?.status === 'completed' ? '0m (Arrived)' : `${etaMinutes} mins`}</span>
                    <span className="text-[9px] text-tertiary font-bold uppercase underline">Click to inspect</span>
                  </div>
                </div>

                {/* Optional Medical Ambulance Backup (Interactive Click Tab) */}
                {(citizenView?.include_ambulance_backup || incidentData?.include_ambulance_backup) ? (
                  <div 
                    onClick={() => setActiveTrackingUnit('ambulance')}
                    className={`bg-surface-container p-3 rounded-xl border cursor-pointer transition-all space-y-1.5 shadow-md ${
                      activeTrackingUnit === 'ambulance' 
                        ? 'border-tertiary ring-2 ring-tertiary/60 bg-surface-container-highest/50' 
                        : 'border-tertiary/30 hover:border-tertiary/70'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-mono font-black text-tertiary uppercase flex items-center gap-1.5">
                        <span className="material-symbols-outlined text-[16px]">medical_services</span>
                        AMB-UNIT-04 (Medical Ambulance Backup)
                      </span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-tertiary/20 text-tertiary font-bold">
                        {unitStatuses.ambulance === 'arrived' || incidentData?.status === 'completed' ? 'ON SITE STANDBY' : 'EN ROUTE (BACKUP)'}
                      </span>
                    </div>
                    <div className="text-[11px] text-on-surface-variant font-mono">
                      Target: <strong className="text-on-surface font-semibold">{hospitalName}</strong>
                    </div>
                    <div className="text-[10px] text-tertiary font-mono font-bold flex justify-between items-center">
                      <span>ETA: {incidentData?.status === 'completed' ? '0m (Bed Reserved)' : `${Math.max(1, etaMinutes - 2)} mins (ER Standby)`}</span>
                      <span className="text-[9px] text-tertiary font-bold uppercase underline">Click to inspect</span>
                    </div>
                  </div>
                ) : (
                  <div className="bg-surface-container/60 p-3 rounded-xl border border-dashed border-tertiary/40 flex flex-col items-center justify-center gap-1 text-center">
                    <span className="text-xs font-mono font-bold text-on-surface-variant">Need Medical Backup for Injury / Burn?</span>
                    <button
                      onClick={async () => {
                        if (!incidentData?.incident_id) return;
                        try {
                          await fetch(`/api/incidents/${incidentData.incident_id}/request_ambulance`, { method: 'POST' });
                          setIncidentData(prev => ({ ...prev, include_ambulance_backup: true }));
                          setCitizenView(prev => ({ ...prev, include_ambulance_backup: true }));
                        } catch (err) {}
                      }}
                      className="px-3 py-1.5 bg-tertiary/20 text-tertiary hover:bg-tertiary/30 rounded-xl text-xs font-mono font-bold border border-tertiary/40 flex items-center gap-1 transition-all"
                    >
                      <span className="material-symbols-outlined text-[16px]">medical_services</span>
                      + DISPATCH AMBULANCE BACKUP NOW
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Emergency type + severity */}
            <div className="flex items-center gap-2 mb-stack-sm">
              <span className="bg-primary-container text-on-primary-container font-label-caps text-label-caps px-3 py-1 rounded-full uppercase">
                {emergencyType}
              </span>
              {severity && (
                <span className="bg-surface-container text-on-surface-variant font-label-caps text-label-caps px-3 py-1 rounded-full">
                  Severity: {severity}%
                </span>
              )}
            </div>

            <div className="flex items-start justify-between mb-stack-md">
              <div className="flex items-center gap-stack-md">
                <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${activeTrackingUnit === 'ambulance' ? 'bg-tertiary/20 text-tertiary' : 'bg-primary-container text-on-primary-container'}`}>
                  <span className="material-symbols-outlined text-[28px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                    {activeTrackingUnit === 'ambulance'
                      ? 'medical_services'
                      : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'local_fire_department' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'local_police' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'helicopter' : 'ambulance'}
                  </span>
                </div>
                <div>
                  <h2 className="font-headline-md text-headline-md text-on-surface">
                    {activeTrackingUnit === 'ambulance'
                      ? (unitStatuses.ambulance === 'arrived' || incidentData?.status === 'completed' ? 'Medical Ambulance Arrived - On Site' : 'Medical Ambulance Unit En Route')
                      : (unitStatuses.primary === 'arrived' || incidentData?.status === 'completed' 
                          ? `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance'} Arrived - On Site` 
                          : `${(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Rescue Engine' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Police Patrol Unit' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Disaster Rescue' ? 'Disaster Rescue Unit' : 'Medical Ambulance Unit'} En Route`)}
                  </h2>
                  <p className={`font-status-code text-status-code font-mono font-bold flex items-center gap-1.5 mt-0.5 ${activeTrackingUnit === 'ambulance' ? 'text-tertiary' : 'text-primary'}`}>
                    <span className={`w-2 h-2 rounded-full animate-ping ${activeTrackingUnit === 'ambulance' ? 'bg-tertiary' : 'bg-primary'}`}></span>
                    {activeTrackingUnit === 'ambulance'
                      ? (unitStatuses.ambulance === 'arrived' || incidentData?.status === 'completed' ? 'MEDICAL AMBULANCE STANDBY ON SITE' : 'PARAMEDIC DISPATCHED FOR MEDICAL BACKUP')
                      : (unitStatuses.primary === 'arrived' || incidentData?.status === 'completed' 
                          ? ((citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE CONTROL ACTIVE ON SCENE' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'SCENE SECURED BY POLICE' : 'ARRIVED AT HOSPITAL ER') 
                          : incidentData?.status === 'dispatched' || incidentData?.driver_claimed ? 'FIRST RESPONDER EN ROUTE TO SITE' : 'AI DISPATCH APPROVED - UNIT EN ROUTE')}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <div className={`font-black text-[32px] leading-none ${activeTrackingUnit === 'ambulance' ? 'text-tertiary' : 'text-primary'}`} style={{ fontFamily: 'Inter' }}>
                  {incidentData?.status === 'completed' ? '0m' : activeTrackingUnit === 'ambulance' ? `${Math.max(1, etaMinutes - 2)}m` : `${etaMinutes}m`}
                </div>
                <p className="font-label-caps text-label-caps text-on-surface-variant uppercase">
                  {incidentData?.status === 'completed' ? 'ARRIVED' : 'Arrival'}
                </p>
              </div>
            </div>

            {/* Timeline dots */}
            <div className="relative py-stack-sm">
              <div className="absolute top-1/2 left-0 w-full h-0.5 bg-surface-container-lowest -translate-y-1/2"></div>
              <div
                className="absolute top-1/2 left-0 h-0.5 bg-tertiary -translate-y-1/2 transition-all duration-1000"
                style={{ width: (activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'arrived' || incidentData?.status === 'completed' ? '100%' : (activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'dispatched' || incidentData?.status === 'dispatched' ? '66%' : '33%' }}
              ></div>
              <div className="relative flex justify-between">
                <div className="flex flex-col items-center gap-1">
                  <div className="w-3 h-3 bg-tertiary rounded-full ring-4 ring-surface-container-high z-10"></div>
                  <span className="font-label-caps text-label-caps text-tertiary">REPORTED</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-3 h-3 rounded-full ring-4 ring-surface-container-high z-10 ${(activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'dispatched' || (activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'arrived' || incidentData?.status === 'dispatched' || incidentData?.status === 'completed' ? 'bg-tertiary' : 'bg-outline'}`}></div>
                  <span className="font-label-caps text-label-caps text-tertiary">DISPATCHED</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-3 h-3 rounded-full ring-4 ring-surface-container-high z-10 ${(activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'arrived' || incidentData?.status === 'completed' ? 'bg-tertiary animate-pulse' : 'bg-outline'}`}></div>
                  <span className={`font-label-caps text-label-caps ${(activeTrackingUnit === 'ambulance' ? unitStatuses.ambulance : unitStatuses.primary) === 'arrived' || incidentData?.status === 'completed' ? 'text-tertiary font-bold' : 'text-on-surface opacity-40'}`}>ON SITE</span>
                </div>
              </div>
            </div>
          </div>


          


          {/* Real-time Socket Chat Section */}
          <div id="socket-chat-section" className="scroll-mt-20">
            {incidentData?.incident_id && (
              <LiveEmergencyChat 
                incidentId={incidentData.incident_id}
                senderRole="citizen"
                senderName={citizenInfo?.name || 'Citizen User'}
                driverPhone="+919876543210"
                hospitalPhone="112"
                hospitalName={hospitalName}
                vehicleRequired={citizenView?.vehicle_required || incidentData?.vehicle_required || 'Ambulance'}
                includeAmbulanceBackup={citizenView?.include_ambulance_backup || incidentData?.include_ambulance_backup || false}
              />
            )}
          </div>

          {/* Direct Paramedic Communication Card */}
          <div className="bg-surface-container rounded-xl p-stack-md flex flex-col gap-2 border border-tertiary/30">
            <div className="text-xs font-bold font-mono text-tertiary uppercase flex items-center gap-2">
              <span className="material-symbols-outlined text-[18px]">support_agent</span>
              Direct First Responder Contact (Unit AMB-UNIT-04)
            </div>
            <div className="grid grid-cols-2 gap-2 mt-1">
              <a 
                href="tel:+919876543210" 
                className="bg-tertiary text-on-tertiary font-bold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-2 shadow-md hover:bg-tertiary/90 transition-all text-center"
              >
                <span className="material-symbols-outlined text-[18px]">call</span>
                Call Paramedic
              </a>
              <a 
                href="sms:+919876543210?body=Emergency%20Update%20from%20Citizen" 
                className="bg-surface-container-highest text-on-surface font-bold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-2 border border-outline-variant/30 hover:bg-surface-variant transition-all text-center"
              >
                <span className="material-symbols-outlined text-[18px]">sms</span>
                Send SMS Text
              </a>
            </div>
          </div>

          
          {/* Dedicated Hospital ER Desk Call Button */}
          <div className="bg-surface-container rounded-xl p-stack-md flex flex-col gap-2 border border-[#B084FF]/30">
            <div className="text-xs font-bold font-mono text-[#B084FF] uppercase flex items-center gap-2">
              <span className="material-symbols-outlined text-[18px]">local_hospital</span>
              Direct Hospital ER Desk Contact ({hospitalName})
            </div>
            <div className="grid grid-cols-2 gap-2 mt-1">
              <a 
                href="tel:112" 
                className="bg-[#B084FF] text-white font-bold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-2 shadow-md hover:bg-[#B084FF]/90 transition-all text-center"
              >
                <span className="material-symbols-outlined text-[18px]">call</span>
                Call Hospital ER
              </a>
              <a 
                href="sms:112?body=Emergency%20Update%20from%20Citizen" 
                className="bg-surface-container-highest text-on-surface font-bold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-2 border border-outline-variant/30 hover:bg-surface-variant transition-all text-center"
              >
                <span className="material-symbols-outlined text-[18px]">sms</span>
                SMS Hospital ER
              </a>
            </div>
          </div>

          {/* Destination info (Hospital vs Fire Scene vs Incident Site) */}
          <div className="bg-surface-container rounded-xl p-stack-md flex items-center gap-stack-md">
            <div className="w-10 h-10 bg-secondary-container rounded-xl flex items-center justify-center">
              <span className="material-symbols-outlined text-on-secondary-container" style={{ fontVariationSettings: "'FILL' 1" }}>
                {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'local_fire_department' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'local_police' : 'local_hospital'}
              </span>
            </div>
            <div>
              <div className="font-label-caps text-label-caps text-on-surface-variant">
                {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'FIRE EMERGENCY SCENE' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'POLICE INCIDENT SITE' : 'DESTINATION HOSPITAL'}
              </div>
              <div className="font-headline-md text-headline-md text-on-surface">
                {(citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Fire Engine' ? 'Fire Incident Structure, Bellary Road' : (citizenView?.vehicle_required || incidentData?.vehicle_required) === 'Police Cruiser' ? 'Incident Site, MG Road' : hospitalName}
              </div>
              {citizenView?.message && (
                <div className="font-body-md text-body-md text-on-surface-variant mt-1">{citizenView.message}</div>
              )}
            </div>
          </div>

          {/* Action buttons */}
          <div className="grid grid-cols-2 gap-stack-md">
            <button onClick={() => window.location.href="tel:112"} className="flex flex-col items-center justify-center bg-secondary-container text-on-secondary-container h-24 rounded-xl active:scale-95 transition-transform hover:bg-secondary hover:text-on-secondary">
              <span className="material-symbols-outlined text-3xl mb-1">call</span>
              <span className="font-label-caps text-label-caps">CALL HELPLINE</span>
            </button>
            <button onClick={() => window.location.href="sms:112,+919876543210,+919988776655?body=EMERGENCY%21%20I%20need%20immediate%20assistance.%20An%20ambulance%20has%20been%20dispatched%20to%20my%20location."} className="flex flex-col items-center justify-center bg-surface-container-highest text-on-surface h-24 rounded-xl active:scale-95 transition-transform hover:bg-surface-variant">
              <span className="material-symbols-outlined text-3xl mb-1">chat</span>
              <span className="font-label-caps text-label-caps">SECURE TEXT</span>
            </button>
          </div>

          {/* Safety tips */}
          <div className="bg-surface-container rounded-xl p-stack-md">
            <h3 className="font-headline-md text-headline-md text-on-surface mb-stack-sm flex items-center gap-2">
              <span className="material-symbols-outlined text-tertiary">check_circle</span>
              Immediate Steps
            </h3>
            <div className="space-y-stack-sm">
              <div className="flex items-center gap-stack-md p-stack-sm bg-surface-container-low rounded-lg">
                <span className="material-symbols-outlined text-on-surface-variant">visibility</span>
                <p className="font-body-md text-body-md text-on-surface-variant">Stay in a well-lit area if possible</p>
              </div>
              <div className="flex items-center gap-stack-md p-stack-sm bg-surface-container-low rounded-lg">
                <span className="material-symbols-outlined text-on-surface-variant">battery_charging_full</span>
                <p className="font-body-md text-body-md text-on-surface-variant">Keep your phone screen on</p>
              </div>
              <div className="flex items-center gap-stack-md p-stack-sm bg-surface-container-low rounded-lg">
                <span className="material-symbols-outlined text-on-surface-variant">door_open</span>
                <p className="font-body-md text-body-md text-on-surface-variant">Unlock access for emergency crew</p>
              </div>
            </div>
          </div>

          <div className="flex flex-col items-center py-stack-lg gap-stack-sm">
            <p className="font-body-md text-body-md text-on-surface-variant text-center px-8">
              Emergency services have been notified of your location and status.
            </p>
            <button
              onClick={() => { setAppState('home'); setPollUrl(null); setIncidentData(null); setCitizenView(null); }}
              className="text-error font-label-caps text-label-caps underline underline-offset-4 decoration-error/30 active:text-error/70 transition-colors uppercase"
            >
              Cancel Assistance Request
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

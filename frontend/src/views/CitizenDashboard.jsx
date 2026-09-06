import LiveEmergencyChat from '../components/LiveEmergencyChat';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';
import { Heart, Activity, Shield, AlertTriangle, CheckCircle, Navigation, MapPin, Plus, LogOut } from 'lucide-react';

const mapContainerStyle = { width: '100%', height: '100%', zIndex: 0 };
const LOADER_STATUSES = [
  { main: "Establishing Secure Connection...", sub: "SIGNAL STRENGTH: EXCELLENT", step2: "Verifying GPS Location..." },
  { main: "Triangulating Emergency Coordinates...", sub: "ACCURACY: 3 METERS", step2: "Syncing User Profile..." },
  { main: "Relaying Incident Telemetry...", sub: "PRIORITY: IMMEDIATE", step2: "Alerting Nearest Station Hub..." },
  { main: "Awaiting Dispatcher Confirmation...", sub: "CONNECTING TO COMMAND CENTER", step2: "Finalizing Route Assignment..." }
];

export default function CitizenDashboard() {
  const { citizenInfo, logout } = useAuth();
  const navigate = useNavigate();
  const handleLogout = () => { logout(); navigate('/', { replace: true }); };
  const isLoaded = true;

  const [appState, setAppState] = useState('home');
  const [details, setDetails] = useState('');
  const [selectedVehicle, setSelectedVehicle] = useState('Ambulance');
  const [includeAmbulanceBackup, setIncludeAmbulanceBackup] = useState(false);
  const [locationStr, setLocationStr] = useState('Fetching location...');
  const [locationCoords, setLocationCoords] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const [pollUrl, setPollUrl] = useState(null);
  const [citizenView, setCitizenView] = useState(null);
  const [incidentData, setIncidentData] = useState(null);
  const [allCitizenIncidents, setAllCitizenIncidents] = useState([]);

  useEffect(() => {
    const fetchAllIncidents = async () => {
      try {
        const res = await fetch('/api/incidents/');
        if (!res.ok) return;
        const data = await res.json();
        const incs = data.incidents || [];
        
        const myIncidents = incs.filter(i => {
          if (!citizenInfo?.phone) return false;
          return i.citizen_phone && i.citizen_phone.trim() === citizenInfo.phone.trim();
        });

        setAllCitizenIncidents(myIncidents);

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

  const [loaderIndex, setLoaderIndex] = useState(0);
  const loaderStatus = LOADER_STATUSES[loaderIndex % LOADER_STATUSES.length];

  useEffect(() => {
    if (appState !== 'loading') return;
    const id = setInterval(() => setLoaderIndex(i => i + 1), 3500);
    return () => clearInterval(id);
  }, [appState]);

  useEffect(() => {
    if (appState !== 'loading' || !pollUrl) return;

    const poll = async () => {
      try {
        const res = await fetch(pollUrl);
        if (!res.ok) return;
        const data = await res.json();

        if (
          data.status === 'awaiting_dispatcher_approval' ||
          data.status === 'dispatched' ||
          data.status === 'completed'
        ) {
          setIncidentData(data);
          setCitizenView(data.citizen_view || null);
          setAppState('tracking');
        }
      } catch (err) {}
    };

    poll();
    const id = setInterval(poll, 2000);
    return () => clearInterval(id);
  }, [appState, pollUrl]);

  const handleUseLocation = () => {
    if (window.navigator?.vibrate) window.navigator.vibrate(100);
    if (!navigator.geolocation) {
      setLocationStr('GPS not supported');
      setLocationCoords({ lat: 12.9756, lng: 77.6068 });
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
        setLocationCoords({ lat: 12.9756, lng: 77.6068 });
        setLocationStr('12.9756°N, 77.6068°E (Default)');
        setAppState('sos');
      }
    );
  };

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

    try {
      const res = await fetch('/api/incidents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (res.status === 202 || res.ok) {
        setPollUrl(data.poll_url);
      } else {
        setErrorMsg('Backend error: ' + (data.detail || res.status));
        setAppState('sos');
      }
    } catch (err) {
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

  const TopHeader = ({ title, onBack }) => (
    <header className="fixed top-0 inset-x-0 z-50 bg-white/95 backdrop-blur-md border-b border-[#dcd3e3] shadow-elevation-sm">
      <div className="h-16 px-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {onBack && (
            <button
              onClick={onBack}
              className="w-10 h-10 flex items-center justify-center text-[#012622] bg-[#ece5f0] hover:bg-[#012622] hover:text-white rounded-full transition-all border border-[#dcd3e3]"
            >
              <span className="font-bold text-base">&larr;</span>
            </button>
          )}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-[#012622] text-[#e98a15] flex items-center justify-center">
              <Heart size={18} className="fill-current" />
            </div>
            <h1 className="font-display font-bold text-lg text-[#012622]">{title}</h1>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {allCitizenIncidents.length > 0 && (
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
              className="bg-[#ece5f0] border border-[#dcd3e3] text-[#012622] text-xs font-mono font-bold px-3 py-1.5 rounded-full focus:outline-none focus:border-[#012622]"
            >
              <option value="new">+ New SOS Emergency</option>
              {allCitizenIncidents.map(inc => (
                <option key={inc.incident_id} value={inc.incident_id}>
                  Track {inc.incident_id} ({inc.emergency_type || 'Emergency'})
                </option>
              ))}
            </select>
          )}

          <div className="hidden sm:flex items-center gap-2 bg-[#fdf3e7] border border-[#e98a15]/40 px-3 py-1 rounded-full text-xs font-mono text-[#012622] font-bold">
            <Shield size={14} className="text-[#e98a15]" />
            <span>{citizenInfo?.name || "Ananya Sharma"}</span>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#012622] hover:bg-[#003b36] text-white transition-all text-xs font-semibold shadow-sm"
            title="Sign Out of Citizen App"
          >
            <LogOut size={14} />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </header>
  );

  if (appState === 'home') return (
    <div className="bg-[#ece5f0] font-body text-[#012622] flex flex-col min-h-screen">
      <TopHeader title="Citizen Portal" />
      <main className="flex-1 flex flex-col relative w-full pt-20 pb-20 max-w-4xl mx-auto px-6">
        <div className="flex justify-between items-center my-4">
          <div className="bg-white rounded-full px-4 py-2 flex items-center gap-2.5 shadow-elevation-sm border border-[#dcd3e3]">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#e98a15] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#e98a15]"></span>
            </span>
            <span className="font-mono text-xs font-bold text-[#012622] uppercase tracking-wider">NETWORK STATUS: OPERATIONAL</span>
          </div>
          <button 
            onClick={handleUseLocation}
            className="w-11 h-11 bg-white border border-[#dcd3e3] text-[#012622] rounded-full flex items-center justify-center shadow-elevation-sm hover:shadow-elevation-md active:scale-95 transition-all"
            title="Recenter Location"
          >
            <Navigation size={18} className="text-[#e98a15]" />
          </button>
        </div>

        <div className="my-auto py-8 text-center space-y-4">
          <div className="w-20 h-20 rounded-3xl bg-[#012622] text-[#e98a15] flex items-center justify-center mx-auto shadow-elevation-md">
            <Heart size={40} className="fill-current" />
          </div>
          <h2 className="font-display text-3xl font-extrabold text-[#012622]">Emergency Assistance</h2>
          <p className="text-sm text-[#003b36] max-w-md mx-auto leading-relaxed">
            One-tap incident dispatch with real-time GPS tracking and direct paramedic communication.
          </p>
        </div>

        <div className="bg-white rounded-3xl p-6 shadow-elevation-md border border-[#dcd3e3] space-y-4">
          <button
            onClick={handleUseLocation}
            className="w-full h-14 bg-[#012622] hover:bg-[#003b36] text-white font-bold rounded-2xl flex items-center justify-center gap-3 shadow-elevation-md hover:shadow-amber-glow active:scale-95 transition-all text-base"
          >
            <MapPin size={20} className="text-[#e98a15]" />
            <span>Use Current GPS Location</span>
          </button>
          <button
            onClick={() => { setLocationCoords({ lat: 12.9756, lng: 77.6068 }); setLocationStr('MG Road, Bengaluru'); setAppState('sos'); }}
            className="w-full h-14 bg-[#ece5f0] hover:bg-[#dcd3e3] text-[#012622] font-bold rounded-2xl flex items-center justify-center gap-3 transition-all active:scale-[0.98] border border-[#dcd3e3]"
          >
            <Navigation size={20} className="text-[#e98a15]" />
            <span>Select Destination on Map</span>
          </button>
        </div>
      </main>
    </div>
  );

  if (appState === 'sos') return (
    <div className="bg-[#ece5f0] font-body text-[#012622] flex flex-col min-h-screen">
      <TopHeader title="Trigger Emergency SOS" onBack={() => setAppState('home')} />
      <main className="flex-1 flex flex-col w-full pt-20 pb-16 max-w-3xl mx-auto px-6 space-y-5">
        <div className="flex items-center justify-between bg-white p-4 rounded-2xl border border-[#dcd3e3] shadow-elevation-sm">
          <div className="flex items-center gap-3">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#e98a15] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-[#e98a15]"></span>
            </span>
            <span className="font-mono text-xs font-bold text-[#012622] uppercase tracking-wider">Live GPS Active</span>
          </div>
          <span className="font-mono text-xs font-bold text-[#e98a15]">{locationStr}</span>
        </div>

        {errorMsg && (
          <div className="bg-red-50 text-red-700 p-4 rounded-2xl flex items-center gap-3 border border-red-200 text-xs font-bold">
            <AlertTriangle size={18} />
            <span>{errorMsg}</span>
          </div>
        )}

        <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-md space-y-4">
          <h2 className="font-display text-lg font-bold text-[#012622]">Describe Emergency Details</h2>

          <textarea
            value={details}
            onChange={(e) => setDetails(e.target.value)}
            className="w-full h-32 bg-[#ece5f0] text-[#012622] p-4 rounded-2xl border border-[#dcd3e3] focus:outline-none focus:border-[#012622] transition-all text-sm resize-none placeholder:text-[#003b36]/60"
            placeholder="e.g., 'chest pain', 'fire on 3rd floor', 'road accident'..."
          />

          <div className="flex flex-wrap gap-2">
            {['Medical Help', 'Fire/Smoke', 'Police/Security', 'Accident', 'Breathing Difficulty'].map(chip => (
              <button
                key={chip}
                onClick={() => addDetail(chip)}
                className="bg-[#fdf3e7] hover:bg-[#012622] hover:text-[#e98a15] px-3.5 py-1.5 rounded-full font-mono text-xs text-[#012622] font-bold transition-all border border-[#e98a15]/30"
              >
                + {chip.toUpperCase()}
              </button>
            ))}
          </div>

          <div className="space-y-2 pt-2">
            <span className="text-xs font-mono font-bold text-[#012622] uppercase block">Select Required Emergency Service</span>
            <div className="grid grid-cols-2 gap-3">
              {[
                { id: 'Ambulance', label: 'Medical Ambulance' },
                { id: 'Fire Engine', label: 'Fire Engine Rescue' },
                { id: 'Police Cruiser', label: 'Police Patrol Unit' },
                { id: 'Disaster Rescue', label: 'Disaster Search & Rescue' },
              ].map(v => (
                <button
                  key={v.id}
                  type="button"
                  onClick={() => setSelectedVehicle(v.id)}
                  className={`p-3.5 rounded-2xl border text-xs font-bold font-mono transition-all flex items-center justify-between ${
                    selectedVehicle === v.id
                      ? 'border-[#012622] bg-[#012622] text-[#e98a15] shadow-sm'
                      : 'border-[#dcd3e3] bg-[#ece5f0] text-[#003b36] hover:bg-[#dcd3e3]'
                  }`}
                >
                  <span>{v.label}</span>
                  {selectedVehicle === v.id && <CheckCircle size={16} className="text-[#e98a15]" />}
                </button>
              ))}
            </div>
          </div>

          {selectedVehicle !== 'Ambulance' && (
            <label className="flex items-center gap-3 p-3 bg-[#ece5f0] rounded-2xl border border-[#dcd3e3] cursor-pointer text-xs font-bold text-[#012622]">
              <input
                type="checkbox"
                checked={includeAmbulanceBackup}
                onChange={(e) => setIncludeAmbulanceBackup(e.target.checked)}
                className="w-4 h-4 rounded text-[#012622] focus:ring-[#012622] accent-[#012622]"
              />
              <span>Request Paramedic Ambulance Standby Backup Unit</span>
            </label>
          )}

          <button
            onClick={handleSOSTrigger}
            className="w-full py-4 bg-[#012622] hover:bg-[#003b36] text-white font-extrabold font-display rounded-2xl shadow-elevation-md hover:shadow-amber-glow active:scale-95 transition-all text-lg tracking-wider"
          >
            DISPATCH EMERGENCY ASSISTANCE NOW
          </button>
        </div>
      </main>
    </div>
  );

  if (appState === 'loading') return (
    <div className="bg-[#ece5f0] font-body text-[#012622] flex flex-col min-h-screen">
      <TopHeader title="Processing Emergency Request" />
      <main className="flex-1 flex flex-col w-full pt-20 max-w-xl mx-auto px-6 text-center space-y-6">
        <div className="bg-white p-8 rounded-3xl border border-[#dcd3e3] shadow-elevation-md space-y-6">
          <div className="relative w-28 h-28 mx-auto flex items-center justify-center">
            <div className="absolute inset-0 rounded-full bg-[#012622]/10 animate-ping"></div>
            <div className="w-20 h-20 rounded-full bg-[#012622] text-[#e98a15] border border-[#012622] flex items-center justify-center shadow-inner">
              <Activity size={36} className="animate-pulse" />
            </div>
          </div>

          <div className="space-y-2">
            <h2 className="font-display text-xl font-bold text-[#012622]">{loaderStatus.main}</h2>
            <p className="font-mono text-xs font-bold text-[#e98a15] uppercase tracking-wider">{loaderStatus.sub}</p>
          </div>

          <div className="p-4 rounded-2xl bg-[#ece5f0] border border-[#dcd3e3] text-xs text-[#003b36] font-mono">
            {loaderStatus.step2}
          </div>
        </div>
      </main>
    </div>
  );

  const hospitalName = citizenView?.hospital_name
    || incidentData?.action_plan?.recommended_hospital?.name
    || 'Nearest Hospital';
  const etaMinutes = citizenView?.eta_minutes ?? 8;
  const emergencyType = citizenView?.emergency_type || incidentData?.emergency_type || 'Emergency';
  const origin = citizenView?.origin || locationCoords || { lat: 12.9756, lng: 77.6068 };
  const hospLoc = citizenView?.hospital_location;
  const routeCoords = citizenView?.route_coordinates || [];
  const mapCenter = hospLoc || origin;

  return (
    <div className="bg-[#ece5f0] font-body text-[#012622] flex flex-col min-h-screen">
      <TopHeader title="Live Incident Traversal" />
      <main className="flex-1 flex flex-col w-full pt-16 pb-16 max-w-4xl mx-auto px-6 space-y-4">
        <div className="relative w-full h-[36vh] rounded-3xl overflow-hidden bg-white border border-[#dcd3e3] shadow-elevation-md flex-shrink-0 mt-4">
          {isLoaded && hospLoc ? (
            <MapContainer center={[mapCenter.lat, mapCenter.lng]} zoom={13} style={mapContainerStyle} zoomControl={false} attributionControl={false}>
              <TileLayer url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png" />
              <Marker position={[origin.lat, origin.lng]} />
              <Marker position={[hospLoc.lat, hospLoc.lng]} />
              {citizenView?.phase1_hub && (
                <Marker position={[citizenView.phase1_hub.lat, citizenView.phase1_hub.lng]} />
              )}
              {citizenView?.phase1_route_coordinates && citizenView.phase1_route_coordinates.length > 0 && (
                <Polyline 
                  positions={citizenView.phase1_route_coordinates.map(c => [c.lat, c.lng])} 
                  pathOptions={{ color: '#e98a15', weight: 4, opacity: 0.9, dashArray: '8, 8' }} 
                />
              )}
              {routeCoords.length > 0 && (
                <Polyline 
                  positions={routeCoords.map(c => [c.lat, c.lng])} 
                  pathOptions={{ color: '#012622', weight: 5, opacity: 0.9 }} 
                />
              )}
            </MapContainer>
          ) : (
            <div className="absolute inset-0 flex items-center justify-center bg-[#ece5f0]">
              <Activity size={32} className="text-[#012622] animate-spin" />
            </div>
          )}

          <div className="absolute top-4 right-4 bg-white/95 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-sm z-10 border border-[#dcd3e3]">
            <span className="w-2.5 h-2.5 bg-[#e98a15] rounded-full animate-pulse"></span>
            <span className="font-mono text-xs font-bold text-[#012622]">LIVE 2-PHASE ROUTE</span>
          </div>

          <div className="absolute bottom-4 left-4 bg-white/95 backdrop-blur-md px-3.5 py-2 rounded-full flex items-center gap-2 shadow-sm z-10 border border-[#dcd3e3] text-xs font-bold font-mono">
            <span className="text-[#012622]">Destination:</span>
            <span className="text-[#e98a15] font-bold">{hospitalName}</span>
          </div>
        </div>

        <div className="bg-white rounded-3xl p-6 shadow-elevation-md border border-[#dcd3e3] space-y-4">
          <div className="flex justify-between items-center border-b border-[#dcd3e3] pb-4">
            <div>
              <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-full bg-[#012622] text-[#e98a15] uppercase border border-[#012622]">
                {emergencyType}
              </span>
              <h2 className="font-display font-extrabold text-xl text-[#012622] mt-2">
                Responder Unit En Route
              </h2>
            </div>
            <div className="text-right">
              <div className="font-display font-extrabold text-3xl text-[#012622]">
                {incidentData?.status === 'completed' ? '0m' : `${etaMinutes}m`}
              </div>
              <span className="text-[10px] font-mono uppercase text-[#003b36] font-bold">Estimated Arrival</span>
            </div>
          </div>

          {(!citizenView?.include_ambulance_backup && !incidentData?.include_ambulance_backup) && (
            <div className="bg-[#ece5f0] p-4 rounded-2xl border border-[#dcd3e3] flex items-center justify-between">
              <div className="text-xs font-bold text-[#012622]">Need Medical Standby Backup?</div>
              <button
                onClick={async () => {
                  if (!incidentData?.incident_id) return;
                  try {
                    await fetch(`/api/incidents/${incidentData.incident_id}/request_ambulance`, { method: 'POST' });
                    setIncidentData(prev => ({ ...prev, include_ambulance_backup: true }));
                    setCitizenView(prev => ({ ...prev, include_ambulance_backup: true }));
                  } catch (err) {}
                }}
                className="px-3.5 py-2 bg-[#012622] text-[#e98a15] rounded-xl text-xs font-mono font-bold shadow-sm hover:bg-[#003b36] transition-all flex items-center gap-1.5"
              >
                <Plus size={14} />
                <span>DISPATCH AMBULANCE BACKUP</span>
              </button>
            </div>
          )}

          <div className="pt-2">
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
        </div>
      </main>
    </div>
  );
}

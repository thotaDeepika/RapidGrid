import LiveEmergencyChat from '../components/LiveEmergencyChat';
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Truck, Navigation, Phone, MessageSquare, Clock, MapPin, CheckCircle2, AlertTriangle, ArrowRight, ShieldAlert } from 'lucide-react';
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function DriverDashboard() {
  const { user } = useAuth();
  const driverData = user?.role === 'driver' ? user.extraData : null;

  const [activeDispatches, setActiveDispatches] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [isNavigating, setIsNavigating] = useState(false);
  const [driverVehicleFilter, setDriverVehicleFilter] = useState('All');
  const [driverStage, setDriverStage] = useState('pickup'); // 'pickup' | 'hospital'

  useEffect(() => {
    if (driverData?.vehicleType) {
      setDriverVehicleFilter(driverData.vehicleType);
    }
  }, [driverData?.vehicleType]);

  // Poll for active dispatches
  useEffect(() => {
    const fetchDispatches = async () => {
      try {
        const res = await fetch('/api/driver/active');
        if (!res.ok) return;
        const data = await res.json();
        const list = data.dispatches || [];
        setActiveDispatches(list);

        // Keep navigating incident updated
        if (selectedIncident && isNavigating) {
          const updated = list.find(i => i.incident_id === selectedIncident.incident_id);
          if (updated) setSelectedIncident(updated);
        }
      } catch (err) {
        console.error('Error fetching driver dispatches:', err);
      }
    };

    fetchDispatches();
    const interval = setInterval(fetchDispatches, 2500);
    return () => clearInterval(interval);
  }, [selectedIncident, isNavigating]);

  // Handle Mark as Arrived
  const handleArrived = async () => {
    if (!selectedIncident) return;
    try {
      await fetch(`/api/incidents/${selectedIncident.incident_id}/arrived`, {
        method: 'POST'
      });
      setIsNavigating(false);
      setSelectedIncident(null);
    } catch (err) {
      console.error('Error marking arrived:', err);
    }
  };

  // VIEW 1: ACTIVE DISPATCH SELECTION QUEUE (Driver picks one to start)
  if (!isNavigating) {
    return (
      <div className="flex flex-col h-[calc(100vh-80px)] p-4 bg-surface text-on-surface gap-4 overflow-y-auto">
        <div className="bg-surface-container-high p-4 rounded-xl border border-outline-variant/30 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-secondary/20 text-secondary rounded-xl">
              <Truck size={24} />
            </div>
            <div>
              <h1 className="font-headline-md text-headline-md text-on-surface">Ambulance Paramedic Unit</h1>
              <p className="text-xs text-on-surface-variant">Active Emergency Dispatch Queue</p>
            </div>
          </div>
          <div className="px-3 py-1.5 bg-tertiary/20 text-tertiary rounded-full font-mono text-xs flex items-center gap-2">
            <span className="w-2 h-2 bg-tertiary rounded-full animate-pulse"></span>
            PARAMEDIC FIELD STATUS: READY
          </div>
        </div>

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
              <span>{v === 'All' ? 'All Emergency Units' : v}</span>
            </button>
          ))}
        </div>

        <div className="space-y-3">
          <h2 className="text-sm font-bold text-on-surface-variant uppercase tracking-wider">
            Available Emergency Calls ({activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter || (driverVehicleFilter === 'Ambulance' && i.include_ambulance_backup)).length})
          </h2>

          {activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter || (driverVehicleFilter === 'Ambulance' && i.include_ambulance_backup)).length === 0 ? (
            <div className="bg-surface-container p-8 rounded-xl text-center border border-outline-variant/20 space-y-2">
              <ShieldAlert size={36} className="mx-auto text-on-surface-variant opacity-40" />
              <div className="font-semibold text-on-surface">No Active Dispatches for {driverVehicleFilter}</div>
              <p className="text-xs text-on-surface-variant">No pending emergency dispatches for this unit type at the moment.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter || (driverVehicleFilter === 'Ambulance' && i.include_ambulance_backup)).map((inc) => (
                <div 
                  key={inc.incident_id}
                  className="bg-surface-container p-5 rounded-2xl border border-outline-variant/30 hover:border-primary transition-all space-y-4 flex flex-col justify-between"
                >
                  <div className="space-y-2">
                    <div className="flex justify-between items-start">
                      <span className="bg-primary/20 text-primary font-mono font-bold text-xs px-2.5 py-1 rounded-lg">
                        {inc.incident_id}
                      </span>
                      <span className="bg-tertiary/20 text-tertiary font-mono text-xs px-2.5 py-1 rounded-lg font-bold uppercase">
                        REQ: {inc.vehicle_required || 'Ambulance'}
                      </span>
                    </div>

                    <div className="text-sm font-bold text-on-surface">
                      Hospital Destination: {inc.hospital_name}
                    </div>

                    <p className="text-xs text-on-surface-variant italic bg-surface-container-low p-2.5 rounded-lg">
                      "{inc.details}"
                    </p>

                    <div className="flex justify-between text-xs font-mono text-on-surface-variant pt-2 border-t border-outline-variant/20">
                      <span>Citizen: {inc.citizen_name || 'Patient'}</span>
                      <span>ETA: {inc.eta_minutes} mins</span>
                    </div>
                  </div>

                  <button
                    onClick={() => {
                      setSelectedIncident(inc);
                      setIsNavigating(true);
                    }}
                    className="w-full bg-primary text-on-primary font-bold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-primary/90 transition-all text-sm shadow-md"
                  >
                    ACCEPT & LEAVE FOR DISPATCH <ArrowRight size={18} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

  // VIEW 2: LIVE TURN-BY-TURN NAVIGATION SCREEN (After selecting an emergency)
  const origin = selectedIncident?.citizen_view?.origin || selectedIncident?.origin || { lat: 12.9756, lng: 77.6068 };
  const hospLoc = selectedIncident?.citizen_view?.hospital_location || selectedIncident?.hospital_location || { lat: 13.0473, lng: 77.5908 };

  const rawCoords = (driverStage === 'pickup' ? selectedIncident?.citizen_view?.phase1_route_coordinates : null)
    || selectedIncident?.route_coordinates 
    || selectedIncident?.citizen_view?.route_coordinates;

  const routeCoords = (rawCoords && rawCoords.length > 0)
    ? rawCoords
    : [origin, hospLoc];

  const etaMinutes = selectedIncident?.citizen_view?.eta_minutes || selectedIncident?.eta_minutes || 7;
  const distanceKm = selectedIncident?.citizen_view?.distance_meters ? (selectedIncident.citizen_view.distance_meters / 1000).toFixed(1) : selectedIncident?.distance_meters ? (selectedIncident.distance_meters / 1000).toFixed(1) : '2.4';

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] p-4 bg-surface text-on-surface gap-4 overflow-y-auto">
      {/* Top Section: Map & Hospital/Patient Panel */}
      <div className="flex flex-col md:flex-row gap-4 min-h-[420px]">
        {/* Left: Tactical Map & Navigation */}
        <div className="flex-1 flex flex-col gap-4 overflow-hidden">
          <div className="bg-surface-container-high p-4 rounded-xl border border-primary/30 flex justify-between items-center shadow-lg">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-primary/20 text-primary rounded-xl animate-pulse">
                <Navigation size={24} />
              </div>
              <div>
                <span className="text-xs font-label-caps text-primary uppercase font-bold tracking-wider">
                  {driverStage === 'pickup' ? 'STAGE 1: EN ROUTE TO PATIENT PICKUP SPOT' : 'STAGE 2: PATIENT PICKED UP - EN ROUTE TO HOSPITAL'}
                </span>
                <h2 className="font-mono text-xl font-bold text-on-surface">{selectedIncident.incident_id}</h2>
              </div>
            </div>

            <div className="text-right">
              <div className="font-mono text-3xl font-black text-primary leading-none">{etaMinutes}m</div>
              <span className="text-[10px] font-label-caps text-on-surface-variant uppercase">ESTIMATED ARRIVAL</span>
            </div>
          </div>

          <div className="relative flex-1 min-h-[280px] rounded-xl overflow-hidden border border-outline-variant/30">
            <MapContainer center={[origin.lat, origin.lng]} zoom={13} style={{ height: '100%', width: '100%' }} zoomControl={false} attributionControl={false}>
              <TileLayer url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png" />
              {/* Patient Pickup Marker */}
              <Marker position={[origin.lat, origin.lng]} />
              {/* Destination Hospital Marker */}
              <Marker position={[hospLoc.lat, hospLoc.lng]} />
              {/* Base Station Hub Marker if available */}
              {selectedIncident?.citizen_view?.phase1_hub && (
                <Marker position={[selectedIncident.citizen_view.phase1_hub.lat, selectedIncident.citizen_view.phase1_hub.lng]} />
              )}
              {/* Phase 1 Route: Station Hub -> Patient Pickup (Gold Dotted Line) */}
              {selectedIncident?.citizen_view?.phase1_route_coordinates && selectedIncident.citizen_view.phase1_route_coordinates.length > 0 && (
                <Polyline 
                  positions={selectedIncident.citizen_view.phase1_route_coordinates.map(c => [c.lat, c.lng])} 
                  pathOptions={{ color: '#FFB900', weight: 4, opacity: 0.9, dashArray: '8, 8' }} 
                />
              )}
              {/* Phase 2 Route: Patient Pickup -> Destination Hospital (Red Solid Line) */}
              {routeCoords.length > 0 && (
                <Polyline 
                  positions={routeCoords.map(c => [c.lat, c.lng])} 
                  pathOptions={{ color: '#FF5451', weight: 5, opacity: 0.9 }} 
                />
              )}
            </MapContainer>

            {/* Station Base Hub Badge Overlay */}
            {selectedIncident?.citizen_view?.phase1_hub && (
              <div className="absolute top-4 left-4 bg-surface-container-highest/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10 font-mono text-[10px] font-bold text-[#FFB900]">
                <span className="material-symbols-outlined text-[14px]">local_convenience_store</span>
                <span>BASE: {selectedIncident.citizen_view.phase1_hub.name} ({selectedIncident.citizen_view.phase1_eta_minutes || 5}m)</span>
              </div>
            )}

            <div className="absolute top-4 right-4 bg-surface-container-highest/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10 text-xs font-mono font-bold">
              <span className="w-2 h-2 bg-tertiary rounded-full animate-pulse"></span>
              LIVE TURN-BY-TURN NAV
            </div>
          </div>

          <div className="flex gap-4">
            <button 
              onClick={() => setIsNavigating(false)}
              className="px-4 py-4 bg-surface-container-highest text-on-surface rounded-xl font-semibold text-xs hover:bg-surface-variant"
            >
              Back to Queue
            </button>
            {driverStage === 'pickup' ? (
              <button
                onClick={async () => {
                  try {
                    const res = await fetch('/api/driver/arrived_pickup', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ incident_id: selectedIncident.incident_id, driver_id: 'drv-11' })
                    });
                    const data = await res.json();
                    setDriverStage('hospital');
                    if (data.citizen_view) {
                      setSelectedIncident(prev => ({ ...prev, citizen_view: data.citizen_view, route_coordinates: data.citizen_view.route_coordinates }));
                    }
                  } catch (err) {}
                }}
                className="flex-1 bg-primary text-on-primary font-bold text-lg py-4 rounded-xl flex items-center justify-center gap-2 shadow-xl hover:bg-primary/90 transition-all active:scale-[0.98]"
              >
                <CheckCircle2 size={24} /> MARK ARRIVED AT PATIENT SPOT
              </button>
            ) : (
              <button
                onClick={handleArrived}
                className="flex-1 bg-tertiary text-on-tertiary font-bold text-lg py-4 rounded-xl flex items-center justify-center gap-2 shadow-xl hover:bg-tertiary/90 transition-all active:scale-[0.98]"
              >
                <CheckCircle2 size={24} /> {selectedIncident?.vehicle_required === 'Fire Engine' ? 'MARK AS ARRIVED AT FIRE SCENE' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'MARK AS ARRIVED ON SCENE' : 'MARK ARRIVED AT DESTINATION HOSPITAL'}
              </button>
            )}
          </div>
        </div>

        {/* Right: Hospital & Patient Details Panel */}
        <div className="w-full md:w-96 flex flex-col gap-4">
          <div className="bg-surface-container p-5 rounded-2xl border border-outline-variant/20 space-y-3">
            <h3 className="font-bold text-xs uppercase text-on-surface-variant tracking-wider flex items-center gap-2">
              <MapPin size={16} className="text-secondary" /> {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Fire Emergency Target' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Police Incident Scene' : 'Destination Hospital'}
            </h3>
            
            {/* AI Optimal Hospital Card + Optional Manual Reroute */}
            <div className="space-y-2">
              <div className="bg-tertiary/10 p-3 rounded-xl border border-tertiary/30 space-y-1">
                <div className="text-[10px] font-mono text-tertiary font-bold uppercase flex items-center gap-1">
                  <span className="material-symbols-outlined text-[14px]">auto_awesome</span>
                  AI OPTIMAL ROUTE (SHORTEST, FASTEST & BEDS READY):
                </div>
                <div className="text-sm font-bold text-on-surface font-mono">
                  {selectedIncident?.vehicle_required === 'Fire Engine' ? 'Commercial Building Fire, Bellary Rd' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'Incident Site, MG Road' : (selectedIncident?.citizen_view?.hospital_name || selectedIncident.hospital_name)}
                </div>
              </div>

              <label className="text-[10px] font-mono text-on-surface-variant font-bold block uppercase pt-1">
                Manual Driver Override (Optional Reroute):
              </label>
              <select
                value={selectedIncident?.citizen_view?.hospital_name || selectedIncident.hospital_name}
                onChange={async (e) => {
                  const newHosp = e.target.value;
                  try {
                    const res = await fetch('/api/driver/change_hospital', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ incident_id: selectedIncident.incident_id, hospital_name: newHosp })
                    });
                    const data = await res.json();
                    if (data.citizen_view) {
                      setSelectedIncident(prev => ({
                        ...prev,
                        hospital_name: newHosp,
                        citizen_view: data.citizen_view,
                        route_coordinates: data.citizen_view.route_coordinates,
                        eta_minutes: data.citizen_view.eta_minutes
                      }));
                    }
                  } catch (err) {}
                }}
                className="w-full bg-surface-container-high border border-tertiary/40 text-on-surface text-xs font-mono font-bold p-2.5 rounded-xl focus:outline-none focus:border-tertiary shadow-sm"
              >
                {[
                  'Aster CMI Hospital (Hebbal)',
                  'MEDSTAR Speciality Hospital',
                  'Manipal Hospital (Hebbal)',
                  'Victoria Hospital',
                  'Fortis Hospital (Cunningham Rd)',
                  'Apollo Hospital (Seshadripuram)'
                ].map(h => (
                  <option key={h} value={h}>{h}</option>
                ))}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/20">
                <span className="text-[10px] text-on-surface-variant block uppercase">ICU Beds</span>
                <strong className="text-base text-tertiary">Available</strong>
              </div>
              <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/20">
                <span className="text-[10px] text-on-surface-variant block uppercase">Distance</span>
                <strong className="text-base text-primary">{distanceKm} km</strong>
              </div>
            </div>
            <button 
              onClick={() => window.location.href = "tel:112"}
              className="w-full bg-secondary-container text-on-secondary-container font-semibold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-secondary transition-colors text-xs"
            >
              <Phone size={16} /> Call Hospital ER Desk
            </button>
          </div>

          <div className="bg-surface-container p-5 rounded-2xl border border-outline-variant/20 space-y-3 flex-1">
            <h3 className="font-bold text-xs uppercase text-on-surface-variant tracking-wider flex items-center gap-2">
              <AlertTriangle size={16} className="text-error" /> Patient & Case Details
            </h3>
            <div className="bg-surface-container-low p-4 rounded-xl border border-outline-variant/20 space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-on-surface-variant">Emergency Type:</span>
                <strong className="text-error uppercase">{selectedIncident.emergency_type}</strong>
              </div>
              <div className="flex justify-between">
                <span className="text-on-surface-variant">Severity Level:</span>
                <strong>{Math.round(selectedIncident.severity * 100)}%</strong>
              </div>
              <div className="pt-3 border-t border-outline-variant/20 space-y-2">
                <span className="text-on-surface-variant font-bold block text-[11px] uppercase">Direct Patient Contact ({selectedIncident.citizen_name || 'Citizen'}):</span>
                <div className="grid grid-cols-2 gap-2">
                  <a 
                    href={`tel:${selectedIncident.citizen_phone || '+919876543210'}`} 
                    className="bg-primary text-on-primary font-bold py-2 px-3 rounded-xl text-xs flex items-center justify-center gap-1.5 shadow-md hover:bg-primary/90 text-center"
                  >
                    <Phone size={14} /> Call Patient
                  </a>
                  <a 
                    href={`sms:${selectedIncident.citizen_phone || '+919876543210'}?body=Ambulance%20Unit%20AMB-UNIT-04%20is%20en%20route%20to%20your%20location.`} 
                    className="bg-surface-container-highest text-on-surface font-bold py-2 px-3 rounded-xl text-xs flex items-center justify-center gap-1.5 border border-outline-variant/30 hover:bg-surface-variant text-center"
                  >
                    <MessageSquare size={14} /> SMS Patient
                  </a>
                </div>
              </div>
              <div className="pt-2 border-t border-outline-variant/20">
                <span className="text-on-surface-variant block mb-1">Citizen Raw Report:</span>
                <p className="italic text-on-surface bg-surface-container p-2.5 rounded-lg border border-outline-variant/10">
                  "{selectedIncident.details}"
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Full-Width Real-Time Emergency Socket Chat */}
      {selectedIncident?.incident_id && (
        <div className="w-full pt-2">
          <LiveEmergencyChat
            incidentId={selectedIncident.incident_id}
            senderRole="driver"
            senderName="Paramedic Unit AMB-04"
            targetPhone={selectedIncident.citizen_phone || '+919876543210'}
          />
        </div>
      )}
    </div>
  );
}

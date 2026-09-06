import LiveEmergencyChat from '../components/LiveEmergencyChat';
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Truck, Navigation, Phone, MessageSquare, MapPin, CheckCircle2, ArrowRight, ShieldAlert, Zap } from 'lucide-react';
import { MapContainer, TileLayer, Marker, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function DriverDashboard() {
  const { user } = useAuth();
  const driverData = user?.role === 'driver' ? user.extraData : null;

  const [activeDispatches, setActiveDispatches] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [isNavigating, setIsNavigating] = useState(false);
  const [driverVehicleFilter, setDriverVehicleFilter] = useState('All');
  const [driverStage, setDriverStage] = useState('pickup');

  useEffect(() => {
    if (driverData?.vehicleType) {
      setDriverVehicleFilter(driverData.vehicleType);
    }
  }, [driverData?.vehicleType]);

  useEffect(() => {
    const fetchDispatches = async () => {
      try {
        const res = await fetch('/api/driver/active');
        if (!res.ok) return;
        const data = await res.json();
        const list = data.dispatches || [];
        setActiveDispatches(list);

        if (selectedIncident && isNavigating) {
          const updated = list.find(i => i.incident_id === selectedIncident.incident_id);
          if (updated) setSelectedIncident(updated);
        }
      } catch (err) {}
    };

    fetchDispatches();
    const interval = setInterval(fetchDispatches, 2500);
    return () => clearInterval(interval);
  }, [selectedIncident, isNavigating]);

  const handleArrived = async () => {
    if (!selectedIncident) return;
    try {
      await fetch(`/api/incidents/${selectedIncident.incident_id}/arrived`, {
        method: 'POST'
      });
      setIsNavigating(false);
      setSelectedIncident(null);
    } catch (err) {}
  };

  if (!isNavigating) {
    return (
      <div className="flex flex-col min-h-[calc(100vh-80px)] p-6 bg-[#ece5f0] text-[#012622] gap-6 max-w-6xl mx-auto font-body">
        <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-md flex flex-wrap justify-between items-center gap-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-[#012622] text-[#e98a15] flex items-center justify-center shadow-sm">
              <Truck size={26} />
            </div>
            <div>
              <h1 className="font-display text-xl font-extrabold text-[#012622]">Paramedic First Responder Dispatch</h1>
              <p className="text-xs text-[#003b36]">Active Emergency Dispatch Queue & Station Hub Telemetry</p>
            </div>
          </div>
          <div className="px-4 py-2 bg-[#fdf3e7] border border-[#e98a15]/50 text-[#e98a15] rounded-full font-mono text-xs font-bold flex items-center gap-2 shadow-sm">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#e98a15] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#e98a15]"></span>
            </span>
            STATUS: STANDBY READY
          </div>
        </div>

        <div className="flex gap-2.5 overflow-x-auto pb-1">
          {['All', 'Ambulance', 'Fire Engine', 'Police Cruiser', 'Disaster Rescue'].map(v => (
            <button
              key={v}
              onClick={() => setDriverVehicleFilter(v)}
              className={`px-4 py-2.5 rounded-full text-xs font-bold font-mono transition-all flex items-center gap-2 border ${
                driverVehicleFilter === v
                  ? 'bg-[#012622] text-[#e98a15] border-[#012622] shadow-elevation-sm'
                  : 'bg-white text-[#003b36] border-[#dcd3e3] hover:border-[#012622]/40 hover:bg-[#e6f0ef]'
              }`}
            >
              {v === 'Ambulance' && <Truck size={14} />}
              {v === 'Fire Engine' && <ShieldAlert size={14} className="text-[#e98a15]" />}
              <span>{v === 'All' ? 'All Emergency Units' : v}</span>
            </button>
          ))}
        </div>

        <div className="space-y-4">
          <h2 className="text-xs font-mono font-bold text-[#003b36] uppercase tracking-wider">
            Available Dispatch Calls ({activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter || (driverVehicleFilter === 'Ambulance' && i.include_ambulance_backup)).length})
          </h2>

          {activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter || (driverVehicleFilter === 'Ambulance' && i.include_ambulance_backup)).length === 0 ? (
            <div className="bg-white p-12 rounded-3xl text-center border border-[#dcd3e3] shadow-elevation-sm space-y-3">
              <ShieldAlert size={40} className="mx-auto text-[#012622]/50" />
              <div className="font-display font-bold text-lg text-[#012622]">No Active Calls for {driverVehicleFilter}</div>
              <p className="text-xs text-[#003b36] max-w-sm mx-auto">No pending emergency dispatches for this unit type at the moment. Standing by for incident triggers.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {activeDispatches.filter(i => driverVehicleFilter === 'All' || (i.vehicle_required || 'Ambulance') === driverVehicleFilter || (driverVehicleFilter === 'Ambulance' && i.include_ambulance_backup)).map((inc) => (
                <div 
                  key={inc.incident_id}
                  className="bg-white p-6 rounded-3xl border border-[#dcd3e3] hover:border-[#012622] transition-all space-y-4 flex flex-col justify-between shadow-elevation-sm hover:shadow-elevation-md"
                >
                  <div className="space-y-3">
                    <div className="flex justify-between items-start">
                      <span className="bg-[#012622] text-[#e98a15] font-mono font-bold text-xs px-3 py-1 rounded-full border border-[#012622]">
                        {inc.incident_id}
                      </span>
                      <span className="bg-[#fdf3e7] text-[#e98a15] font-mono text-xs px-3 py-1 rounded-full font-bold uppercase border border-[#e98a15]/40">
                        REQ: {inc.vehicle_required || 'Ambulance'}
                      </span>
                    </div>

                    <div className="text-base font-bold font-display text-[#012622]">
                      Hospital ER Destination: {inc.hospital_name}
                    </div>

                    <p className="text-xs text-[#003b36] italic bg-[#ece5f0] p-3 rounded-2xl border border-[#dcd3e3]">
                      "{inc.details}"
                    </p>

                    <div className="flex justify-between text-xs font-mono text-[#003b36] pt-2 border-t border-[#dcd3e3]">
                      <span>Citizen: {inc.citizen_name || 'Patient'}</span>
                      <span className="font-bold text-[#e98a15]">ETA: {inc.eta_minutes} mins</span>
                    </div>
                  </div>

                  <button
                    onClick={() => {
                      setSelectedIncident(inc);
                      setIsNavigating(true);
                    }}
                    className="w-full bg-[#012622] hover:bg-[#003b36] text-white font-bold py-3.5 rounded-2xl flex items-center justify-center gap-2 transition-all text-xs font-mono shadow-elevation-sm active:scale-95"
                  >
                    ACCEPT & START DISPATCH NAVIGATION <ArrowRight size={16} className="text-[#e98a15]" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

  const origin = selectedIncident?.citizen_view?.origin || selectedIncident?.origin || { lat: 12.9756, lng: 77.6068 };
  const hospLoc = selectedIncident?.citizen_view?.hospital_location || selectedIncident?.hospital_location || { lat: 13.0473, lng: 77.5908 };

  const rawCoords = (driverStage === 'pickup' ? selectedIncident?.citizen_view?.phase1_route_coordinates : null)
    || selectedIncident?.route_coordinates 
    || selectedIncident?.citizen_view?.route_coordinates;

  const routeCoords = (rawCoords && rawCoords.length > 0)
    ? rawCoords
    : [origin, hospLoc];

  const etaMinutes = selectedIncident?.citizen_view?.eta_minutes || selectedIncident?.eta_minutes || 7;

  return (
    <div className="flex flex-col min-h-[calc(100vh-80px)] p-6 bg-[#ece5f0] text-[#012622] gap-6 max-w-7xl mx-auto font-body">
      <div className="flex flex-col lg:flex-row gap-6">
        <div className="flex-1 flex flex-col gap-4">
          <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-md flex justify-between items-center">
            <div className="flex items-center gap-3.5">
              <div className="w-12 h-12 rounded-2xl bg-[#012622] text-[#e98a15] flex items-center justify-center shadow-md">
                <Navigation size={24} />
              </div>
              <div>
                <span className="text-[11px] font-mono font-bold text-[#e98a15] uppercase tracking-wider block">
                  {driverStage === 'pickup' ? 'STAGE 1: EN ROUTE TO PATIENT PICKUP SPOT' : 'STAGE 2: PATIENT PICKED UP — EN ROUTE TO ER'}
                </span>
                <h2 className="font-display text-lg font-bold text-[#012622]">{selectedIncident.incident_id}</h2>
              </div>
            </div>

            <div className="text-right">
              <div className="font-display font-extrabold text-3xl text-[#012622]">{etaMinutes}m</div>
              <span className="text-[10px] font-mono uppercase text-[#003b36] font-bold">ETA Arrival</span>
            </div>
          </div>

          <div className="relative h-[380px] rounded-3xl overflow-hidden border border-[#dcd3e3] shadow-elevation-md bg-white">
            <MapContainer center={[origin.lat, origin.lng]} zoom={13} style={{ height: '100%', width: '100%' }} zoomControl={false} attributionControl={false}>
              <TileLayer url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png" />
              <Marker position={[origin.lat, origin.lng]} />
              <Marker position={[hospLoc.lat, hospLoc.lng]} />
              {selectedIncident?.citizen_view?.phase1_hub && (
                <Marker position={[selectedIncident.citizen_view.phase1_hub.lat, selectedIncident.citizen_view.phase1_hub.lng]} />
              )}
              {selectedIncident?.citizen_view?.phase1_route_coordinates && selectedIncident.citizen_view.phase1_route_coordinates.length > 0 && (
                <Polyline 
                  positions={selectedIncident.citizen_view.phase1_route_coordinates.map(c => [c.lat, c.lng])} 
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

            <div className="absolute top-4 right-4 bg-white/95 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-sm z-10 border border-[#dcd3e3] text-xs font-mono font-bold">
              <span className="w-2.5 h-2.5 bg-[#e98a15] rounded-full animate-pulse"></span>
              <span>LIVE TURN-BY-TURN NAV</span>
            </div>
          </div>

          <div className="flex gap-3">
            <button 
              onClick={() => setIsNavigating(false)}
              className="px-5 py-3.5 bg-[#ece5f0] hover:bg-[#dcd3e3] text-[#012622] rounded-2xl font-bold text-xs transition-all border border-[#dcd3e3]"
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
                className="flex-1 bg-[#012622] hover:bg-[#003b36] text-white font-bold text-sm py-3.5 rounded-2xl flex items-center justify-center gap-2 shadow-elevation-md transition-all active:scale-[0.98]"
              >
                <CheckCircle2 size={20} className="text-[#e98a15]" /> MARK ARRIVED AT PATIENT SPOT
              </button>
            ) : (
              <button
                onClick={handleArrived}
                className="flex-1 bg-[#012622] hover:bg-black text-white font-bold text-sm py-3.5 rounded-2xl flex items-center justify-center gap-2 shadow-elevation-md transition-all active:scale-[0.98]"
              >
                <CheckCircle2 size={20} className="text-[#e98a15]" /> {selectedIncident?.vehicle_required === 'Fire Engine' ? 'MARK ARRIVED AT FIRE SCENE' : selectedIncident?.vehicle_required === 'Police Cruiser' ? 'MARK ARRIVED ON SCENE' : 'MARK ARRIVED AT DESTINATION HOSPITAL'}
              </button>
            )}
          </div>
        </div>

        <div className="w-full lg:w-96 flex flex-col gap-5">
          <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-md space-y-4">
            <h3 className="font-display font-bold text-xs uppercase text-[#003b36] tracking-wider flex items-center gap-2">
              <MapPin size={16} className="text-[#012622]" /> Destination Hospital Controls
            </h3>
            
            <div className="space-y-2">
              <div className="bg-[#fdf3e7] p-3.5 rounded-2xl border border-[#e98a15]/30 space-y-1">
                <div className="text-[10px] font-mono text-[#e98a15] font-bold uppercase flex items-center gap-1">
                  <Zap size={12} className="text-[#e98a15]" /> AI OPTIMAL HOSPITAL ASSIGNED:
                </div>
                <div className="text-xs font-bold text-[#012622] font-mono">
                  {selectedIncident?.citizen_view?.hospital_name || selectedIncident.hospital_name}
                </div>
              </div>

              <label className="text-[10px] font-mono text-[#003b36] font-bold block uppercase pt-1">
                Uber-Style Driver Hospital Reroute:
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
                className="w-full bg-[#ece5f0] border border-[#dcd3e3] text-[#012622] text-xs font-mono font-bold p-3 rounded-2xl focus:outline-none focus:border-[#012622] shadow-sm"
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
            
            <button 
              onClick={() => window.location.href = "tel:112"}
              className="w-full bg-[#012622] hover:bg-[#003b36] text-white font-bold py-3 rounded-2xl flex items-center justify-center gap-2 transition-all text-xs"
            >
              <Phone size={15} className="text-[#e98a15]" /> Call Hospital ER Desk
            </button>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-md space-y-3">
            <h3 className="font-display font-bold text-xs uppercase text-[#003b36] tracking-wider flex items-center gap-2">
              <ShieldAlert size={16} className="text-[#012622]" /> Patient & Case Summary
            </h3>
            <div className="bg-[#ece5f0] p-4 rounded-2xl border border-[#dcd3e3] space-y-3 text-xs">
              <div className="flex justify-between">
                <span className="text-[#003b36]">Emergency Type:</span>
                <strong className="text-[#012622] uppercase">{selectedIncident.emergency_type}</strong>
              </div>
              <div className="flex justify-between">
                <span className="text-[#003b36]">Severity Level:</span>
                <strong className="text-[#e98a15]">{Math.round(selectedIncident.severity * 100)}%</strong>
              </div>
              <div className="pt-2 border-t border-[#dcd3e3]">
                <span className="text-[#003b36] block mb-1">Citizen Raw Report:</span>
                <p className="italic text-[#012622] bg-white p-3 rounded-xl border border-[#dcd3e3]">
                  "{selectedIncident.details}"
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

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

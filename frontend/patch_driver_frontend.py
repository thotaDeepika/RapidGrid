import sys

driver_jsx = "src/views/DriverDashboard.jsx"

new_driver_jsx = """import React, { useState, useEffect } from 'react';
import { Truck, Navigation, Phone, Clock, MapPin, CheckCircle2, AlertTriangle, ArrowRight, ShieldAlert } from 'lucide-react';
import MapOverlay from '../components/MapOverlay';

export default function DriverDashboard() {
  const [activeDispatches, setActiveDispatches] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [isNavigating, setIsNavigating] = useState(false);

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
              <p className="text-xs text-on-surface-variant">Unit ID: AMB-IND-04 - Active Field Operator</p>
            </div>
          </div>
          <div className="badge bg-tertiary/20 text-tertiary px-3 py-1 rounded-full text-xs font-bold uppercase">
            STATUS: STANDBY / READY
          </div>
        </div>

        <div className="flex flex-col gap-3">
          <h2 className="font-bold text-sm uppercase text-on-surface-variant tracking-wider flex items-center gap-2">
            <ShieldAlert size={18} className="text-error" /> Active Dispatched Emergencies ({activeDispatches.length})
          </h2>

          {activeDispatches.length === 0 ? (
            <div className="bg-surface-container rounded-xl p-12 text-center border border-outline-variant/20 flex flex-col items-center gap-3">
              <Truck size={48} className="text-on-surface-variant/40" />
              <p className="font-semibold text-sm text-on-surface-variant">No active dispatched emergencies.</p>
              <p className="text-xs text-on-surface-variant/60">Raise an emergency on Citizen App or Approve one on Dispatcher Admin Dashboard.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {activeDispatches.map(inc => {
                const distanceKm = inc.distance_meters ? (inc.distance_meters / 1000).toFixed(1) : '2.4';
                return (
                  <div 
                    key={inc.incident_id}
                    className="bg-surface-container p-5 rounded-2xl border border-outline-variant/30 flex flex-col justify-between gap-4 hover:border-primary/50 transition-all shadow-lg"
                  >
                    <div>
                      <div className="flex justify-between items-center mb-3">
                        <span className="font-mono text-sm font-bold text-primary">{inc.incident_id}</span>
                        <span className="bg-error/20 text-error font-bold text-xs px-3 py-1 rounded-full uppercase">
                          {inc.emergency_type}
                        </span>
                      </div>

                      <div className="space-y-2 text-xs text-on-surface-variant">
                        <div className="flex items-center gap-2">
                          <MapPin size={16} className="text-secondary flex-shrink-0" />
                          <span className="font-semibold text-on-surface text-sm">{inc.hospital_name}</span>
                        </div>
                        <div className="flex items-center gap-4 text-xs font-mono">
                          <span>ETA: <strong className="text-primary">{inc.eta_minutes} mins</strong></span>
                          <span>|</span>
                          <span>Distance: <strong>{distanceKm} km</strong></span>
                          <span>|</span>
                          <span>Severity: <strong>{Math.round(inc.severity * 100)}%</strong></span>
                        </div>
                        <p className="bg-surface-container-low p-3 rounded-lg italic text-on-surface-variant/80 border border-outline-variant/20">
                          "{inc.details}"
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={() => {
                        setSelectedIncident(inc);
                        setIsNavigating(true);
                      }}
                      className="w-full bg-primary text-on-primary font-bold py-3 px-4 rounded-xl flex items-center justify-center gap-2 shadow-lg hover:bg-primary/90 transition-all active:scale-[0.98]"
                    >
                      ACCEPT & LEAVE FOR DISPATCH <ArrowRight size={18} />
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    );
  }

  // VIEW 2: LIVE TURN-BY-TURN NAVIGATION SCREEN (After selecting an emergency)
  const routeCoords = selectedIncident?.route_coordinates 
    || selectedIncident?.citizen_view?.route_coordinates 
    || [];
  const etaMinutes = selectedIncident?.eta_minutes || 7;
  const distanceKm = selectedIncident?.distance_meters ? (selectedIncident.distance_meters / 1000).toFixed(1) : '2.4';

  return (
    <div className="flex flex-col md:flex-row gap-4 h-[calc(100vh-80px)] p-4 bg-surface text-on-surface">
      {/* Left: Tactical Map & Navigation */}
      <div className="flex-1 flex flex-col gap-4 overflow-hidden">
        {/* Header ETA Banner */}
        <div className="bg-surface-container-high p-4 rounded-xl border border-primary/30 flex justify-between items-center shadow-lg">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-primary/20 text-primary rounded-xl animate-pulse">
              <Navigation size={24} />
            </div>
            <div>
              <span className="text-xs font-label-caps text-primary uppercase font-bold tracking-wider">EN ROUTE TO EMERGENCY</span>
              <h2 className="font-mono text-xl font-bold text-on-surface">{selectedIncident.incident_id}</h2>
            </div>
          </div>

          <div className="text-right">
            <div className="font-mono text-3xl font-black text-primary leading-none">{etaMinutes}m</div>
            <span className="text-[10px] font-label-caps text-on-surface-variant uppercase">ESTIMATED ARRIVAL</span>
          </div>
        </div>

        {/* Map Container */}
        <div className="relative flex-1 min-h-[350px] rounded-xl overflow-hidden border border-outline-variant/30">
          {routeCoords.length > 0 ? (
            <MapOverlay routeCoordinates={routeCoords} height="100%" />
          ) : (
            <div className="absolute inset-0 flex items-center justify-center bg-surface-container-low text-on-surface-variant text-sm">
              Loading Route Map...
            </div>
          )}
          <div className="absolute top-4 right-4 bg-surface-container-highest/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-xl z-10 text-xs font-mono font-bold">
            <span className="w-2 h-2 bg-tertiary rounded-full animate-pulse"></span>
            LIVE TURN-BY-TURN NAV
          </div>
        </div>

        {/* Primary Action Button */}
        <div className="flex gap-4">
          <button 
            onClick={() => setIsNavigating(false)}
            className="px-4 py-4 bg-surface-container-highest text-on-surface rounded-xl font-semibold text-xs hover:bg-surface-variant"
          >
            Back to Queue
          </button>
          <button
            onClick={handleArrived}
            className="flex-1 bg-tertiary text-on-tertiary font-bold text-lg py-4 rounded-xl flex items-center justify-center gap-2 shadow-xl hover:bg-tertiary/90 transition-all active:scale-[0.98]"
          >
            <CheckCircle2 size={24} /> MARK AS ARRIVED AT DESTINATION
          </button>
        </div>
      </div>

      {/* Right: Hospital & Patient Details Panel */}
      <div className="w-full md:w-96 flex flex-col gap-4 overflow-y-auto">
        {/* Hospital Card */}
        <div className="bg-surface-container p-5 rounded-2xl border border-outline-variant/20 space-y-3">
          <h3 className="font-bold text-xs uppercase text-on-surface-variant tracking-wider flex items-center gap-2">
            <MapPin size={16} className="text-secondary" /> Destination Hospital
          </h3>

          <div className="text-lg font-bold text-on-surface">{selectedIncident.hospital_name}</div>

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

        {/* Patient Report Card */}
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
  );
}
"""

with open(driver_jsx, "w", encoding="utf-8") as f:
    f.write(new_driver_jsx)

print("DriverDashboard updated successfully with dispatch queue and navigation modes")

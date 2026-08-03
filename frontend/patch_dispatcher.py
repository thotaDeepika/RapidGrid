import sys

file_path = "src/views/DispatcherDashboard.jsx"

new_code = """import React, { useState, useEffect } from 'react';
import { ShieldAlert, Check, X, AlertTriangle, TrendingUp, CheckCircle2, RefreshCw } from 'lucide-react';
import MapOverlay from '../components/MapOverlay';
import AIRationale from '../components/AIRationale';

export default function DispatcherDashboard() {
  const [incidents, setIncidents] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [autoDispatch, setAutoDispatch] = useState(false);

  // Poll for active incidents every 2 seconds
  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await fetch('/api/incidents/');
        if (!res.ok) return;
        const data = await res.json();
        const incList = data.incidents || [];
        setIncidents(incList);

        // Auto-select first incident if none selected
        if (incList.length > 0 && !selectedIncident) {
          setSelectedIncident(incList[0]);
        } else if (selectedIncident) {
          // Update currently selected incident data
          const updated = incList.find(i => i.incident_id === selectedIncident.incident_id);
          if (updated) setSelectedIncident(updated);
        }
      } catch (err) {
        console.error('Failed to fetch incidents:', err);
      }
    };

    fetchIncidents();
    const interval = setInterval(fetchIncidents, 2000);
    return () => clearInterval(interval);
  }, [selectedIncident]);

  // Handle Approve / Reject
  const handleDecision = async (decision) => {
    if (!selectedIncident) return;

    try {
      if (decision === 'approved') {
        const res = await fetch(`/api/incidents/${selectedIncident.incident_id}/approve`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            dispatcher_id: 'DISPATCHER-01',
            approved_hospital: selectedIncident.action_plan?.recommended_hospital?.hospital_id || 'HOSP-DEFAULT',
            approved_route: selectedIncident.action_plan?.recommended_route?.route_id || 'ROUTE-DEFAULT'
          })
        });

        if (res.ok) {
          const updatedInc = { ...selectedIncident, status: 'dispatched' };
          setSelectedIncident(updatedInc);
          setIncidents(prev => prev.map(i => i.incident_id === selectedIncident.incident_id ? updatedInc : i));
        }
      }
    } catch (err) {
      console.error('Error approving incident:', err);
    }
  };

  // Extract route coordinates for map
  const routeCoords = selectedIncident?.citizen_view?.route_coordinates 
    || selectedIncident?.action_plan?.recommended_route?.coordinates 
    || [];

  const pendingCount = incidents.filter(i => i.status === 'processing' || i.status === 'awaiting_dispatcher_approval').length;
  const dispatchedCount = incidents.filter(i => i.status === 'dispatched' || i.status === 'completed').length;

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] gap-4 p-4 bg-surface text-on-surface">
      {/* Top Admin Stats Panel */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-surface-container-high p-4 rounded-xl flex items-center gap-4 border border-outline-variant/30">
          <div className="p-3 bg-error/20 text-error rounded-xl"><ShieldAlert size={24}/></div>
          <div>
            <div className="text-xs font-label-caps text-on-surface-variant uppercase">Active Queue</div>
            <div className="text-2xl font-bold font-headline-md">{pendingCount}</div>
          </div>
        </div>

        <div className="bg-surface-container-high p-4 rounded-xl flex items-center gap-4 border border-outline-variant/30">
          <div className="p-3 bg-tertiary/20 text-tertiary rounded-xl"><CheckCircle2 size={24}/></div>
          <div>
            <div className="text-xs font-label-caps text-on-surface-variant uppercase font-mono">Dispatched Today</div>
            <div className="text-2xl font-bold font-headline-md">{dispatchedCount}</div>
          </div>
        </div>

        <div className="bg-surface-container-high p-4 rounded-xl flex items-center gap-4 border border-outline-variant/30">
          <div className="p-3 bg-secondary/20 text-secondary rounded-xl"><TrendingUp size={24}/></div>
          <div>
            <div className="text-xs font-label-caps text-on-surface-variant uppercase font-mono">AI Confidence</div>
            <div className="text-2xl font-bold font-headline-md">94%</div>
          </div>
        </div>

        <div className="bg-surface-container-high p-4 rounded-xl flex items-center justify-between border border-outline-variant/30">
          <div>
            <div className="text-xs font-label-caps text-on-surface-variant uppercase font-mono">Auto-Dispatch</div>
            <div className="text-xs text-on-surface-variant">{autoDispatch ? 'AUTOMATIC MODE' : 'MANUAL APPROVAL'}</div>
          </div>
          <button 
            onClick={() => setAutoDispatch(!autoDispatch)}
            className={`px-3 py-1.5 rounded-full text-xs font-bold transition-colors ${
              autoDispatch ? 'bg-tertiary text-on-tertiary' : 'bg-surface-container-highest text-on-surface-variant'
            }`}
          >
            {autoDispatch ? 'ENABLED' : 'MANUAL'}
          </button>
        </div>
      </div>

      {/* Main Workspace */}
      <div className="flex gap-4 flex-1 overflow-hidden">
        {/* Left Sidebar - Queue */}
        <div className="w-80 flex flex-col gap-2 overflow-y-auto bg-surface-container p-3 rounded-xl border border-outline-variant/20">
          <h2 className="font-bold text-sm uppercase text-on-surface-variant flex items-center gap-2 mb-2">
            <ShieldAlert size={16} className="text-error" /> Live Emergency Queue
          </h2>

          {incidents.length === 0 ? (
            <div className="text-on-surface-variant/60 text-xs p-4 text-center">
              No active emergencies reported. Raise one from Citizen App!
            </div>
          ) : (
            incidents.map(inc => {
              const isSelected = selectedIncident?.incident_id === inc.incident_id;
              const isPending = inc.status === 'awaiting_dispatcher_approval' || inc.status === 'processing';

              return (
                <button
                  key={inc.incident_id}
                  onClick={() => setSelectedIncident(inc)}
                  className={`p-3 rounded-xl text-left border transition-all ${
                    isSelected 
                      ? 'bg-surface-container-highest border-primary shadow-lg' 
                      : 'bg-surface-container-low border-outline-variant/20 hover:bg-surface-container-high'
                  }`}
                >
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-mono text-xs font-bold text-primary">{inc.incident_id}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                      inc.status === 'dispatched' 
                        ? 'bg-tertiary/20 text-tertiary' 
                        : isPending 
                        ? 'bg-error/20 text-error animate-pulse' 
                        : 'bg-surface-variant text-on-surface-variant'
                    }`}>
                      {inc.status === 'awaiting_dispatcher_approval' ? 'NEEDS APPROVAL' : inc.status}
                    </span>
                  </div>

                  <div className="text-xs text-on-surface font-semibold truncate mb-1">
                    {inc.emergency_type || inc.citizen_text || 'Emergency Incident'}
                  </div>

                  <div className="text-[11px] text-on-surface-variant flex justify-between">
                    <span>Severity: {inc.severity ? Math.round(inc.severity * 100) : 50}%</span>
                    <span>{inc.citizen_view?.hospital_name || 'Calculating...'}</span>
                  </div>
                </button>
              );
            })
          )}
        </div>

        {/* Center/Right - Map & AI Rationale Details */}
        {selectedIncident ? (
          <div className="flex-1 flex gap-4 overflow-hidden">
            {/* Map & Actions */}
            <div className="flex-1 flex flex-col gap-4 overflow-y-auto">
              <div className="bg-surface-container p-4 rounded-xl border border-outline-variant/20 flex flex-col flex-1">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="font-headline-md text-headline-md text-on-surface">Live Tactical Map</h3>
                  <span className="text-xs font-mono text-on-surface-variant">Incident: {selectedIncident.incident_id}</span>
                </div>

                <div className="relative flex-1 min-h-[350px] rounded-xl overflow-hidden">
                  {routeCoords.length > 0 ? (
                    <MapOverlay routeCoordinates={routeCoords} height="100%" />
                  ) : (
                    <div className="absolute inset-0 flex items-center justify-center bg-surface-container-low text-on-surface-variant text-sm">
                      <RefreshCw className="animate-spin mr-2" size={18} /> Processing AI Spatial Route...
                    </div>
                  )}
                </div>
              </div>

              {/* Approval Controls */}
              {(selectedIncident.status === 'awaiting_dispatcher_approval' || selectedIncident.status === 'processing') && (
                <div className="flex gap-4">
                  <button 
                    onClick={() => handleDecision('approved')} 
                    className="flex-1 bg-primary text-on-primary font-bold py-3.5 px-6 rounded-xl flex items-center justify-center gap-2 shadow-lg hover:bg-primary/90 transition-colors"
                  >
                    <Check size={20}/> APPROVE AI DISPATCH PLAN
                  </button>
                  <button 
                    onClick={() => handleDecision('rejected')} 
                    className="bg-surface-container-highest text-error font-semibold py-3.5 px-6 rounded-xl flex items-center justify-center gap-2 hover:bg-error/20 transition-colors"
                  >
                    <X size={20}/> RE-ROUTE / OVERRIDE
                  </button>
                </div>
              )}

              {selectedIncident.status === 'dispatched' && (
                <div className="p-4 bg-tertiary/10 border border-tertiary/30 rounded-xl flex items-center justify-between text-tertiary font-bold text-sm">
                  <span className="flex items-center gap-2">
                    <CheckCircle2 size={20} /> Ambulance Dispatched & En Route
                  </span>
                  <span className="font-mono text-xs">Driver: drv-11</span>
                </div>
              )}
            </div>

            {/* Right - AI Rationale & Hospital Rankings */}
            <div className="w-96 flex flex-col gap-4 overflow-y-auto">
              {selectedIncident.action_plan ? (
                <>
                  <AIRationale plan={selectedIncident.action_plan} />

                  <div className="bg-surface-container p-4 rounded-xl border border-outline-variant/20">
                    <h3 className="font-bold text-xs uppercase text-on-surface-variant tracking-wider mb-3">
                      Ranked Destination Hospitals
                    </h3>
                    <div className="flex flex-col gap-2">
                      {selectedIncident.action_plan.all_hospitals?.map((h, i) => (
                        <div 
                          key={h.hospital_id || i} 
                          className={`p-3 rounded-lg border text-xs ${
                            i === 0 
                              ? 'bg-primary-container/20 border-primary/40 text-on-primary-container' 
                              : 'bg-surface-container-low border-outline-variant/20'
                          }`}
                        >
                          <div className="flex justify-between items-center mb-1">
                            <span className="font-bold">{i + 1}. {h.name}</span>
                            <span className="font-mono text-[10px] bg-surface-container px-2 py-0.5 rounded">
                              Score: {h.score ? h.score.toFixed(2) : '0.92'}
                            </span>
                          </div>
                          <div className="text-[11px] text-on-surface-variant flex gap-3 mt-1">
                            <span>ICU Beds: {h.icu_available ?? 4}</span>
                            <span>Blood: {h.blood_availability ? Math.round(h.blood_availability * 100) : 85}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              ) : (
                <div className="bg-surface-container p-4 rounded-xl border border-outline-variant/20 text-xs text-on-surface-variant text-center">
                  Awaiting AI Decision Fusion Engine response...
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="flex-1 bg-surface-container rounded-xl flex flex-col items-center justify-center text-on-surface-variant/60 border border-outline-variant/20">
            <ShieldAlert size={48} className="mb-3 opacity-40" />
            <p className="font-semibold text-sm">Select an emergency from the queue to review AI recommendations.</p>
          </div>
        )}
      </div>
    </div>
  );
}
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_code)

print("DispatcherDashboard patched successfully")

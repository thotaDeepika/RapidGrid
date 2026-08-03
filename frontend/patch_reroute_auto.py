import sys

file_path = "src/views/DispatcherDashboard.jsx"

new_code = """import React, { useState, useEffect } from 'react';
import { ShieldAlert, Check, X, AlertTriangle, TrendingUp, CheckCircle2, RefreshCw, Navigation, CornerUpRight } from 'lucide-react';
import MapOverlay from '../components/MapOverlay';
import AIRationale from '../components/AIRationale';

export default function DispatcherDashboard() {
  const [incidents, setIncidents] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [autoDispatch, setAutoDispatch] = useState(false);
  const [showOverrideModal, setShowOverrideModal] = useState(false);

  // Poll for active incidents every 2 seconds
  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await fetch('/api/incidents/');
        if (!res.ok) return;
        const data = await res.json();
        const incList = data.incidents || [];
        setIncidents(incList);

        // AUTO-DISPATCH LOGIC: If automatic mode is ON, auto-approve any pending incidents
        if (autoDispatch) {
          incList.forEach(async (inc) => {
            if (inc.status === 'awaiting_dispatcher_approval' && inc.action_plan) {
              try {
                await fetch(`/api/incidents/${inc.incident_id}/approve`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    dispatcher_id: 'AUTO-DISPATCHER-BOT',
                    approved_hospital: inc.action_plan?.recommended_hospital?.hospital_id || 'HOSP-AUTO',
                    approved_route: inc.action_plan?.recommended_route?.route_id || 'ROUTE-AUTO'
                  })
                });
              } catch (e) {
                console.error('Auto-dispatch error:', e);
              }
            }
          });
        }
      } catch (err) {
        console.error('Failed to fetch incidents:', err);
      }
    };

    fetchIncidents();
    const interval = setInterval(fetchIncidents, 2000);
    return () => clearInterval(interval);
  }, [autoDispatch]);

  // Derive selected incident cleanly
  const selectedIncident = incidents.find(i => i.incident_id === selectedId) || incidents[0] || null;

  // Handle Approve with specific hospital (default top or override choice)
  const handleApproveOrOverride = async (targetHospital = null) => {
    if (!selectedIncident) return;

    const chosenHospital = targetHospital || selectedIncident.action_plan?.recommended_hospital;
    const hospId = chosenHospital?.hospital_id || 'HOSP-DEFAULT';
    const hospName = chosenHospital?.name || 'Selected Hospital';

    try {
      const res = await fetch(`/api/incidents/${selectedIncident.incident_id}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dispatcher_id: 'DISPATCHER-01',
          approved_hospital: hospId,
          approved_route: selectedIncident.action_plan?.recommended_route?.route_id || 'ROUTE-DEFAULT'
        })
      });

      if (res.ok) {
        const updatedInc = {
          ...selectedIncident,
          status: 'dispatched',
          citizen_view: {
            ...selectedIncident.citizen_view,
            hospital_name: hospName,
            message: `Help is being dispatched. Approved Hospital: ${hospName}.`
          }
        };
        
        setIncidents(prev => prev.map(i => i.incident_id === selectedIncident.incident_id ? updatedInc : i));
        setShowOverrideModal(false);
      }
    } catch (err) {
      console.error('Error approving/re-routing incident:', err);
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
            <div className="text-xs font-label-caps text-on-surface-variant uppercase font-mono">Auto-Dispatch Mode</div>
            <div className={`text-xs font-bold ${autoDispatch ? 'text-tertiary' : 'text-on-surface-variant'}`}>
              {autoDispatch ? 'AUTOMATIC APPROVAL' : 'MANUAL APPROVAL'}
            </div>
          </div>
          <button 
            onClick={() => setAutoDispatch(!autoDispatch)}
            className={`px-3 py-1.5 rounded-full text-xs font-bold transition-all shadow-md ${
              autoDispatch ? 'bg-tertiary text-on-tertiary ring-2 ring-tertiary/50' : 'bg-surface-container-highest text-on-surface-variant'
            }`}
          >
            {autoDispatch ? 'AUTO (ENABLED)' : 'MANUAL'}
          </button>
        </div>
      </div>

      {/* Main Workspace */}
      <div className="flex gap-4 flex-1 overflow-hidden">
        {/* Left Sidebar - Queue */}
        <div className="w-80 flex flex-col gap-2 overflow-y-auto bg-surface-container p-3 rounded-xl border border-outline-variant/20">
          <div className="flex justify-between items-center mb-2">
            <h2 className="font-bold text-xs uppercase text-on-surface-variant flex items-center gap-1">
              <ShieldAlert size={16} className="text-error" /> Live Emergency Queue
            </h2>
            <button 
              onClick={async () => {
                await fetch('/api/incidents/clear', { method: 'POST' }).catch(() => {});
                setIncidents([]);
                setSelectedId(null);
              }}
              className="text-[10px] text-on-surface-variant hover:text-error underline"
            >
              Clear Queue
            </button>
          </div>

          {incidents.length === 0 ? (
            <div className="text-on-surface-variant/60 text-xs p-4 text-center">
              No active emergencies. Press SOS on Citizen App!
            </div>
          ) : (
            incidents.map(inc => {
              const isSelected = selectedIncident?.incident_id === inc.incident_id;
              const isPending = inc.status === 'awaiting_dispatcher_approval' || inc.status === 'processing';

              return (
                <button
                  key={inc.incident_id}
                  onClick={() => setSelectedId(inc.incident_id)}
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

              {/* Action & Override Controls */}
              <div className="flex flex-col gap-3">
                {/* Automatic Mode Indicator banner if Auto-Dispatch is ON */}
                {autoDispatch && (
                  <div className="p-3 bg-tertiary/10 border border-tertiary/30 rounded-xl text-tertiary text-xs font-bold flex items-center justify-between">
                    <span>AUTO MODE ACTIVE - AI automatically approving incoming plans.</span>
                    <span className="font-mono text-[10px]">Status: {selectedIncident.status}</span>
                  </div>
                )}

                <div className="flex gap-4">
                  {/* Show Manual Approve button if in Manual mode AND incident needs approval */}
                  {!autoDispatch && (selectedIncident.status === 'awaiting_dispatcher_approval' || selectedIncident.status === 'processing') && (
                    <button 
                      onClick={() => handleApproveOrOverride()} 
                      className="flex-1 bg-primary text-on-primary font-bold py-3.5 px-6 rounded-xl flex items-center justify-center gap-2 shadow-lg hover:bg-primary/90 transition-colors"
                    >
                      <Check size={20}/> APPROVE AI DISPATCH PLAN
                    </button>
                  )}

                  {/* RE-ROUTE / OVERRIDE button (Available in BOTH Manual and Automatic modes!) */}
                  <button 
                    onClick={() => setShowOverrideModal(!showOverrideModal)} 
                    className="flex-1 bg-surface-container-highest text-error border border-error/30 font-semibold py-3.5 px-6 rounded-xl flex items-center justify-center gap-2 hover:bg-error/20 transition-colors"
                  >
                    <CornerUpRight size={20}/> {showOverrideModal ? 'CLOSE OVERRIDE' : 'RE-ROUTE / OVERRIDE'}
                  </button>
                </div>

                {/* Interactive Override Selector Panel when RE-ROUTE is clicked */}
                {showOverrideModal && (
                  <div className="p-4 bg-surface-container-high border-2 border-error/40 rounded-xl space-y-3">
                    <div className="flex justify-between items-center">
                      <h4 className="text-xs font-bold text-error uppercase tracking-wider flex items-center gap-1">
                        <Navigation size={14} /> Manual Override - Pick Destination Hospital
                      </h4>
                      <span className="text-[11px] text-on-surface-variant">Click any hospital to re-route immediately</span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {selectedIncident.action_plan?.all_hospitals?.slice(0, 4).map((h, idx) => (
                        <button
                          key={h.hospital_id || idx}
                          onClick={() => handleApproveOrOverride(h)}
                          className="p-3 bg-surface-container rounded-lg border border-outline-variant/30 hover:border-error text-left flex justify-between items-center transition-all hover:scale-[1.01]"
                        >
                          <div>
                            <div className="text-xs font-bold text-on-surface">{idx + 1}. {h.name}</div>
                            <div className="text-[10px] text-on-surface-variant">ICU: {h.icu_available ?? 5} beds | Blood: {h.blood_availability ? Math.round(h.blood_availability*100) : 85}%</div>
                          </div>
                          <span className="text-[10px] font-bold bg-error/20 text-error px-2 py-1 rounded">Re-Route Here</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Right - AI Rationale & Hospital Rankings */}
            <div className="w-96 flex flex-col gap-4 overflow-y-auto">
              {selectedIncident.action_plan ? (
                <>
                  <AIRationale plan={selectedIncident.action_plan} />

                  <div className="bg-surface-container p-4 rounded-xl border border-outline-variant/20">
                    <h3 className="font-bold text-xs uppercase text-on-surface-variant tracking-wider mb-3">
                      Ranked Destination Hospitals (Click to Re-Route)
                    </h3>
                    <div className="flex flex-col gap-2">
                      {selectedIncident.action_plan.all_hospitals?.map((h, i) => (
                        <button 
                          key={h.hospital_id || i}
                          onClick={() => handleApproveOrOverride(h)}
                          className={`p-3 rounded-lg border text-xs text-left transition-all hover:border-primary ${
                            selectedIncident.citizen_view?.hospital_name === h.name || (i === 0 && !selectedIncident.citizen_view?.hospital_name)
                              ? 'bg-primary-container/20 border-primary/40 text-on-primary-container ring-1 ring-primary/30' 
                              : 'bg-surface-container-low border-outline-variant/20 hover:bg-surface-container-high'
                          }`}
                        >
                          <div className="flex justify-between items-center mb-1">
                            <span className="font-bold">{i + 1}. {h.name}</span>
                            <span className="font-mono text-[10px] bg-surface-container px-2 py-0.5 rounded">
                              Score: {h.score ? h.score.toFixed(2) : '0.92'}
                            </span>
                          </div>
                          <div className="text-[11px] text-on-surface-variant flex justify-between mt-1">
                            <span>ICU Beds: {h.icu_available ?? 4} | Blood: {h.blood_availability ? Math.round(h.blood_availability * 100) : 85}%</span>
                            <span className="text-primary font-bold hover:underline">Select & Route</span>
                          </div>
                        </button>
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

print("DispatcherDashboard auto-dispatch and re-route override patched successfully")

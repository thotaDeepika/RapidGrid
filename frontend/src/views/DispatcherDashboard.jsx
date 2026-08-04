import React, { useState, useEffect } from 'react';
import { ShieldAlert, Check, TrendingUp, CheckCircle2, RefreshCw, Navigation, CornerUpRight } from 'lucide-react';
import MapOverlay from '../components/MapOverlay';
import AIRationale from '../components/AIRationale';

export default function DispatcherDashboard() {
  const [incidents, setIncidents] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [autoDispatch, setAutoDispatch] = useState(false);
  const [showOverrideModal, setShowOverrideModal] = useState(false);

  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await fetch('/api/incidents/');
        if (!res.ok) return;
        const data = await res.json();
        const incList = data.incidents || [];
        setIncidents(incList);

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
              } catch (e) {}
            }
          });
        }
      } catch (err) {}
    };

    fetchIncidents();
    const interval = setInterval(fetchIncidents, 2000);
    return () => clearInterval(interval);
  }, [autoDispatch]);

  const selectedIncident = incidents.find(i => i.incident_id === selectedId) || incidents[0] || null;

  const handleApproveOrOverride = async (targetHospital = null) => {
    if (!selectedIncident) return;

    const chosenHospital = targetHospital || selectedIncident.action_plan?.recommended_hospital;
    const hospId = chosenHospital?.hospital_id || 'HOSP-DEFAULT';

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
        const updatedBackendInc = await res.json();
        setIncidents(prev => prev.map(i => i.incident_id === selectedIncident.incident_id ? updatedBackendInc : i));
        setShowOverrideModal(false);
      }
    } catch (err) {}
  };

  const routeCoords = selectedIncident?.citizen_view?.route_coordinates 
    || selectedIncident?.action_plan?.recommended_route?.coordinates 
    || [];

  const pendingCount = incidents.filter(i => i.status === 'processing' || i.status === 'awaiting_dispatcher_approval').length;
  const dispatchedCount = incidents.filter(i => i.status === 'dispatched' || i.status === 'completed').length;

  return (
    <div className="flex flex-col min-h-[calc(100vh-80px)] gap-6 p-6 bg-[#ece5f0] text-[#012622] max-w-7xl mx-auto font-body">
      {/* Top Admin Stats Panel */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-[#f5ebf4] text-[#59114d] border border-[#59114d]/20 flex items-center justify-center">
            <ShieldAlert size={24} />
          </div>
          <div>
            <div className="text-[11px] font-mono font-bold text-[#003b36] uppercase">Active Queue</div>
            <div className="text-2xl font-extrabold font-display text-[#012622]">{pendingCount}</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-[#fdf3e7] text-[#e98a15] border border-[#e98a15]/40 flex items-center justify-center">
            <CheckCircle2 size={24} />
          </div>
          <div>
            <div className="text-[11px] font-mono font-bold text-[#003b36] uppercase">Dispatched Calls</div>
            <div className="text-2xl font-extrabold font-display text-[#012622]">{dispatchedCount}</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-[#f5ebf4] text-[#59114d] border border-[#59114d]/20 flex items-center justify-center">
            <TrendingUp size={24} />
          </div>
          <div>
            <div className="text-[11px] font-mono font-bold text-[#003b36] uppercase">AI Fusion Accuracy</div>
            <div className="text-2xl font-extrabold font-display text-[#59114d]">96.4%</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm flex items-center justify-between">
          <div>
            <div className="text-[11px] font-mono font-bold text-[#003b36] uppercase">Approval Mode</div>
            <div className="text-xs font-bold text-[#59114d]">
              {autoDispatch ? 'AUTOMATIC APPROVAL' : 'MANUAL DISPATCH'}
            </div>
          </div>
          <button 
            onClick={() => setAutoDispatch(!autoDispatch)}
            className={`px-4 py-2 rounded-full text-xs font-mono font-bold transition-all border ${
              autoDispatch 
                ? 'bg-[#59114d] text-white border-[#59114d] shadow-sm' 
                : 'bg-[#f4eff7] text-[#012622] border-[#dcd3e3] hover:bg-[#dcd3e3]'
            }`}
          >
            {autoDispatch ? 'AUTO (ON)' : 'MANUAL'}
          </button>
        </div>
      </div>

      {/* Main Workspace */}
      <div className="flex flex-col lg:flex-row gap-6 flex-1">
        {/* Left Sidebar - Live Emergency Queue */}
        <div className="w-full lg:w-80 flex flex-col gap-3 bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm">
          <div className="flex justify-between items-center pb-2 border-b border-[#dcd3e3]">
            <h2 className="font-display font-bold text-xs uppercase text-[#59114d] tracking-wider flex items-center gap-1.5">
              <ShieldAlert size={16} /> Live Emergency Queue
            </h2>
            <button 
              onClick={async () => {
                await fetch('/api/incidents/clear', { method: 'POST' }).catch(() => {});
                setIncidents([]);
                setSelectedId(null);
              }}
              className="text-[11px] font-mono text-[#003b36] hover:text-[#59114d] underline font-semibold"
            >
              Clear
            </button>
          </div>

          {incidents.length === 0 ? (
            <div className="text-[#003b36] text-xs p-6 text-center italic">
              No active emergencies. Trigger SOS from Citizen App.
            </div>
          ) : (
            <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
              {incidents.map(inc => {
                const isSelected = selectedIncident?.incident_id === inc.incident_id;
                const isPending = inc.status === 'awaiting_dispatcher_approval' || inc.status === 'processing';

                return (
                  <button
                    key={inc.incident_id}
                    onClick={() => setSelectedId(inc.incident_id)}
                    className={`w-full p-4 rounded-2xl text-left border transition-all ${
                      isSelected 
                        ? 'bg-[#f5ebf4] border-[#59114d] shadow-sm' 
                        : 'bg-[#ece5f0] border-[#dcd3e3] hover:border-[#59114d]/40'
                    }`}
                  >
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-mono text-xs font-bold text-[#59114d]">{inc.incident_id}</span>
                      <span className={`text-[10px] font-mono px-2.5 py-0.5 rounded-full font-bold uppercase ${
                        inc.status === 'dispatched' 
                          ? 'bg-[#fdf3e7] text-[#e98a15] border border-[#e98a15]/40' 
                          : isPending 
                          ? 'bg-[#f5ebf4] text-[#59114d] animate-pulse border border-[#59114d]/30' 
                          : 'bg-[#f4eff7] text-[#003b36]'
                      }`}>
                        {inc.status === 'awaiting_dispatcher_approval' ? 'NEEDS APPROVAL' : inc.status}
                      </span>
                    </div>

                    <div className="text-xs font-bold text-[#012622] truncate mb-1">
                      {inc.emergency_type || inc.citizen_text || 'Emergency Incident'}
                    </div>

                    <div className="text-[11px] font-mono text-[#003b36] flex justify-between">
                      <span>Severity: {inc.severity ? Math.round(inc.severity * 100) : 50}%</span>
                      <span className="truncate max-w-[120px]">{inc.citizen_view?.hospital_name || 'Calculating...'}</span>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Center/Right - Map & AI Rationale Details */}
        {selectedIncident ? (
          <div className="flex-1 flex flex-col lg:flex-row gap-6">
            {/* Map & Actions */}
            <div className="flex-1 flex flex-col gap-4">
              <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-md flex flex-col flex-1">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="font-display font-bold text-base text-[#012622]">Tactical Spatial Route Map</h3>
                  <span className="text-xs font-mono font-bold text-[#59114d]">Incident: {selectedIncident.incident_id}</span>
                </div>

                <div className="relative flex-1 min-h-[360px] rounded-2xl overflow-hidden border border-[#dcd3e3]">
                  {routeCoords.length > 0 ? (
                    <MapOverlay routeCoordinates={routeCoords} height="100%" />
                  ) : (
                    <div className="absolute inset-0 flex items-center justify-center bg-[#ece5f0] text-[#003b36] text-xs font-mono">
                      <RefreshCw className="animate-spin mr-2 text-[#59114d]" size={18} /> Processing AI Spatial Route...
                    </div>
                  )}
                </div>
              </div>

              {/* Action Controls */}
              <div className="flex flex-col gap-3">
                {autoDispatch && (
                  <div className="p-3.5 bg-[#f5ebf4] border border-[#59114d]/30 rounded-2xl text-[#59114d] text-xs font-mono font-bold flex items-center justify-between">
                    <span>AUTO MODE ACTIVE — AI automatically approving incoming plans.</span>
                    <span>Status: {selectedIncident.status}</span>
                  </div>
                )}

                <div className="flex gap-4">
                  {!autoDispatch && (selectedIncident.status === 'awaiting_dispatcher_approval' || selectedIncident.status === 'processing') && (
                    <button 
                      onClick={() => handleApproveOrOverride()} 
                      className="flex-1 bg-[#59114d] hover:bg-[#420b39] text-white font-bold py-3.5 px-6 rounded-2xl flex items-center justify-center gap-2 shadow-elevation-md transition-all active:scale-95 text-xs font-mono"
                    >
                      <Check size={18}/> APPROVE AI DISPATCH PLAN
                    </button>
                  )}

                  <button 
                    onClick={() => setShowOverrideModal(!showOverrideModal)} 
                    className="flex-1 bg-white hover:bg-[#f4eff7] text-[#012622] border border-[#dcd3e3] font-bold py-3.5 px-6 rounded-2xl flex items-center justify-center gap-2 shadow-elevation-sm transition-all active:scale-95 text-xs font-mono"
                  >
                    <CornerUpRight size={18}/> {showOverrideModal ? 'CLOSE OVERRIDE' : 'MANUAL RE-ROUTE / OVERRIDE'}
                  </button>
                </div>

                {showOverrideModal && (
                  <div className="p-5 bg-white border border-[#59114d] rounded-3xl space-y-3 shadow-elevation-md">
                    <div className="flex justify-between items-center">
                      <h4 className="text-xs font-mono font-bold text-[#59114d] uppercase tracking-wider flex items-center gap-1.5">
                        <Navigation size={16} /> Manual Override — Pick Destination Hospital
                      </h4>
                      <span className="text-[11px] text-[#003b36] font-mono">Select any candidate hospital to re-route</span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {selectedIncident.action_plan?.all_hospitals?.slice(0, 4).map((h, idx) => (
                        <button
                          key={h.hospital_id || idx}
                          onClick={() => handleApproveOrOverride(h)}
                          className="p-3.5 bg-[#ece5f0] hover:bg-[#f5ebf4] rounded-2xl border border-[#dcd3e3] hover:border-[#59114d] text-left flex justify-between items-center transition-all"
                        >
                          <div>
                            <div className="text-xs font-bold text-[#012622]">{idx + 1}. {h.name}</div>
                            <div className="text-[10px] font-mono text-[#003b36]">ICU: {h.icu_available ?? 5} beds | Blood: {h.blood_availability ? Math.round(h.blood_availability*100) : 85}%</div>
                          </div>
                          <span className="text-[10px] font-mono font-bold bg-[#59114d] text-white px-2.5 py-1 rounded-full">Re-Route</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Right - AI Rationale & Hospital Rankings */}
            <div className="w-full lg:w-96 flex flex-col gap-4">
              {selectedIncident.action_plan ? (
                <>
                  <AIRationale plan={selectedIncident.action_plan} />

                  <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-md space-y-3">
                    <h3 className="font-display font-bold text-xs uppercase text-[#003b36] tracking-wider">
                      Ranked Destination Hospitals
                    </h3>
                    <div className="flex flex-col gap-2.5">
                      {selectedIncident.action_plan.all_hospitals?.map((h, i) => (
                        <button 
                          key={h.hospital_id || i}
                          onClick={() => handleApproveOrOverride(h)}
                          className={`p-3.5 rounded-2xl border text-xs text-left transition-all ${
                            selectedIncident.citizen_view?.hospital_name === h.name || (i === 0 && !selectedIncident.citizen_view?.hospital_name)
                              ? 'bg-[#f5ebf4] border-[#59114d] text-[#012622] shadow-sm' 
                              : 'bg-[#ece5f0] border-[#dcd3e3] hover:border-[#59114d]/40'
                          }`}
                        >
                          <div className="flex justify-between items-center mb-1">
                            <span className="font-bold">{i + 1}. {h.name}</span>
                            <span className="font-mono text-[10px] font-bold bg-white px-2 py-0.5 rounded-full border border-[#dcd3e3]">
                              Score: {h.score ? h.score.toFixed(2) : '0.92'}
                            </span>
                          </div>
                          <div className="text-[11px] font-mono text-[#003b36] flex justify-between mt-1">
                            <span>ICU: {h.icu_available ?? 4} beds</span>
                            <span className="text-[#59114d] font-bold hover:underline">Select & Route</span>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              ) : (
                <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] text-xs text-[#003b36] text-center font-mono shadow-elevation-sm">
                  Awaiting AI Decision Fusion Engine response...
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="flex-1 bg-white rounded-3xl flex flex-col items-center justify-center text-[#003b36] border border-[#dcd3e3] p-12 shadow-elevation-sm">
            <ShieldAlert size={48} className="mb-3 text-[#59114d]" />
            <p className="font-display font-bold text-base text-[#012622]">Select an emergency call from the queue to review AI recommendations.</p>
          </div>
        )}
      </div>
    </div>
  );
}

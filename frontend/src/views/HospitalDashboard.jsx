import LiveEmergencyChat from '../components/LiveEmergencyChat';
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { PlusSquare, Activity, User, Clock, AlertTriangle, CheckCircle2, ShieldAlert, HeartPulse, Stethoscope, Droplet } from 'lucide-react';

export default function HospitalDashboard() {
  const { hospitalInfo } = useAuth();
  const [incomingCases, setIncomingCases] = useState([]);
  const [icuAvailable, setIcuAvailable] = useState(true);
  const [acknowledgedCases, setAcknowledgedCases] = useState({});

  const toggleIcu = async () => {
    const newVal = !icuAvailable;
    setIcuAvailable(newVal);
    try {
      await fetch('/api/hospital/mock-hospital-1/resources', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ icu_available: newVal })
      }).catch(() => {});
    } catch (err) {
      console.error('Failed to update ICU status:', err);
    }
  };

  // Poll for incoming emergency cases
  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await fetch(`/api/hospital/${hospitalInfo?.id || 'all'}/incoming?name=${encodeURIComponent(hospitalInfo?.name || '')}`);
        if (!res.ok) return;
        const data = await res.json();
        setIncomingCases(data.incoming || []);
      } catch (err) {
        console.error('Error fetching incoming hospital cases:', err);
      }
    };

    fetchIncidents();
    const interval = setInterval(fetchIncidents, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleAcknowledge = (incidentId) => {
    setAcknowledgedCases(prev => ({ ...prev, [incidentId]: true }));
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] p-4 bg-surface text-on-surface gap-4 overflow-y-auto">
      {/* Top ER Command Bar */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Hospital Info */}
        <div className="bg-surface-container-high p-4 rounded-2xl border border-outline-variant/30 flex items-center gap-4">
          <div className="p-3 bg-primary/20 text-primary rounded-xl">
            <PlusSquare size={24} />
          </div>
          <div>
            <h1 className="font-headline-md text-base font-bold text-on-surface">{hospitalInfo?.name || "Bangalore Central ER Desk"}</h1>
            <p className="text-xs text-on-surface-variant">Bangalore Central ER Desk</p>
          </div>
        </div>

        {/* ICU Bed Status Toggle */}
        <div className="bg-surface-container-high p-4 rounded-2xl border border-outline-variant/30 flex items-center justify-between">
          <div>
            <div className="text-xs font-label-caps text-on-surface-variant uppercase font-mono">ICU Beds</div>
            <div className={`text-xs font-bold ${icuAvailable ? 'text-tertiary' : 'text-error'}`}>
              {icuAvailable ? '12 BEDS AVAILABLE' : 'FULL (DIVERT)'}
            </div>
          </div>
          <button 
            onClick={toggleIcu}
            className={`px-3 py-1.5 rounded-full text-xs font-bold transition-all shadow-md ${
              icuAvailable ? 'bg-tertiary text-on-tertiary' : 'bg-error text-on-error'
            }`}
          >
            {icuAvailable ? 'AVAILABLE' : 'TOGGLE FULL'}
          </button>
        </div>

        {/* Trauma Center Readiness */}
        <div className="bg-surface-container-high p-4 rounded-2xl border border-outline-variant/30 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-secondary/20 text-secondary rounded-lg">
              <Stethoscope size={20} />
            </div>
            <div>
              <div className="text-xs font-label-caps text-on-surface-variant uppercase font-mono">Trauma Bay</div>
              <div className="text-xs font-bold text-secondary">STANDBY READY</div>
            </div>
          </div>
          <span className="w-2.5 h-2.5 bg-secondary rounded-full animate-pulse"></span>
        </div>

        {/* Blood Bank Availability */}
        <div className="bg-surface-container-high p-4 rounded-2xl border border-outline-variant/30 flex items-center gap-3">
          <div className="p-2 bg-error/20 text-error rounded-lg">
            <Droplet size={20} />
          </div>
          <div>
            <div className="text-xs font-label-caps text-on-surface-variant uppercase font-mono">Blood Bank</div>
            <div className="text-xs font-bold text-on-surface">O- / A+ / B+ OPTIMAL (88%)</div>
          </div>
        </div>
      </div>

      {/* Main Incoming ER Patient Queue */}
      <div className="flex-1 bg-surface-container p-5 rounded-2xl border border-outline-variant/20 flex flex-col overflow-hidden">
        <div className="flex justify-between items-center mb-4">
          <h2 className="font-bold text-sm uppercase text-on-surface-variant tracking-wider flex items-center gap-2">
            <Activity className="text-primary" size={20} /> Live ER Incoming Patients ({incomingCases.length})
          </h2>
          <span className="text-xs font-mono text-on-surface-variant/80">Real-time sync with Ambulance & AI Agents</span>
        </div>

        {incomingCases.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-on-surface-variant/50 gap-3 border border-dashed border-outline-variant/20 rounded-xl p-8">
            <User size={48} className="opacity-30" />
            <p className="font-semibold text-sm">No incoming ambulance dispatches at this moment.</p>
            <p className="text-xs text-on-surface-variant/60">Raise an SOS on Citizen App to simulate an incoming emergency.</p>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto space-y-3 pr-2">
            {incomingCases.map(inc => {
              const isAck = acknowledgedCases[inc.incident_id];
              const severityPct = Math.round((inc.severity || 0.7) * 100);

              return (
                <div 
                  key={inc.incident_id}
                  className="bg-surface-container-high p-4 rounded-xl border border-outline-variant/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-md hover:border-primary/40 transition-all"
                >
                  {/* Left: ETA Badge */}
                  <div className="flex items-center gap-4 min-w-[120px]">
                    <div className="bg-primary/20 text-primary p-3 rounded-xl text-center min-w-[70px]">
                      <div className="font-mono text-2xl font-black leading-none">{inc.eta_minutes || 7}m</div>
                      <span className="text-[9px] font-label-caps uppercase font-bold">ETA</span>
                    </div>
                    <div>
                      <span className="font-mono text-xs font-bold text-primary block">{inc.incident_id}</span>
                      <span className="bg-error/20 text-error font-bold text-[10px] px-2.5 py-0.5 rounded-full uppercase inline-block mt-1">
                        {inc.emergency_type}
                      </span>
                    </div>
                  </div>

                  {/* Center: Details & Destination */}
                  <div className="flex-1 space-y-1">
                    <div className="text-xs font-semibold text-on-surface flex items-center gap-2">
                      <span>Destination: <strong className="text-secondary">{inc.hospital_name}</strong></span>
                      <span>|</span>
                      <span className="text-on-surface-variant">Driver Unit: {inc.assigned_driver || 'AMB-IND-04'}</span>
                    </div>
                    <p className="text-xs text-on-surface-variant italic bg-surface-container p-2.5 rounded-lg border border-outline-variant/10">
                      "{inc.patient_summary}"
                    </p>
                  </div>

                  {/* Right: Severity & ER Actions */}
                  <div className="flex items-center gap-4 min-w-[240px] justify-between md:justify-end w-full md:w-auto">
                    <div className="text-right min-w-[90px]">
                      <div className="text-[10px] font-label-caps text-on-surface-variant uppercase">Severity</div>
                      <div className="font-bold text-sm text-error">{severityPct}%</div>
                      <div className="w-16 h-1.5 bg-surface-container rounded-full overflow-hidden mt-1">
                        <div 
                          className={`h-full ${severityPct > 75 ? 'bg-error' : severityPct > 45 ? 'bg-secondary' : 'bg-tertiary'}`} 
                          style={{ width: `${severityPct}%` }}
                        />
                      </div>
                    </div>

                    <button
                      onClick={() => handleAcknowledge(inc.incident_id)}
                      className={`px-4 py-3 rounded-xl text-xs font-bold transition-all shadow-md flex items-center gap-2 ${
                        isAck 
                          ? 'bg-tertiary/20 text-tertiary border border-tertiary/40' 
                          : 'bg-primary text-on-primary hover:bg-primary/90'
                      }`}
                    >
                      <CheckCircle2 size={16} />
                      {isAck ? 'BED RESERVED' : 'PREPARE ER BED'}
                    </button>
                  
                    {/* Live ER Socket Chat */}
                    <div className="mt-3">
                      <LiveEmergencyChat
                        incidentId={inc.incident_id}
                        senderRole="hospital"
                        senderName={hospitalInfo?.name || 'Hospital ER Desk'}
                        targetPhone="+919876543210"
                      />
                    </div>
</div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

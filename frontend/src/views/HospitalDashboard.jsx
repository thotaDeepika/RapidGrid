import LiveEmergencyChat from '../components/LiveEmergencyChat';
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { PlusSquare, Activity, User, CheckCircle2, Stethoscope, Droplet } from 'lucide-react';

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
    } catch (err) {}
  };

  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        const res = await fetch(`/api/hospital/${hospitalInfo?.id || 'all'}/incoming?name=${encodeURIComponent(hospitalInfo?.name || '')}`);
        if (!res.ok) return;
        const data = await res.json();
        setIncomingCases(data.incoming || []);
      } catch (err) {}
    };

    fetchIncidents();
    const interval = setInterval(fetchIncidents, 2000);
    return () => clearInterval(interval);
  }, [hospitalInfo]);

  const handleAcknowledge = (incidentId) => {
    setAcknowledgedCases(prev => ({ ...prev, [incidentId]: true }));
  };

  return (
    <div className="flex flex-col min-h-[calc(100vh-80px)] p-6 bg-[#ece5f0] text-[#012622] gap-6 max-w-7xl mx-auto font-body">
      {/* Top ER Command Bar */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-[#f5ebf4] text-[#59114d] border border-[#59114d]/20 flex items-center justify-center">
            <PlusSquare size={24} />
          </div>
          <div>
            <h1 className="font-display text-base font-extrabold text-[#012622]">{hospitalInfo?.name || "Bangalore Central ER Desk"}</h1>
            <p className="text-xs text-[#003b36]">Emergency Department Terminal</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm flex items-center justify-between">
          <div>
            <div className="text-[11px] font-mono font-bold text-[#003b36] uppercase">ICU Capacity</div>
            <div className={`text-xs font-bold font-mono ${icuAvailable ? 'text-[#59114d]' : 'text-red-600'}`}>
              {icuAvailable ? '12 BEDS READY' : 'FULL (DIVERT)'}
            </div>
          </div>
          <button 
            onClick={toggleIcu}
            className={`px-3.5 py-1.5 rounded-full text-xs font-mono font-bold transition-all border ${
              icuAvailable ? 'bg-[#59114d] text-white border-[#59114d] shadow-sm' : 'bg-red-50 text-red-600 border-red-200'
            }`}
          >
            {icuAvailable ? 'AVAILABLE' : 'TOGGLE FULL'}
          </button>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#fdf3e7] text-[#e98a15] border border-[#e98a15]/40 flex items-center justify-center">
              <Stethoscope size={20} />
            </div>
            <div>
              <div className="text-[11px] font-mono font-bold text-[#003b36] uppercase">Trauma Bay</div>
              <div className="text-xs font-bold text-[#e98a15]">STANDBY READY</div>
            </div>
          </div>
          <span className="w-2.5 h-2.5 bg-[#e98a15] rounded-full animate-pulse"></span>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#f5ebf4] text-[#59114d] border border-[#59114d]/20 flex items-center justify-center">
            <Droplet size={20} />
          </div>
          <div>
            <div className="text-[11px] font-mono font-bold text-[#003b36] uppercase">Blood Supply</div>
            <div className="text-xs font-bold text-[#012622] font-mono">O- / A+ / B+ OPTIMAL (88%)</div>
          </div>
        </div>
      </div>

      <div className="flex-1 bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-md flex flex-col space-y-4">
        <div className="flex justify-between items-center pb-3 border-b border-[#dcd3e3]">
          <h2 className="font-display font-bold text-base text-[#012622] uppercase tracking-wider flex items-center gap-2">
            <Activity className="text-[#59114d]" size={22} /> Incoming Ambulance Triage Queue ({incomingCases.length})
          </h2>
          <span className="text-xs font-mono text-[#003b36]">Real-time sync with Ambulance & AI Agents</span>
        </div>

        {incomingCases.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-[#003b36] gap-3 border border-dashed border-[#dcd3e3] rounded-2xl p-12 my-4">
            <User size={48} className="text-[#59114d]/40" />
            <p className="font-display font-bold text-sm text-[#012622]">No incoming ambulance dispatches at this moment.</p>
            <p className="text-xs text-[#003b36]">Trigger an SOS from the Citizen App to simulate incoming patients.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {incomingCases.map(inc => {
              const isAck = acknowledgedCases[inc.incident_id];
              const severityPct = Math.round((inc.severity || 0.7) * 100);

              return (
                <div 
                  key={inc.incident_id}
                  className="bg-[#ece5f0] p-5 rounded-3xl border border-[#dcd3e3] flex flex-col space-y-4 shadow-elevation-sm hover:border-[#59114d] transition-all"
                >
                  <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                    <div className="flex items-center gap-4 min-w-[140px]">
                      <div className="bg-[#59114d] text-white p-3.5 rounded-2xl text-center min-w-[80px] shadow-md">
                        <div className="font-display font-extrabold text-2xl leading-none">{inc.eta_minutes || 7}m</div>
                        <span className="text-[10px] font-mono uppercase font-bold text-[#e98a15]">ETA</span>
                      </div>
                      <div>
                        <span className="font-mono text-xs font-bold text-[#59114d] block">{inc.incident_id}</span>
                        <span className="bg-[#f5ebf4] text-[#59114d] font-mono text-[10px] px-2.5 py-0.5 rounded-full uppercase font-bold inline-block mt-1 border border-[#59114d]/20">
                          {inc.emergency_type}
                        </span>
                      </div>
                    </div>

                    <div className="flex-1 space-y-1.5">
                      <div className="text-xs font-semibold text-[#012622] flex items-center gap-2">
                        <span>Target: <strong className="text-[#59114d] font-bold">{inc.hospital_name}</strong></span>
                        <span>|</span>
                        <span className="text-[#003b36] font-mono">Driver Unit: {inc.assigned_driver || 'AMB-UNIT-04'}</span>
                      </div>
                      <p className="text-xs text-[#003b36] italic bg-white p-3 rounded-xl border border-[#dcd3e3]">
                        "{inc.patient_summary}"
                      </p>
                    </div>

                    <div className="flex items-center gap-4 min-w-[240px] justify-between md:justify-end w-full md:w-auto">
                      <div className="text-right min-w-[90px]">
                        <div className="text-[10px] font-mono text-[#003b36] uppercase">Severity</div>
                        <div className="font-bold text-sm text-[#59114d] font-mono">{severityPct}%</div>
                        <div className="w-16 h-1.5 bg-[#dcd3e3] rounded-full overflow-hidden mt-1">
                          <div 
                            className="h-full bg-[#59114d]" 
                            style={{ width: `${severityPct}%` }}
                          />
                        </div>
                      </div>

                      <button
                        onClick={() => handleAcknowledge(inc.incident_id)}
                        className={`px-4 py-3 rounded-2xl text-xs font-mono font-bold transition-all shadow-sm flex items-center gap-2 ${
                          isAck 
                            ? 'bg-[#fdf3e7] text-[#e98a15] border border-[#e98a15]/40' 
                            : 'bg-[#59114d] text-white hover:bg-[#420b39]'
                        }`}
                      >
                        <CheckCircle2 size={16} />
                        {isAck ? 'BED RESERVED' : 'PREPARE ER BED'}
                      </button>
                    </div>
                  </div>

                  <div className="pt-2 border-t border-[#dcd3e3]">
                    <LiveEmergencyChat
                      incidentId={inc.incident_id}
                      senderRole="hospital"
                      senderName={hospitalInfo?.name || 'Hospital ER Desk'}
                      targetPhone="+919876543210"
                    />
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

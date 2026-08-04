import React, { useState, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Shield, Activity, Truck, PlusSquare, ChevronRight, Heart, Zap, Lock, Sparkles, CheckCircle2 } from 'lucide-react';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const systemAccessRef = useRef(null);

  const [showDriverModal, setShowDriverModal] = useState(false);
  const [customDriverName, setCustomDriverName] = useState('');
  const [customUnitId, setCustomUnitId] = useState('');
  const [customHubName, setCustomHubName] = useState('');
  const [customVehicleType, setCustomVehicleType] = useState('Ambulance');

  const emergencyDriverUnits = [
    { unitId: 'AMB-UNIT-04', vehicleType: 'Ambulance', driverName: 'Suresh Kumar', hubName: 'Aster CMI Emergency Ambulance Hub', phone: '+91 98765 43210' },
    { unitId: 'AMB-UNIT-01', vehicleType: 'Ambulance', driverName: 'Ramesh Gowda', hubName: 'Manipal Ambulance Base Depot', phone: '+91 98765 43211' },
    { unitId: 'AMB-UNIT-02', vehicleType: 'Ambulance', driverName: 'Vijay Naik', hubName: 'Victoria Hospital Paramedic Base', phone: '+91 98765 43212' },
    { unitId: 'FIRE-UNIT-09', vehicleType: 'Fire Engine', driverName: 'Capt. Rajesh Rao', hubName: 'Hebbal Fire & Rescue Station #4', phone: '+91 98765 43220' },
    { unitId: 'FIRE-UNIT-01', vehicleType: 'Fire Engine', driverName: 'Sub-Officer Praveen', hubName: 'High Grounds Central Fire Station', phone: '+91 98765 43221' },
    { unitId: 'POLICE-UNIT-02', vehicleType: 'Police Cruiser', driverName: 'Insp. Vikram Singh', hubName: 'Hebbal Police Patrol Base', phone: '+91 98765 43230' },
    { unitId: 'RESCUE-UNIT-01', vehicleType: 'Disaster Rescue', driverName: 'Cmdr. Arjun Reddy', hubName: 'NDRF Disaster Rescue Hub North', phone: '+91 98765 43240' }
  ];

  const [showHospModal, setShowHospModal] = useState(false);
  const [showCitModal, setShowCitModal] = useState(false);
  const [customCitName, setCustomCitName] = useState('');
  const [customCitPhone, setCustomCitPhone] = useState('');

  const sampleCitizens = [
    { name: 'Ananya Sharma', phone: '+91 98765 43210' },
    { name: 'Rahul Verma', phone: '+91 91234 56789' },
    { name: 'Priya Patel', phone: '+91 99887 76655' }
  ];

  const bangaloreHospitals = [
    { id: 'all', name: 'Bangalore Central ER Desk (All Incidents)' },
    { id: 'blr-007', name: 'Aster CMI Hospital (Hebbal)' },
    { id: 'blr-001', name: 'Manipal Hospital (Old Airport Road)' },
    { id: 'blr-002', name: 'Fortis Hospital (Bannerghatta Road)' },
    { id: 'blr-003', name: 'Apollo Hospital (Bannerghatta Road)' },
    { id: 'blr-005', name: "St. John's Medical College Hospital" },
    { id: 'blr-012', name: 'Columbia Asia Hospital (Hebbal)' },
    { id: 'medstar', name: 'MEDSTAR Speciality Hospital' },
    { id: 'prolife', name: 'Prolife Hospital' }
  ];

  const scrollToSystemAccess = () => {
    systemAccessRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleRoleLogin = (roleId, extraData = null) => {
    if (roleId === 'driver' && !extraData) {
      setShowDriverModal(true);
      return;
    }
    if (roleId === 'hospital' && !extraData) {
      setShowHospModal(true);
      return;
    }
    if (roleId === 'citizen' && !extraData) {
      setShowCitModal(true);
      return;
    }
    login(roleId, extraData);
    navigate(`/${roleId}`);
  };

  const roles = [
    {
      id: 'citizen',
      label: 'Citizen Mobile App',
      desc: 'Personal SOS & 2-Phase Live Map Tracking',
      icon: Shield,
      accentColor: 'border-[#5f4bb6]',
      iconBg: 'bg-[#5f4bb6]/10 text-[#5f4bb6]',
      badge: 'Citizen Access'
    },
    {
      id: 'dispatcher',
      label: 'City Dispatch Control',
      desc: 'Command Center & Explainable AI Rationale',
      icon: Activity,
      accentColor: 'border-[#5f4bb6]',
      iconBg: 'bg-[#5f4bb6]/10 text-[#5f4bb6]',
      badge: 'Command Center'
    },
    {
      id: 'driver',
      label: 'Paramedic / Driver Unit',
      desc: '2-Stage Navigation & Live Hospital Rerouting',
      icon: Truck,
      accentColor: 'border-[#5f4bb6]',
      iconBg: 'bg-[#5f4bb6]/10 text-[#5f4bb6]',
      badge: 'First Responder'
    },
    {
      id: 'hospital',
      label: 'Hospital ER Terminal',
      desc: 'Dedicated ER Bed Capacity & Patient Triage',
      icon: PlusSquare,
      accentColor: 'border-[#5f4bb6]',
      iconBg: 'bg-[#5f4bb6]/10 text-[#5f4bb6]',
      badge: 'ER Desk'
    },
  ];

  return (
    <div className="bg-[#f6f8fb] min-h-screen text-[#202a25] font-body flex flex-col selection:bg-[#5f4bb6]/20">
      {/* Top Fixed Navigation Header */}
      <header className="fixed top-0 inset-x-0 z-50 bg-white/90 backdrop-blur-md border-b border-[#e2e8f0] shadow-elevation-sm">
        <div className="max-w-6xl mx-auto h-16 px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-[#5f4bb6] text-white flex items-center justify-center shadow-md">
              <Zap size={20} className="fill-current text-[#26f0f1]" />
            </div>
            <span className="font-display text-xl font-extrabold text-[#202a25] tracking-tight">RapidGrid</span>
          </div>
          <button 
            onClick={scrollToSystemAccess}
            className="text-xs font-mono font-bold bg-[#f0f4f9] hover:bg-[#5f4bb6] text-[#202a25] hover:text-white px-4 py-2 rounded-full border border-[#e2e8f0] transition-all shadow-sm active:scale-95"
          >
            PORTAL LOGIN
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 w-full pt-16 flex flex-col items-center">
        <div className="w-full max-w-5xl flex flex-col px-6">
          
          {/* Hero Section */}
          <section className="relative py-16 text-center flex flex-col items-center gap-6">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#f0ecfd] border border-[#86a5d9]/40 text-[#5f4bb6] text-xs font-bold font-mono shadow-sm">
              <Sparkles size={14} className="text-[#5f4bb6]" />
              <span>Autonomous Multi-Agent AI Response Platform</span>
            </div>

            <div className="space-y-4 max-w-3xl">
              <h1 className="font-display text-4xl sm:text-5xl font-extrabold text-[#202a25] tracking-tight leading-tight">
                Rapid Emergency Coordination, <br />
                <span className="bg-gradient-to-r from-[#5f4bb6] via-[#5f4bb6] to-[#86a5d9] bg-clip-text text-transparent">
                  Powered by Autonomous AI
                </span>
              </h1>
              <p className="text-[#5a6860] text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
                Connect citizens, city dispatchers, paramedic responders, and hospital ER desks in seconds. Experience 2-Phase station hub routing and live Uber-style hospital rerouting.
              </p>
            </div>

            <div className="flex flex-wrap gap-4 mt-2 justify-center">
              <button 
                onClick={() => handleRoleLogin('citizen')}
                className="h-13 px-8 bg-[#5f4bb6] hover:bg-[#4c3a9e] text-white font-bold text-sm rounded-full shadow-elevation-md hover:shadow-violet-glow active:scale-95 transition-all flex items-center gap-2"
              >
                <Heart size={18} />
                Get Started as Citizen
              </button>
              <button 
                onClick={scrollToSystemAccess}
                className="h-13 px-8 bg-white hover:bg-[#f0f4f9] text-[#202a25] font-bold text-sm rounded-full border border-[#e2e8f0] shadow-elevation-sm active:scale-95 transition-all flex items-center gap-2"
              >
                Select Portal Access
              </button>
            </div>
          </section>

          {/* Value Feature Highlights */}
          <section className="py-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-2xl border border-[#e2e8f0] flex flex-col gap-3 shadow-elevation-sm hover:shadow-elevation-md transition-all">
                <div className="w-12 h-12 rounded-xl bg-[#f0ecfd] text-[#5f4bb6] border border-[#86a5d9]/30 flex items-center justify-center">
                  <Zap size={24} />
                </div>
                <div>
                  <h3 className="font-display text-base font-bold text-[#202a25]">2-Phase Station Hub Routing</h3>
                  <p className="text-xs text-[#5a6860] leading-relaxed mt-1">
                    Phase 1 calculates hub base response to citizen. Phase 2 handles patient transport to hospital ER.
                  </p>
                </div>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-[#e2e8f0] flex flex-col gap-3 shadow-elevation-sm hover:shadow-elevation-md transition-all">
                <div className="w-12 h-12 rounded-xl bg-[#e6fcfc] text-[#008b8c] border border-[#26f0f1]/50 flex items-center justify-center">
                  <Activity size={24} />
                </div>
                <div>
                  <h3 className="font-display text-base font-bold text-[#202a25]">Uber-Style Live Rerouting</h3>
                  <p className="text-xs text-[#5a6860] leading-relaxed mt-1">
                    First responder field drivers can select any hospital on the fly with instant PWA map route recalculation.
                  </p>
                </div>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-[#e2e8f0] flex flex-col gap-3 shadow-elevation-sm hover:shadow-elevation-md transition-all">
                <div className="w-12 h-12 rounded-xl bg-[#f1f5fc] text-[#5f4bb6] border border-[#86a5d9]/40 flex items-center justify-center">
                  <CheckCircle2 size={24} />
                </div>
                <div>
                  <h3 className="font-display text-base font-bold text-[#202a25]">Explainable AI Decision Fusion</h3>
                  <p className="text-xs text-[#5a6860] leading-relaxed mt-1">
                    5-dimension factor scoring (Response Time, Traffic, Hospital, Severity, Accessibility) with clear dispatcher rationale.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Role Based Login Section */}
          <section ref={systemAccessRef} className="py-12 bg-white rounded-3xl border border-[#e2e8f0] my-8 p-8 space-y-6 shadow-elevation-md">
            <div className="text-center space-y-1">
              <h2 className="font-display text-2xl font-extrabold text-[#202a25]">Select Role Portal</h2>
              <p className="text-xs font-mono text-[#5a6860] uppercase tracking-wider">
                Choose your portal interface to enter the RapidGrid network
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {roles.map(r => {
                const IconComp = r.icon;
                return (
                  <button
                    key={r.id}
                    onClick={() => handleRoleLogin(r.id)}
                    className="group w-full bg-[#f6f8fb] hover:bg-[#f0ecfd] rounded-2xl p-6 flex items-center gap-5 text-left transition-all border border-[#e2e8f0] hover:border-[#5f4bb6] shadow-elevation-sm hover:shadow-elevation-md active:scale-[0.99]"
                  >
                    <div className="w-14 h-14 rounded-2xl bg-white text-[#5f4bb6] border border-[#86a5d9]/40 flex items-center justify-center flex-shrink-0 shadow-sm group-hover:bg-[#5f4bb6] group-hover:text-white transition-all">
                      <IconComp size={26} />
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-display text-base font-bold text-[#202a25] group-hover:text-[#5f4bb6] transition-colors">
                          {r.label}
                        </span>
                        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-[#86a5d9]/20 text-[#5f4bb6] border border-[#86a5d9]/30">
                          {r.badge}
                        </span>
                      </div>
                      <div className="text-xs text-[#5a6860] mt-1">
                        {r.desc}
                      </div>
                    </div>

                    <ChevronRight size={20} className="text-[#86a5d9] group-hover:text-[#5f4bb6] group-hover:translate-x-1 transition-all" />
                  </button>
                );
              })}
            </div>

            <div className="p-4 rounded-2xl bg-[#f6f8fb] flex items-center justify-between border border-[#e2e8f0] text-xs font-mono">
              <div className="flex items-center gap-2.5">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#26f0f1] opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-[#00b8b9]"></span>
                </span>
                <span className="text-[#202a25] font-bold">RapidGrid Autonomous Node v4.2.0</span>
              </div>
              <div className="text-[#5f4bb6] font-bold uppercase tracking-wider">All 9 Agents Operational</div>
            </div>
          </section>

        </div>
      </main>

      {/* Citizen Credentials Modal */}
      {showCitModal && (
        <div className="fixed inset-0 z-50 bg-[#202a25]/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white p-6 rounded-3xl border border-[#e2e8f0] max-w-md w-full space-y-5 shadow-elevation-lg">
            <div className="flex justify-between items-center border-b border-[#e2e8f0] pb-3">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-[#f0ecfd] text-[#5f4bb6]">
                  <Shield size={22} />
                </div>
                <div>
                  <h3 className="text-base font-bold font-display text-[#202a25]">Citizen Account Login</h3>
                  <p className="text-xs text-[#5a6860]">Select registered profile or enter custom details</p>
                </div>
              </div>
              <button onClick={() => setShowCitModal(false)} className="text-[#5a6860] hover:text-[#202a25] font-bold text-base px-2">✕</button>
            </div>

            <div className="space-y-2">
              <span className="text-[11px] font-mono text-[#5f4bb6] font-bold block uppercase tracking-wider">Registered Citizen Accounts</span>
              {sampleCitizens.map((c, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setShowCitModal(false);
                    handleRoleLogin('citizen', c);
                  }}
                  className="w-full p-3.5 bg-[#f6f8fb] hover:bg-[#f0ecfd] rounded-2xl border border-[#e2e8f0] hover:border-[#5f4bb6] text-left text-xs font-bold transition-all flex justify-between items-center group"
                >
                  <div>
                    <div className="text-[#202a25] text-sm group-hover:text-[#5f4bb6]">{c.name}</div>
                    <div className="text-[#5a6860] text-[11px] font-mono">{c.phone}</div>
                  </div>
                  <span className="text-[#5f4bb6] font-mono text-xs font-bold">LOGIN &rarr;</span>
                </button>
              ))}
            </div>

            <div className="pt-3 border-t border-[#e2e8f0] space-y-3">
              <span className="text-[11px] font-mono text-[#5a6860] font-bold block uppercase tracking-wider">Or Custom Credentials</span>
              <input
                type="text"
                placeholder="Full Name (e.g. Ramesh Kumar)"
                value={customCitName}
                onChange={(e) => setCustomCitName(e.target.value)}
                className="w-full bg-[#f6f8fb] border border-[#e2e8f0] text-[#202a25] p-3 rounded-xl text-xs focus:outline-none focus:border-[#5f4bb6]"
              />
              <input
                type="text"
                placeholder="Phone Number (e.g. +91 98765 00000)"
                value={customCitPhone}
                onChange={(e) => setCustomCitPhone(e.target.value)}
                className="w-full bg-[#f6f8fb] border border-[#e2e8f0] text-[#202a25] p-3 rounded-xl text-xs focus:outline-none focus:border-[#5f4bb6]"
              />
              <button
                onClick={() => {
                  if (!customCitName.trim()) return;
                  setShowCitModal(false);
                  handleRoleLogin('citizen', { name: customCitName, phone: customCitPhone || '+91 98765 00000' });
                }}
                className="w-full bg-[#5f4bb6] text-white font-bold py-3.5 rounded-xl text-xs shadow-elevation-md hover:bg-[#4c3a9e] transition-all"
              >
                LOG IN AS CUSTOM CITIZEN
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Driver Hub-Wise Login Modal */}
      {showDriverModal && (
        <div className="fixed inset-0 bg-[#202a25]/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white border border-[#e2e8f0] rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-elevation-lg">
            <div className="flex justify-between items-center border-b border-[#e2e8f0] pb-3">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-[#f0ecfd] text-[#5f4bb6]">
                  <Truck size={22} />
                </div>
                <h3 className="font-display font-bold text-base text-[#202a25]">First Responder Station Hub Login</h3>
              </div>
              <button 
                onClick={() => setShowDriverModal(false)}
                className="text-[#5a6860] hover:text-[#202a25] text-base font-bold px-2"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-[#5a6860] font-mono">
              Select your assigned Base Station Hub & Emergency Unit:
            </p>

            {/* Pre-configured Hub Units List */}
            <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
              {emergencyDriverUnits.map((u) => (
                <button
                  key={u.unitId}
                  onClick={() => {
                    setShowDriverModal(false);
                    handleRoleLogin('driver', u);
                  }}
                  className="w-full bg-[#f6f8fb] hover:bg-[#f0ecfd] border border-[#e2e8f0] hover:border-[#5f4bb6] rounded-2xl p-3.5 text-left transition-all flex items-center justify-between group"
                >
                  <div>
                    <div className="font-mono text-xs font-bold text-[#202a25] group-hover:text-[#5f4bb6] flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded-md bg-[#5f4bb6]/10 text-[#5f4bb6] border border-[#86a5d9]/30 text-xs font-mono">{u.unitId}</span>
                      <span>{u.driverName}</span>
                    </div>
                    <div className="text-[11px] text-[#5a6860] mt-1 font-mono">
                      Base Hub: {u.hubName}
                    </div>
                  </div>
                  <ChevronRight size={18} className="text-[#86a5d9] group-hover:text-[#5f4bb6]" />
                </button>
              ))}
            </div>

            {/* Custom Unit Entry Form */}
            <div className="border-t border-[#e2e8f0] pt-3 space-y-2">
              <span className="text-[11px] font-mono text-[#5f4bb6] uppercase font-bold block">Or Custom Driver Credentials:</span>
              <div className="grid grid-cols-2 gap-2">
                <input
                  type="text"
                  placeholder="Driver Name (e.g. Ramesh)"
                  value={customDriverName}
                  onChange={(e) => setCustomDriverName(e.target.value)}
                  className="bg-[#f6f8fb] border border-[#e2e8f0] text-[#202a25] px-3 py-2 rounded-xl text-xs font-mono focus:outline-none focus:border-[#5f4bb6]"
                />
                <input
                  type="text"
                  placeholder="Unit ID (e.g. AMB-UNIT-99)"
                  value={customUnitId}
                  onChange={(e) => setCustomUnitId(e.target.value)}
                  className="bg-[#f6f8fb] border border-[#e2e8f0] text-[#202a25] px-3 py-2 rounded-xl text-xs font-mono focus:outline-none focus:border-[#5f4bb6]"
                />
              </div>
              <input
                type="text"
                placeholder="Station Hub Name (e.g. Hebbal Base Depot)"
                value={customHubName}
                onChange={(e) => setCustomHubName(e.target.value)}
                className="w-full bg-[#f6f8fb] border border-[#e2e8f0] text-[#202a25] px-3 py-2 rounded-xl text-xs font-mono focus:outline-none focus:border-[#5f4bb6]"
              />
              <button
                onClick={() => {
                  if (!customDriverName || !customUnitId) return;
                  setShowDriverModal(false);
                  handleRoleLogin('driver', {
                    unitId: customUnitId,
                    driverName: customDriverName,
                    hubName: customHubName || 'Central Base Depot',
                    vehicleType: customVehicleType
                  });
                }}
                className="w-full py-3 bg-[#5f4bb6] text-white font-bold font-mono rounded-xl text-xs hover:bg-[#4c3a9e] transition-all shadow-md"
              >
                Login to Station Hub Unit
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Hospital Selection Modal */}
      {showHospModal && (
        <div className="fixed inset-0 z-50 bg-[#202a25]/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white p-6 rounded-3xl border border-[#e2e8f0] max-w-md w-full space-y-4 shadow-elevation-lg">
            <div className="flex justify-between items-center border-b border-[#e2e8f0] pb-3">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-[#f0ecfd] text-[#5f4bb6]">
                  <PlusSquare size={22} />
                </div>
                <div>
                  <h3 className="text-base font-bold font-display text-[#202a25]">Select Hospital ER Desk</h3>
                  <p className="text-xs text-[#5a6860]">Pick hospital for dedicated ER bed terminal</p>
                </div>
              </div>
              <button onClick={() => setShowHospModal(false)} className="text-[#5a6860] hover:text-[#202a25] font-bold text-base px-2">✕</button>
            </div>

            <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
              {bangaloreHospitals.map(h => (
                <button
                  key={h.id}
                  onClick={() => {
                    setShowHospModal(false);
                    handleRoleLogin('hospital', h);
                  }}
                  className="w-full p-3.5 bg-[#f6f8fb] hover:bg-[#f0ecfd] rounded-2xl border border-[#e2e8f0] hover:border-[#5f4bb6] text-left text-xs font-bold transition-all flex justify-between items-center group"
                >
                  <span className="text-[#202a25] group-hover:text-[#5f4bb6]">{h.name}</span>
                  <span className="text-[11px] text-[#5f4bb6] font-mono font-bold">LOGIN &rarr;</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

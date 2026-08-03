import sys

login_file = "src/views/Login.jsx"

new_login_jsx = """import React, { useState, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Shield, Activity, Truck, PlusSquare, ChevronRight, Heart, Share2, UserCheck, Smartphone } from 'lucide-react';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const systemAccessRef = useRef(null);

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
      desc: 'Personal SOS & Emergency Tracking',
      icon: Shield,
      color: 'border-tertiary',
      iconBg: 'bg-tertiary/10 text-tertiary',
    },
    {
      id: 'dispatcher',
      label: 'City Dispatch Control',
      desc: 'Command Center Monitoring Portal',
      icon: Activity,
      color: 'border-primary',
      iconBg: 'bg-primary/10 text-primary',
    },
    {
      id: 'driver',
      label: 'Paramedic / Driver Unit',
      desc: 'Ambulance First Responder Field App',
      icon: Truck,
      color: 'border-[#FFB900]',
      iconBg: 'bg-[#FFB900]/10 text-[#FFB900]',
    },
    {
      id: 'hospital',
      label: 'Hospital ER Terminal',
      desc: 'Dedicated ER Bed Capacity Terminal',
      icon: PlusSquare,
      color: 'border-[#B084FF]',
      iconBg: 'bg-[#B084FF]/10 text-[#B084FF]',
    },
  ];

  return (
    <div className="bg-surface min-h-screen text-on-surface font-body-md flex flex-col selection:bg-primary/30">
      {/* Top Fixed Navigation Header */}
      <header className="fixed top-0 inset-x-0 z-50 bg-surface/80 backdrop-blur-xl border-b border-outline-variant/20 shadow-lg">
        <div className="max-w-6xl mx-auto h-16 px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="material-symbols-outlined text-primary text-[28px]">monitor_heart</span>
            <span className="font-headline-md text-xl font-bold text-on-surface tracking-tight">GeoAgentic</span>
          </div>
          <button 
            onClick={scrollToSystemAccess}
            className="text-xs font-mono font-bold bg-surface-container-highest px-3.5 py-1.5 rounded-full border border-outline-variant/30 text-on-surface-variant hover:text-on-surface transition-colors"
          >
            LOGIN PORTAL
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 w-full pt-16 bg-surface flex flex-col items-center">
        <div className="w-full max-w-4xl flex flex-col">
          
          {/* Hero Section */}
          <section className="relative px-6 py-16 overflow-hidden text-center flex flex-col items-center gap-6">
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none">
              <svg className="w-full h-full" preserveAspectRatio="xMidYMid slice" viewBox="0 0 100 100">
                <defs>
                  <radialGradient id="hero-glow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stopColor="#ff5451" stopOpacity="0.4" />
                    <stop offset="100%" stopColor="transparent" stopOpacity="0" />
                  </radialGradient>
                </defs>
                <circle cx="50" cy="30" r="40" fill="url(#hero-glow)">
                  <animate attributeName="opacity" values="0.3;0.7;0.3" dur="8s" repeatCount="indefinite" />
                  <animate attributeName="r" values="35;48;35" dur="10s" repeatCount="indefinite" />
                </circle>
              </svg>
            </div>

            <div className="relative z-10 w-20 h-20 rounded-full bg-surface-container-highest border border-outline-variant/30 flex items-center justify-center shadow-2xl">
              <span className="material-symbols-outlined text-primary text-[42px]">emergency_share</span>
            </div>

            <div className="relative z-10 space-y-3 max-w-2xl">
              <h1 className="font-headline-lg text-4xl md:text-5xl font-black text-on-surface tracking-tight leading-none">
                Your Safety, <br />
                <span className="text-primary bg-gradient-to-r from-primary via-primary-fixed-dim to-tertiary bg-clip-text text-transparent">
                  Our Priority
                </span>
              </h1>
              <p className="text-on-surface-variant text-base md:text-lg max-w-xl mx-auto leading-relaxed">
                A mission-critical agentic network connecting citizens with emergency responders in seconds. Experience rapid, intelligent spatial routing when every moment counts.
              </p>
            </div>

            <div className="relative z-10 flex gap-4 mt-2">
              <button 
                onClick={() => handleRoleLogin('citizen')}
                className="h-14 px-8 bg-primary text-on-primary font-bold text-base rounded-full shadow-[0_4px_16px_rgba(255,84,81,0.4)] active:translate-y-0.5 transition-all flex items-center gap-2 hover:bg-primary/90"
              >
                <Heart size={20} />
                Get Started
              </button>
            </div>
          </section>

          {/* Value Propositions */}
          <section className="px-6 py-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-surface-container p-6 rounded-2xl border border-outline-variant/20 flex flex-col gap-3 shadow-md">
                <div className="w-12 h-12 rounded-xl bg-primary-container/20 text-primary flex items-center justify-center">
                  <span className="material-symbols-outlined text-[28px]">emergency_share</span>
                </div>
                <div>
                  <h3 className="font-headline-md text-base font-bold text-on-surface">Instant SOS</h3>
                  <p className="text-xs text-on-surface-variant leading-relaxed mt-1">
                    One-tap emergency alerts with pinpoint GPS tracking. No delays, just immediate response triggers.
                  </p>
                </div>
              </div>

              <div className="bg-surface-container p-6 rounded-2xl border border-outline-variant/20 flex flex-col gap-3 shadow-md">
                <div className="w-12 h-12 rounded-xl bg-tertiary-container/20 text-tertiary flex items-center justify-center">
                  <span className="material-symbols-outlined text-[28px]">hub</span>
                </div>
                <div>
                  <h3 className="font-headline-md text-base font-bold text-on-surface">Real-Time Sync</h3>
                  <p className="text-xs text-on-surface-variant leading-relaxed mt-1">
                    Seamless data flow between citizens, dispatchers, and paramedics for unified emergency management.
                  </p>
                </div>
              </div>

              <div className="bg-surface-container p-6 rounded-2xl border border-outline-variant/20 flex flex-col gap-3 shadow-md">
                <div className="w-12 h-12 rounded-xl bg-secondary-container/20 text-secondary flex items-center justify-center">
                  <span className="material-symbols-outlined text-[28px]">verified_user</span>
                </div>
                <div>
                  <h3 className="font-headline-md text-base font-bold text-on-surface">Secure & Trusted</h3>
                  <p className="text-xs text-on-surface-variant leading-relaxed mt-1">
                    End-to-end encrypted protocol ensures private information is only shared with verified first responders.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Role Based Login Section */}
          <section ref={systemAccessRef} className="px-6 py-12 bg-surface-container-low/60 rounded-t-[32px] border-t border-outline-variant/20 mt-4 space-y-6">
            <div className="text-center space-y-1">
              <h2 className="font-headline-lg text-2xl font-bold text-on-surface">System Access</h2>
              <p className="text-xs font-mono text-on-surface-variant uppercase tracking-wider">
                Select your role to enter the secure environment
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {roles.map(r => {
                const IconComp = r.icon;
                return (
                  <button
                    key={r.id}
                    onClick={() => handleRoleLogin(r.id)}
                    className={`group w-full bg-surface-container-high rounded-2xl p-5 flex items-center gap-4 text-left transition-all hover:bg-surface-container-highest active:scale-[0.98] border-l-4 ${r.color} border-y border-r border-outline-variant/20 shadow-lg`}
                  >
                    <div className={`w-14 h-14 rounded-xl ${r.iconBg} flex items-center justify-center flex-shrink-0`}>
                      <IconComp size={28} />
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="font-headline-md text-lg font-bold text-on-surface group-hover:text-primary transition-colors">
                        {r.label}
                      </div>
                      <div className="font-mono text-xs text-on-surface-variant mt-0.5">
                        {r.desc}
                      </div>
                    </div>

                    <ChevronRight size={20} className="text-on-surface-variant group-hover:translate-x-1 transition-transform" />
                  </button>
                );
              })}
            </div>

            <div className="p-4 rounded-xl bg-surface-container-highest flex items-center justify-between border border-outline-variant/20 text-xs font-mono">
              <div className="flex items-center gap-2">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-tertiary opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-tertiary"></span>
                </span>
                <span className="text-on-surface font-bold">GeoAgentic Node v4.2.0</span>
              </div>
              <div className="text-tertiary font-bold uppercase">Systems Operational</div>
            </div>
          </section>

        </div>
      </main>

      {/* Citizen Credentials Modal */}
      {showCitModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-surface-container p-6 rounded-2xl border border-tertiary/40 max-w-md w-full space-y-4 shadow-2xl">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <Shield className="text-tertiary" size={24} />
                <div>
                  <h3 className="text-lg font-bold text-on-surface">Citizen Safety Login</h3>
                  <p className="text-xs text-on-surface-variant">Enter your account credentials to store traversal history</p>
                </div>
              </div>
              <button onClick={() => setShowCitModal(false)} className="text-on-surface-variant hover:text-on-surface font-bold text-sm">X</button>
            </div>

            <div className="space-y-2">
              <span className="text-xs font-mono text-tertiary font-bold block uppercase">Select Registered Citizen Account</span>
              {sampleCitizens.map((c, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setShowCitModal(false);
                    handleRoleLogin('citizen', c);
                  }}
                  className="w-full p-3 bg-surface-container-high hover:bg-tertiary/20 rounded-xl border border-outline-variant/20 hover:border-tertiary text-left text-xs font-bold transition-all flex justify-between items-center"
                >
                  <div>
                    <div className="text-on-surface text-sm">{c.name}</div>
                    <div className="text-on-surface-variant text-[11px] font-mono">{c.phone}</div>
                  </div>
                  <span className="text-tertiary font-mono text-xs font-bold">LOGIN &rarr;</span>
                </button>
              ))}
            </div>

            <div className="pt-2 border-t border-outline-variant/20 space-y-3">
              <span className="text-xs font-mono text-on-surface-variant font-bold block uppercase">Or Enter Custom Credentials</span>
              <input
                type="text"
                placeholder="Full Name (e.g. Ramesh Kumar)"
                value={customCitName}
                onChange={(e) => setCustomCitName(e.target.value)}
                className="w-full bg-surface-container-low border border-outline-variant/30 text-on-surface p-2.5 rounded-xl text-xs focus:outline-none focus:border-tertiary"
              />
              <input
                type="text"
                placeholder="Phone Number (e.g. +91 98765 00000)"
                value={customCitPhone}
                onChange={(e) => setCustomCitPhone(e.target.value)}
                className="w-full bg-surface-container-low border border-outline-variant/30 text-on-surface p-2.5 rounded-xl text-xs focus:outline-none focus:border-tertiary"
              />
              <button
                onClick={() => {
                  if (!customCitName.trim()) return;
                  setShowCitModal(false);
                  handleRoleLogin('citizen', { name: customCitName, phone: customCitPhone || '+91 98765 00000' });
                }}
                className="w-full bg-tertiary text-on-tertiary font-bold py-3 rounded-xl text-xs shadow-lg hover:bg-tertiary/90 transition-all"
              >
                LOG IN AS CUSTOM CITIZEN
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Hospital Selection Modal */}
      {showHospModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-surface-container p-6 rounded-2xl border border-outline-variant/30 max-w-md w-full space-y-4 shadow-2xl">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-lg font-bold text-on-surface">Select Hospital ER Credentials</h3>
                <p className="text-xs text-on-surface-variant">Pick a hospital to log into its dedicated ER Desk</p>
              </div>
              <button onClick={() => setShowHospModal(false)} className="text-on-surface-variant hover:text-on-surface font-bold text-sm">X</button>
            </div>

            <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
              {bangaloreHospitals.map(h => (
                <button
                  key={h.id}
                  onClick={() => {
                    setShowHospModal(false);
                    handleRoleLogin('hospital', h);
                  }}
                  className="w-full p-3 bg-surface-container-high hover:bg-primary-container/20 rounded-xl border border-outline-variant/20 hover:border-primary text-left text-xs font-bold transition-all flex justify-between items-center"
                >
                  <span>{h.name}</span>
                  <span className="text-[10px] text-primary font-mono font-bold">LOGIN &rarr;</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
"""

with open(login_file, "w", encoding="utf-8") as f:
    f.write(new_login_jsx)

print("Login.jsx updated with Citizen Credentials modal and fixed hospital routing")

import sys

login_file = "src/views/Login.jsx"

new_login = """import React, { useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { Shield, Activity, Truck, PlusSquare, ChevronRight, Zap, Hub, Lock, HeartHandshake } from 'lucide-react';

export default function Login() {
  const { login } = useAuth();
  const systemAccessRef = useRef(null);

  const scrollToSystemAccess = () => {
    systemAccessRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const roles = [
    {
      id: 'citizen',
      label: 'Citizen',
      desc: 'Login as citizen_demo',
      icon: Shield,
      color: 'border-tertiary',
      iconBg: 'bg-tertiary/10 text-tertiary',
    },
    {
      id: 'dispatcher',
      label: 'Dispatcher',
      desc: 'Login as dispatcher_demo',
      icon: Activity,
      color: 'border-primary',
      iconBg: 'bg-primary/10 text-primary',
    },
    {
      id: 'driver',
      label: 'Paramedic / Driver',
      desc: 'Login as driver_demo',
      icon: Truck,
      color: 'border-[#FFB900]',
      iconBg: 'bg-[#FFB900]/10 text-[#FFB900]',
    },
    {
      id: 'hospital',
      label: 'Hospital ER Desk',
      desc: 'Login as hospital_demo',
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
            className="text-xs font-mono font-bold bg-surface-container-highest px-3 py-1.5 rounded-full border border-outline-variant/30 text-on-surface-variant hover:text-on-surface transition-colors"
          >
            SELECT ROLE
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 w-full pt-16 bg-surface flex flex-col items-center">
        <div className="w-full max-w-4xl flex flex-col">
          
          {/* Hero Section */}
          <section className="relative px-6 py-16 overflow-hidden text-center flex flex-col items-center gap-6">
            {/* Ambient Background Animation */}
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
                onClick={scrollToSystemAccess}
                className="h-14 px-8 bg-primary text-on-primary font-bold text-base rounded-full shadow-[0_4px_16px_rgba(255,84,81,0.4)] active:translate-y-0.5 transition-all flex items-center gap-2 hover:bg-primary/90"
              >
                <HeartHandshake size={20} />
                Get Started
              </button>
            </div>
          </section>

          {/* Value Propositions */}
          <section className="px-6 py-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Card 1 */}
              <div className="bg-surface-container p-6 rounded-2xl border border-outline-variant/20 flex flex-col gap-3 shadow-md hover:border-outline-variant/40 transition-colors">
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

              {/* Card 2 */}
              <div className="bg-surface-container p-6 rounded-2xl border border-outline-variant/20 flex flex-col gap-3 shadow-md hover:border-outline-variant/40 transition-colors">
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

              {/* Card 3 */}
              <div className="bg-surface-container p-6 rounded-2xl border border-outline-variant/20 flex flex-col gap-3 shadow-md hover:border-outline-variant/40 transition-colors">
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
                    onClick={() => login(r.id)}
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

            {/* System Status Footer */}
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
    </div>
  );
}
"""

with open(login_file, "w", encoding="utf-8") as f:
    f.write(new_login)

print("Login.jsx updated successfully with the hero design and role access dashboard")

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Zap, Heart, Shield, Activity, Truck, PlusSquare, ChevronRight, 
  Sparkles, CheckCircle2, ArrowRight, Radio, Cpu, Clock, 
  ShieldAlert, Navigation, RefreshCw, BarChart3, Lock
} from 'lucide-react';

export default function LandingPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [activeFeatureTab, setActiveFeatureTab] = useState('routing');
  const [activeModalRole, setActiveModalRole] = useState(null);

  const [simStep, setSimStep] = useState(0);
  const simSteps = [
    { title: "Citizen SOS Received", subtitle: "GPS: 12.9756°N, 77.6068°E", status: "PROCESSING", agent: "Accessibility Agent" },
    { title: "Emergency Classified", subtitle: "Cardiac / Trauma — Severity: 88%", status: "CLASSIFIED", agent: "Emergency Coordinator" },
    { title: "Nearest Hub Located", subtitle: "Aster Ambulance Hub (1.8km away)", status: "COMPUTED", agent: "Route Optimization Agent" },
    { title: "Hospital ER Selected", subtitle: "Aster CMI — 12 ICU Beds Ready", status: "MATCHED", agent: "Hospital Intelligence Agent" },
    { title: "5-Factor AI Plan Fused", subtitle: "Overall Confidence Score: 96.4%", status: "READY", agent: "Decision Fusion Engine" }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setSimStep((prev) => (prev + 1) % simSteps.length);
    }, 2800);
    return () => clearInterval(timer);
  }, [simSteps.length]);

  const emergencyDriverUnits = [
    { unitId: 'AMB-UNIT-04', vehicleType: 'Ambulance', driverName: 'Suresh Kumar', hubName: 'Aster CMI Emergency Ambulance Hub', phone: '+91 98765 43210' },
    { unitId: 'AMB-UNIT-01', vehicleType: 'Ambulance', driverName: 'Ramesh Gowda', hubName: 'Manipal Ambulance Base Depot', phone: '+91 98765 43211' },
    { unitId: 'FIRE-UNIT-09', vehicleType: 'Fire Engine', driverName: 'Capt. Rajesh Rao', hubName: 'Hebbal Fire & Rescue Station #4', phone: '+91 98765 43220' },
    { unitId: 'POLICE-UNIT-02', vehicleType: 'Police Cruiser', driverName: 'Insp. Vikram Singh', hubName: 'Hebbal Police Patrol Base', phone: '+91 98765 43230' }
  ];

  const bangaloreHospitals = [
    { id: 'blr-007', name: 'Aster CMI Hospital (Hebbal)' },
    { id: 'blr-001', name: 'Manipal Hospital (Old Airport Road)' },
    { id: 'blr-002', name: 'Fortis Hospital (Bannerghatta Road)' },
    { id: 'blr-003', name: 'Apollo Hospital (Bannerghatta Road)' },
    { id: 'medstar', name: 'MEDSTAR Speciality Hospital' }
  ];

  const handleRoleLaunch = (roleId, extraData = null) => {
    if ((roleId === 'driver' || roleId === 'hospital' || roleId === 'citizen') && !extraData) {
      setActiveModalRole(roleId);
      return;
    }
    login(roleId, extraData);
    navigate(`/${roleId}`);
  };

  const agentsList = [
    { name: "Traffic Intelligence Agent", desc: "Monitors road segment congestion, incidents & weather risks in real time.", icon: Activity },
    { name: "Route Optimization Agent", desc: "Calls Google Routes API v2 for live 2-Phase turn-by-turn routing.", icon: Navigation },
    { name: "Hospital Intelligence Agent", desc: "Ranks hospitals using weighted multi-factor ICU & specialty criteria.", icon: PlusSquare },
    { name: "Decision Fusion Engine", desc: "Fuses agent outputs into explainable action plans with factor scores.", icon: Cpu },
    { name: "Prediction Agent", desc: "Estimates ETAs with weather risk factors and confidence intervals.", icon: Clock },
    { name: "Accessibility Agent", desc: "Normalizes multi-modal SOS reports (text, voice, SOS button, sign).", icon: Shield },
    { name: "Communication Agent", desc: "Manages multi-channel WebSocket & SMS notifications across units.", icon: Radio },
    { name: "Emergency Coordinator", desc: "Assesses severity and assigns required vehicle dispatch requirements.", icon: ShieldAlert },
    { name: "Learning Agent", desc: "Logs historical response metrics for continuous performance optimization.", icon: BarChart3 }
  ];

  return (
    <div className="bg-[#ece5f0] text-[#012622] font-body min-h-screen selection:bg-[#e98a15]/20">
      
      {/* 1. TOP STICKY GLASS NAVIGATION BAR */}
      <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-xl border-b border-[#dcd3e3] shadow-elevation-sm">
        <div className="max-w-7xl mx-auto h-20 px-6 flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-11 h-11 rounded-2xl bg-[#012622] text-[#e98a15] flex items-center justify-center shadow-elevation-sm hover:rotate-6 transition-transform">
              <Zap size={24} className="fill-current text-[#e98a15]" />
            </div>
            <div>
              <span className="font-display text-2xl font-extrabold text-[#012622] tracking-tight block leading-none">RapidGrid</span>
              <span className="text-[10px] font-mono font-bold text-[#e98a15] uppercase tracking-wider block mt-1">Autonomous Emergency AI</span>
            </div>
          </div>

          {/* Center Links */}
          <nav className="hidden md:flex items-center gap-8 text-xs font-mono font-bold text-[#003b36]">
            <a href="#features" className="hover:text-[#e98a15] transition-colors">FEATURES</a>
            <a href="#architecture" className="hover:text-[#e98a15] transition-colors">9-AGENT AI</a>
            <a href="#portals" className="hover:text-[#e98a15] transition-colors">ROLE PORTALS</a>
            <a href="#demo" className="hover:text-[#e98a15] transition-colors">LIVE DEMO</a>
          </nav>

          {/* Live Node Badge & Action Button */}
          <div className="flex items-center gap-4">
            <div className="hidden lg:flex items-center gap-2 bg-[#fdf3e7] border border-[#e98a15]/50 text-[#e98a15] px-3.5 py-1.5 rounded-full text-xs font-mono font-bold shadow-sm">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#e98a15] opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#e98a15]"></span>
              </span>
              <span>9/9 AGENTS ONLINE</span>
            </div>

            <a
              href="#portals"
              className="px-5 py-2.5 bg-[#012622] hover:bg-[#003b36] text-white font-display font-bold text-xs rounded-full shadow-elevation-sm hover:shadow-evergreen-glow active:scale-95 transition-all flex items-center gap-2"
            >
              <span>LAUNCH PORTAL</span>
              <ArrowRight size={14} className="text-[#e98a15]" />
            </a>
          </div>
        </div>
      </header>

      {/* 2. HERO SECTION WITH LIVE TELEMETRY SIMULATOR */}
      <section className="relative pt-16 pb-24 overflow-hidden">
        {/* Subtle Ambient Light Glows */}
        <div className="absolute top-10 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-[#e6f0ef] rounded-full blur-3xl opacity-70 pointer-events-none -z-10"></div>
        <div className="absolute top-40 right-10 w-96 h-96 bg-[#fdf3e7] rounded-full blur-3xl opacity-60 pointer-events-none -z-10"></div>

        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Column — Thesis & Hero CTAs */}
          <div className="lg:col-span-7 space-y-6 text-left">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-[#012622]/20 text-[#012622] text-xs font-bold font-mono shadow-elevation-sm">
              <Sparkles size={14} className="text-[#e98a15]" />
              <span>Next-Generation Autonomous AI Emergency Response</span>
            </div>

            <h1 className="font-display text-4xl sm:text-6xl font-extrabold text-[#012622] tracking-tight leading-[1.1]">
              Seconds Save Lives. <br />
              <span className="bg-gradient-to-r from-[#012622] via-[#003b36] to-[#e98a15] bg-clip-text text-transparent">
                Autonomous AI Coordinates the Grid.
              </span>
            </h1>

            <p className="text-[#003b36] text-base sm:text-lg leading-relaxed max-w-2xl font-body font-medium">
              RapidGrid connects citizens, city dispatchers, paramedic responders, and hospital ER desks into a single synchronized grid. Featuring 2-Phase station hub routing, live Uber-style hospital rerouting, and 9 specialized AI micro-agents.
            </p>

            <div className="flex flex-wrap gap-4 pt-2">
              <button
                onClick={() => handleRoleLaunch('citizen')}
                className="h-14 px-8 bg-[#012622] hover:bg-[#003b36] text-white font-display font-extrabold text-sm rounded-full shadow-elevation-md hover:shadow-amber-glow active:scale-95 transition-all flex items-center gap-3"
              >
                <Heart size={20} className="fill-current text-[#e98a15]" />
                <span>Launch Citizen SOS App</span>
              </button>

              <a
                href="#portals"
                className="h-14 px-8 bg-white hover:bg-[#f4eff7] text-[#012622] font-display font-bold text-sm rounded-full border border-[#dcd3e3] shadow-elevation-sm active:scale-95 transition-all flex items-center gap-2"
              >
                <span>Select Role Portal</span>
                <ChevronRight size={18} className="text-[#e98a15]" />
              </a>
            </div>

            {/* Quick Metrics Line */}
            <div className="grid grid-cols-3 gap-6 pt-6 border-t border-[#dcd3e3]">
              <div>
                <div className="font-display text-2xl font-extrabold text-[#012622]">&lt; 1.2s</div>
                <div className="text-xs font-mono text-[#003b36] mt-0.5">AI Dispatch Fusion Time</div>
              </div>
              <div>
                <div className="font-display text-2xl font-extrabold text-[#e98a15]">96.4%</div>
                <div className="text-xs font-mono text-[#003b36] mt-0.5">Hospital Match Accuracy</div>
              </div>
              <div>
                <div className="font-display text-2xl font-extrabold text-[#012622]">0ms</div>
                <div className="text-xs font-mono text-[#003b36] mt-0.5">WebSocket Live Latency</div>
              </div>
            </div>
          </div>

          {/* Right Column — Live Telemetry Simulator Card */}
          <div className="lg:col-span-5">
            <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-lg relative overflow-hidden">
              {/* Header Bar */}
              <div className="flex justify-between items-center pb-4 border-b border-[#dcd3e3]">
                <div className="flex items-center gap-2.5">
                  <div className="w-3 h-3 rounded-full bg-[#e98a15] animate-ping"></div>
                  <span className="font-mono text-xs font-bold text-[#012622] uppercase tracking-wider">Live AI Pipeline Simulation</span>
                </div>
                <span className="text-[10px] font-mono px-2.5 py-1 rounded-full bg-[#fdf3e7] text-[#e98a15] font-bold border border-[#e98a15]/30">
                  STEP {simStep + 1} OF 5
                </span>
              </div>

              {/* Simulation Content */}
              <div className="py-6 space-y-4">
                <div className="flex items-center gap-4 bg-[#ece5f0]/60 p-4 rounded-2xl border border-[#dcd3e3]">
                  <div className="w-12 h-12 rounded-xl bg-[#012622] text-[#e98a15] flex items-center justify-center flex-shrink-0 shadow-md">
                    <Cpu size={24} />
                  </div>
                  <div>
                    <span className="text-[10px] font-mono font-bold text-[#e98a15] uppercase block">
                      Active Agent: {simSteps[simStep].agent}
                    </span>
                    <h3 className="font-display text-base font-bold text-[#012622]">
                      {simSteps[simStep].title}
                    </h3>
                    <p className="text-xs font-mono text-[#003b36] mt-0.5">
                      {simSteps[simStep].subtitle}
                    </p>
                  </div>
                </div>

                {/* Step Progress Bar */}
                <div className="space-y-1.5">
                  <div className="flex justify-between text-[11px] font-mono font-bold text-[#003b36]">
                    <span>Pipeline Progress</span>
                    <span className="text-[#e98a15]">{Math.round(((simStep + 1) / simSteps.length) * 100)}%</span>
                  </div>
                  <div className="w-full h-2 bg-[#ece5f0] rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-[#012622] transition-all duration-700 ease-out rounded-full"
                      style={{ width: `${((simStep + 1) / simSteps.length) * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              {/* Footer Indicator */}
              <div className="pt-3 border-t border-[#dcd3e3] flex justify-between items-center text-xs font-mono">
                <span className="text-[#003b36] flex items-center gap-1.5">
                  <Lock size={12} className="text-[#e98a15]" />
                  <span>256-Bit Encrypted Data Bus</span>
                </span>
                <button
                  onClick={() => setSimStep((prev) => (prev + 1) % simSteps.length)}
                  className="text-[#012622] font-bold hover:text-[#e98a15] flex items-center gap-1 transition-colors"
                >
                  <RefreshCw size={12} /> Next Step
                </button>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* 3. INTERACTIVE 2-PHASE HUB ROUTING & LIVE REROUTING FEATURE SHOWCASE */}
      <section id="features" className="py-20 bg-white border-y border-[#dcd3e3]">
        <div className="max-w-7xl mx-auto px-6 space-y-12">
          
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <span className="text-xs font-mono font-bold text-[#e98a15] uppercase tracking-wider px-3 py-1 rounded-full bg-[#fdf3e7] border border-[#e98a15]/30">
              Core Architectural Innovations
            </span>
            <h2 className="font-display text-3xl sm:text-4xl font-extrabold text-[#012622]">
              Designed for High-Stakes Emergency Mobility
            </h2>
            <p className="text-sm text-[#003b36] leading-relaxed">
              Standard GPS apps compute single point-to-point lines. RapidGrid introduces 2-Phase hub routing and live Uber-style hospital rerouting.
            </p>
          </div>

          {/* Feature Selector Tabs */}
          <div className="flex justify-center gap-3">
            {[
              { id: 'routing', label: '2-Phase Station Hub Routing', icon: Navigation },
              { id: 'reroute', label: 'Uber-Style Live Hospital Reroute', icon: RefreshCw },
              { id: 'fusion', label: '5-Factor AI Decision Fusion', icon: Cpu }
            ].map(tab => {
              const IconComp = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveFeatureTab(tab.id)}
                  className={`px-5 py-3 rounded-2xl text-xs font-mono font-bold transition-all flex items-center gap-2 border ${
                    activeFeatureTab === tab.id
                      ? 'bg-[#012622] text-[#e98a15] border-[#012622] shadow-elevation-sm'
                      : 'bg-[#ece5f0] text-[#003b36] border-[#dcd3e3] hover:border-[#012622]/40'
                  }`}
                >
                  <IconComp size={16} />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>

          {/* Feature Tab Content Display */}
          <div className="bg-[#ece5f0] p-8 rounded-3xl border border-[#dcd3e3] shadow-elevation-md">
            {activeFeatureTab === 'routing' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                <div className="space-y-4">
                  <div className="w-10 h-10 rounded-xl bg-[#012622] text-[#e98a15] flex items-center justify-center font-bold">
                    1
                  </div>
                  <h3 className="font-display text-2xl font-bold text-[#012622]">2-Phase Station Hub Routing Engine</h3>
                  <p className="text-sm text-[#003b36] leading-relaxed">
                    Emergency response happens in two distinct physical phases. RapidGrid models both independently:
                  </p>
                  <div className="space-y-3 font-mono text-xs">
                    <div className="p-4 rounded-2xl bg-white border border-[#dcd3e3] space-y-1">
                      <div className="text-[#012622] font-bold flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-[#e98a15]"></span>
                        PHASE 1: STATION HUB BASE &rarr; CITIZEN PICKUP
                      </div>
                      <p className="text-[#003b36]">Finds nearest service hub (Aster Ambulance Hub, Hebbal Fire Station #4, etc.) and computes response traversal.</p>
                    </div>

                    <div className="p-4 rounded-2xl bg-white border border-[#dcd3e3] space-y-1">
                      <div className="text-[#012622] font-bold flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-[#012622]"></span>
                        PHASE 2: CITIZEN PICKUP &rarr; DESTINATION HOSPITAL ER
                      </div>
                      <p className="text-[#003b36]">Computes live traffic-aware shortest path from patient location to selected hospital ER entrance.</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm space-y-4 text-center">
                  <div className="font-mono text-xs font-bold text-[#012622] uppercase tracking-wider">Live Route Polylines Visualizer</div>
                  <div className="h-56 rounded-2xl bg-[#ece5f0] border border-[#dcd3e3] flex flex-col items-center justify-center p-6 space-y-3">
                    <div className="flex items-center gap-3">
                      <span className="px-3 py-1 rounded-full bg-[#fdf3e7] text-[#e98a15] text-xs font-mono font-bold border border-[#e98a15]/30">Phase 1: Dotted Amber</span>
                      <span className="px-3 py-1 rounded-full bg-white text-[#012622] text-xs font-mono font-bold border border-[#012622]/30">Phase 2: Solid Evergreen</span>
                    </div>
                    <p className="text-xs text-[#003b36]">Renders real-time turn-by-turn coordinates directly on Leaflet maps across Citizen, Driver, and Dispatcher screens.</p>
                  </div>
                </div>
              </div>
            )}

            {activeFeatureTab === 'reroute' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                <div className="space-y-4">
                  <div className="w-10 h-10 rounded-xl bg-[#012622] text-[#e98a15] flex items-center justify-center font-bold">
                    2
                  </div>
                  <h3 className="font-display text-2xl font-bold text-[#012622]">Uber-Style Live Hospital Rerouting</h3>
                  <p className="text-sm text-[#003b36] leading-relaxed">
                    First responder field paramedics can change the destination hospital on the fly. RapidGrid recomputes the route via Google Routes API and instantly updates both Driver and Citizen screens in real time.
                  </p>
                  <ul className="space-y-2 text-xs font-mono text-[#003b36]">
                    <li className="flex items-center gap-2">
                      <CheckCircle2 size={16} className="text-[#e98a15]" />
                      <span>Instant Google Routes API recomputation in &lt; 400ms</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle2 size={16} className="text-[#e98a15]" />
                      <span>Real-time WebSockets synchronization across all devices</span>
                    </li>
                  </ul>
                </div>

                <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm space-y-4">
                  <div className="font-mono text-xs font-bold text-[#012622] uppercase tracking-wider">Driver Hospital Selection UI</div>
                  <div className="p-4 bg-[#ece5f0] rounded-2xl border border-[#dcd3e3] space-y-2 font-mono text-xs">
                    <span className="text-[#003b36] font-bold block">SELECT NEW DESTINATION HOSPITAL:</span>
                    <div className="p-3 bg-white rounded-xl border border-[#e98a15] font-bold text-[#012622]">
                      Aster CMI Hospital (Hebbal) — 12 ICU Beds
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeFeatureTab === 'fusion' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                <div className="space-y-4">
                  <div className="w-10 h-10 rounded-xl bg-[#012622] text-[#e98a15] flex items-center justify-center font-bold">
                    3
                  </div>
                  <h3 className="font-display text-2xl font-bold text-[#012622]">5-Dimension Explainable Decision Fusion</h3>
                  <p className="text-sm text-[#003b36] leading-relaxed">
                    No black boxes. The Decision Fusion Engine calculates weighted scores across 5 distinct dimensions and provides plain-language explanations for city dispatchers.
                  </p>
                  <div className="grid grid-cols-2 gap-3 text-xs font-mono font-bold">
                    <div className="p-3 bg-white rounded-xl border border-[#dcd3e3] text-[#012622]">1. Response Time (ETA)</div>
                    <div className="p-3 bg-white rounded-xl border border-[#dcd3e3] text-[#012622]">2. Live Traffic Congestion</div>
                    <div className="p-3 bg-white rounded-xl border border-[#dcd3e3] text-[#012622]">3. Hospital ICU Readiness</div>
                    <div className="p-3 bg-white rounded-xl border border-[#dcd3e3] text-[#012622]">4. Emergency Severity</div>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm space-y-3">
                  <div className="font-mono text-xs font-bold text-[#012622] uppercase">AI Explanation Output</div>
                  <p className="text-xs text-[#003b36] italic bg-[#ece5f0] p-4 rounded-2xl border border-[#dcd3e3] leading-relaxed">
                    "Action plan for incident INC-8492 (cardiac emergency, critical severity). ROUTE: Primary route via Google Maps Live Traffic. ETA: 420s. HOSPITAL: Aster CMI selected (score 0.94). Decision driven primarily by Hospital Availability and Response Time."
                  </p>
                </div>
              </div>
            )}
          </div>

        </div>
      </section>

      {/* 4. 9-AGENT AUTONOMOUS AI ARCHITECTURE SHOWCASE */}
      <section id="architecture" className="py-20 max-w-7xl mx-auto px-6 space-y-12">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-xs font-mono font-bold text-[#e98a15] uppercase tracking-wider px-3 py-1 rounded-full bg-[#fdf3e7] border border-[#e98a15]/30">
            Decoupled Micro-Agent Network
          </span>
          <h2 className="font-display text-3xl sm:text-4xl font-extrabold text-[#012622]">
            9 Autonomous AI Micro-Agents
          </h2>
          <p className="text-sm text-[#003b36] leading-relaxed">
            Operating over an async in-process Event Bus (`EventBus`), keeping agents independently testable and deployable.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {agentsList.map((ag, idx) => {
            const IconComp = ag.icon;
            return (
              <div 
                key={idx}
                className="bg-white p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm hover:shadow-elevation-md transition-all space-y-3 group hover:border-[#012622]"
              >
                <div className="w-12 h-12 rounded-2xl bg-[#012622] text-[#e98a15] flex items-center justify-center transition-all shadow-sm">
                  <IconComp size={22} />
                </div>
                <h3 className="font-display text-base font-bold text-[#012622] group-hover:text-[#e98a15] transition-colors">
                  {ag.name}
                </h3>
                <p className="text-xs text-[#003b36] leading-relaxed">
                  {ag.desc}
                </p>
                <div className="pt-2 flex justify-between items-center text-[10px] font-mono text-[#e98a15] font-bold">
                  <span className="flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#e98a15] animate-pulse"></span>
                    ACTIVE
                  </span>
                  <span className="text-[#003b36]">PUB/SUB BUS</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* 5. ROLE-BASED PORTALS SHOWCASE */}
      <section id="portals" className="py-20 bg-white border-t border-[#dcd3e3]">
        <div className="max-w-7xl mx-auto px-6 space-y-12">
          
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <span className="text-xs font-mono font-bold text-[#e98a15] uppercase tracking-wider px-3 py-1 rounded-full bg-[#fdf3e7] border border-[#e98a15]/30">
              Unified Role Access
            </span>
            <h2 className="font-display text-3xl sm:text-4xl font-extrabold text-[#012622]">
              Select Your Role Portal
            </h2>
            <p className="text-sm text-[#003b36] leading-relaxed">
              Launch directly into any of the 4 synchronized role interfaces.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            {/* Citizen App */}
            <div className="bg-[#ece5f0] p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm hover:shadow-elevation-md transition-all flex flex-col justify-between space-y-6">
              <div className="space-y-4">
                <div className="w-14 h-14 rounded-2xl bg-[#012622] text-[#e98a15] flex items-center justify-center shadow-md">
                  <Heart size={28} className="fill-current" />
                </div>
                <div>
                  <span className="text-[10px] font-mono font-bold text-[#e98a15] uppercase">PORTAL 01</span>
                  <h3 className="font-display text-xl font-bold text-[#012622]">Citizen Mobile PWA</h3>
                  <p className="text-xs text-[#003b36] mt-1 leading-relaxed">
                    One-tap SOS triggers, 2-phase map tracking, paramedic standby backup request, and direct chat.
                  </p>
                </div>
              </div>

              <button
                onClick={() => handleRoleLaunch('citizen')}
                className="w-full py-3.5 bg-[#012622] hover:bg-[#003b36] text-white font-bold font-mono text-xs rounded-2xl shadow-elevation-sm transition-all flex items-center justify-center gap-2 active:scale-95"
              >
                <span>ENTER CITIZEN APP</span>
                <ArrowRight size={14} className="text-[#e98a15]" />
              </button>
            </div>

            {/* City Dispatch Control */}
            <div className="bg-[#ece5f0] p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm hover:shadow-elevation-md transition-all flex flex-col justify-between space-y-6">
              <div className="space-y-4">
                <div className="w-14 h-14 rounded-2xl bg-[#012622] text-[#e98a15] flex items-center justify-center shadow-md">
                  <Activity size={28} />
                </div>
                <div>
                  <span className="text-[10px] font-mono font-bold text-[#e98a15] uppercase">PORTAL 02</span>
                  <h3 className="font-display text-xl font-bold text-[#012622]">City Dispatch Control</h3>
                  <p className="text-xs text-[#003b36] mt-1 leading-relaxed">
                    Real-time incident queue, explainable AI Decision Rationale breakdown, and manual hospital override.
                  </p>
                </div>
              </div>

              <button
                onClick={() => handleRoleLaunch('dispatcher')}
                className="w-full py-3.5 bg-[#012622] hover:bg-[#003b36] text-white font-bold font-mono text-xs rounded-2xl shadow-elevation-sm transition-all flex items-center justify-center gap-2 active:scale-95"
              >
                <span>ENTER DISPATCH CONTROL</span>
                <ArrowRight size={14} className="text-[#e98a15]" />
              </button>
            </div>

            {/* Paramedic Driver Field App */}
            <div className="bg-[#ece5f0] p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm hover:shadow-elevation-md transition-all flex flex-col justify-between space-y-6">
              <div className="space-y-4">
                <div className="w-14 h-14 rounded-2xl bg-[#012622] text-[#e98a15] flex items-center justify-center shadow-md">
                  <Truck size={28} />
                </div>
                <div>
                  <span className="text-[10px] font-mono font-bold text-[#e98a15] uppercase">PORTAL 03</span>
                  <h3 className="font-display text-xl font-bold text-[#012622]">Paramedic Field Unit</h3>
                  <p className="text-xs text-[#003b36] mt-1 leading-relaxed">
                    2-Stage navigation workflow, hub logins, Uber-style live hospital rerouting dropdown, and direct chat.
                  </p>
                </div>
              </div>

              <button
                onClick={() => handleRoleLaunch('driver')}
                className="w-full py-3.5 bg-[#012622] hover:bg-[#003b36] text-white font-bold font-mono text-xs rounded-2xl shadow-elevation-sm transition-all flex items-center justify-center gap-2 active:scale-95"
              >
                <span>ENTER PARAMEDIC APP</span>
                <ArrowRight size={14} className="text-[#e98a15]" />
              </button>
            </div>

            {/* Hospital ER Terminal */}
            <div className="bg-[#ece5f0] p-6 rounded-3xl border border-[#dcd3e3] shadow-elevation-sm hover:shadow-elevation-md transition-all flex flex-col justify-between space-y-6">
              <div className="space-y-4">
                <div className="w-14 h-14 rounded-2xl bg-[#012622] text-[#e98a15] flex items-center justify-center shadow-md">
                  <PlusSquare size={28} />
                </div>
                <div>
                  <span className="text-[10px] font-mono font-bold text-[#e98a15] uppercase">PORTAL 04</span>
                  <h3 className="font-display text-xl font-bold text-[#012622]">Hospital ER Terminal</h3>
                  <p className="text-xs text-[#003b36] mt-1 leading-relaxed">
                    Dedicated hospital ER desk logins, bed capacity management, incoming triage queue, and direct paramedic chat.
                  </p>
                </div>
              </div>

              <button
                onClick={() => handleRoleLaunch('hospital')}
                className="w-full py-3.5 bg-[#012622] hover:bg-[#003b36] text-white font-bold font-mono text-xs rounded-2xl shadow-elevation-sm transition-all flex items-center justify-center gap-2 active:scale-95"
              >
                <span>ENTER HOSPITAL TERMINAL</span>
                <ArrowRight size={14} className="text-[#e98a15]" />
              </button>
            </div>

          </div>
        </div>
      </section>

      {/* 6. FOOTER */}
      <footer className="py-12 bg-[#012622] text-white border-t border-[#003b36]">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-[#003b36] text-[#e98a15] flex items-center justify-center">
              <Zap size={20} className="fill-current text-[#e98a15]" />
            </div>
            <div>
              <span className="font-display text-lg font-extrabold text-white block">RapidGrid</span>
              <span className="text-[10px] font-mono text-[#ece5f0]/80">GeoAgentic AI Emergency System</span>
            </div>
          </div>

          <div className="text-xs font-mono text-[#ece5f0]/80">
            Developed for RapidGrid Autonomous Multi-Agent AI Platform.
          </div>
        </div>
      </footer>

      {/* 7. ROLE SELECTION MODAL */}
      {activeModalRole && (
        <div className="fixed inset-0 z-50 bg-[#012622]/70 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white p-6 rounded-3xl border border-[#dcd3e3] max-w-md w-full space-y-4 shadow-elevation-lg">
            <div className="flex justify-between items-center border-b border-[#dcd3e3] pb-3">
              <h3 className="font-display text-base font-bold text-[#012622]">Select Credentials for {activeModalRole.toUpperCase()}</h3>
              <button onClick={() => setActiveModalRole(null)} className="text-[#003b36] font-bold">✕</button>
            </div>

            {activeModalRole === 'citizen' && (
              <div className="space-y-3">
                <span className="text-xs font-mono text-[#012622] font-bold uppercase block">Select Registered Citizen Profile:</span>
                {[
                  { name: 'Ananya Sharma', phone: '+91 98765 43210' },
                  { name: 'Rahul Verma', phone: '+91 91234 56789' }
                ].map((c, idx) => (
                  <button
                    key={idx}
                    onClick={() => { setActiveModalRole(null); handleRoleLaunch('citizen', c); }}
                    className="w-full p-3 bg-[#ece5f0] hover:bg-[#e6f0ef] rounded-2xl border border-[#dcd3e3] hover:border-[#012622] text-left text-xs font-bold transition-all flex justify-between items-center"
                  >
                    <div>
                      <div className="text-[#012622] text-sm">{c.name}</div>
                      <div className="text-[#003b36] text-[11px] font-mono">{c.phone}</div>
                    </div>
                    <span className="text-[#012622] font-mono text-xs font-bold">LOGIN &rarr;</span>
                  </button>
                ))}
              </div>
            )}

            {activeModalRole === 'driver' && (
              <div className="space-y-3 max-h-60 overflow-y-auto">
                <span className="text-xs font-mono text-[#012622] font-bold uppercase block">Select First Responder Hub Unit:</span>
                {emergencyDriverUnits.map(u => (
                  <button
                    key={u.unitId}
                    onClick={() => { setActiveModalRole(null); handleRoleLaunch('driver', u); }}
                    className="w-full p-3 bg-[#ece5f0] hover:bg-[#e6f0ef] rounded-2xl border border-[#dcd3e3] hover:border-[#012622] text-left text-xs font-mono font-bold transition-all flex justify-between items-center"
                  >
                    <div>
                      <span className="px-2 py-0.5 rounded bg-[#012622] text-[#e98a15] text-xs font-mono">{u.unitId}</span>
                      <div className="text-[#012622] text-xs mt-1">{u.driverName} ({u.hubName})</div>
                    </div>
                    <span className="text-[#012622]">LOGIN &rarr;</span>
                  </button>
                ))}
              </div>
            )}

            {activeModalRole === 'hospital' && (
              <div className="space-y-3 max-h-60 overflow-y-auto">
                <span className="text-xs font-mono text-[#012622] font-bold uppercase block">Select Hospital ER Terminal:</span>
                {bangaloreHospitals.map(h => (
                  <button
                    key={h.id}
                    onClick={() => { setActiveModalRole(null); handleRoleLaunch('hospital', h); }}
                    className="w-full p-3 bg-[#ece5f0] hover:bg-[#e6f0ef] rounded-2xl border border-[#dcd3e3] hover:border-[#012622] text-left text-xs font-bold transition-all flex justify-between items-center"
                  >
                    <span className="text-[#012622]">{h.name}</span>
                    <span className="text-[#012622] font-mono text-xs">LOGIN &rarr;</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  );
}

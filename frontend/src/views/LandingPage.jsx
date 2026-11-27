import React from 'react';
import { Link } from 'react-router-dom';

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-transparent text-[#1a1c1a] font-['Inter',sans-serif]">
      {/* Precision grid overlay */}
      <div
        className="pointer-events-none fixed inset-0 z-0 opacity-40"
        style={{
          backgroundImage: `
            linear-gradient(to right, rgba(26, 28, 26, 0.05) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(26, 28, 26, 0.05) 1px, transparent 1px)
          `,
          backgroundSize: '32px 32px',
        }}
      />
      {/* HEADER */}
      <header className="fixed top-0 w-full z-50 bg-[#131a33] shadow-[0_1px_8px_rgba(0,0,0,0.04)]">
        <div className="h-16 max-w-7xl mx-auto px-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-9 h-9 rounded-lg bg-[#f59e0b] flex items-center justify-center font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
              R
            </div>
            <div className="flex flex-col">
              <span className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-white tracking-tight">
                RapidGrid
              </span>
              <span className="text-[12px] text-[#bec5e5]">
                Bengaluru emergency vehicle dispatch
              </span>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-6">
            <Link
              to="/dispatcher"
              className="px-2 py-1 text-[14px] transition-colors bg-[#f59e0b] text-[#613b00] font-bold rounded-lg"
            >
              Dispatch
            </Link>
            <Link
              to="/seats"
              className="px-2 py-1 text-[14px] font-bold text-[#bec5e5] hover:text-white transition-colors"
            >
              Fleet &amp; Seats
            </Link>
            <Link
              to="/control"
              className="px-2 py-1 text-[14px] font-bold text-[#bec5e5] hover:text-white transition-colors"
            >
              Control Room
            </Link>
          </nav>

          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="px-4 py-2 rounded-lg bg-[#f59e0b] text-[#131a33] font-bold text-[14px] hover:bg-[#ffb95f] hover:text-[#2a1700] transition-colors"
            >
              Sign in
            </Link>
            <Link
              to="/login"
              className="w-8 h-8 rounded-full bg-[#855300] flex items-center justify-center hover:opacity-90"
            >
              <span className="material-symbols-outlined text-white text-[18px]">person</span>
            </Link>
          </div>
        </div>
      </header>

      {/* MAIN BODY */}
      <main className="relative z-10 w-full pt-16 bg-transparent">
        <div className="flex flex-col w-full">
          {/* 1. HERO SECTION */}
          <section className="w-full bg-transparent relative overflow-hidden">
            <div className="absolute top-0 right-0 w-96 h-96 bg-[#f59e0b]/10 rounded-full blur-3xl -mt-16 -mr-16 pointer-events-none"></div>
            <div className="absolute bottom-0 left-0 w-80 h-80 bg-[#d8deff]/40 rounded-full blur-3xl -ml-16 pointer-events-none"></div>
            <div className="max-w-7xl mx-auto px-6 py-8 relative z-10">
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                {/* Left Column */}
                <div className="lg:col-span-6 flex flex-col gap-6 min-w-0">
                  <div className="inline-flex items-center gap-2 self-start px-4 py-1 rounded-lg bg-[#ffdad7] text-[#930013] shadow-xs">
                    <span className="w-2 h-2 rounded-full bg-[#b91a24] animate-pulse"></span>
                    <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider">
                      EMERGENCY VEHICLE MOVEMENT
                    </span>
                  </div>

                  <h1 className="font-['Space_Grotesk',sans-serif] text-[clamp(28px,4.5vw,40px)] font-bold text-[#131a33] leading-tight tracking-tight">
                    It watches the route, so dispatch does not have to guess.
                  </h1>

                  <p className="text-[16px] leading-relaxed text-[#534434]">
                    RapidGrid's monitoring agent follows every unit on a call. When one leaves its
                    route, meets a closed road or slows down, it says why, how late, which way round,
                    and whether to keep that unit or send a closer one, in plain words. It also sends
                    each patient to a hospital that can treat them, not just the nearest.
                  </p>

                  <div className="flex flex-wrap items-center gap-4 pt-1">
                    <Link
                      to="/citizen"
                      className="inline-flex items-center gap-2 px-6 py-4 rounded-lg bg-[#f59e0b] text-[#131a33] font-['Archivo_Narrow',sans-serif] font-bold text-[14px] shadow-md hover:bg-[#ffb95f] hover:shadow-lg transition-all"
                    >
                      <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                        emergency
                      </span>
                      <span>Report an emergency</span>
                    </Link>
                    <Link
                      to="/dispatcher"
                      className="inline-flex items-center gap-2 px-6 py-4 rounded-lg bg-[#131a33] text-white font-['Archivo_Narrow',sans-serif] font-bold text-[14px] shadow-md hover:bg-[#3e4660] transition-all"
                    >
                      <span className="material-symbols-outlined text-[20px]">monitoring</span>
                      <span>Open the dispatch console</span>
                    </Link>
                  </div>

                  <div className="flex flex-wrap items-center gap-4 pt-1 text-[12px] text-[#5a627e]">
                    <Link
                      to="/seats"
                      className="inline-flex items-center gap-1 hover:text-[#855300] transition-colors"
                    >
                      <span className="material-symbols-outlined text-[16px] text-[#f59e0b]">groups</span>
                      <span>Choose your seat (team demo)</span>
                    </Link>
                    <span className="text-[#d8c3ad]">/</span>
                    <Link
                      to="/control"
                      className="inline-flex items-center gap-1 hover:text-[#855300] transition-colors"
                    >
                      <span className="material-symbols-outlined text-[16px] text-[#565d79]">apartment</span>
                      <span>City control room</span>
                    </Link>
                    <span className="text-[#d8c3ad]">/</span>
                    <Link
                      to="/demo"
                      className="inline-flex items-center gap-1 hover:text-[#855300] transition-colors"
                    >
                      <span className="material-symbols-outlined text-[16px] text-[#b91a24]">play_circle</span>
                      <span>Guided demo</span>
                    </Link>
                  </div>
                </div>

                {/* Right Column */}
                <div className="lg:col-span-6 flex flex-col gap-4 min-w-0">
                  <div className="relative rounded-xl overflow-hidden shadow-xl bg-[#131a33]">
                    <img
                      className="w-full h-80 object-cover"
                      alt="Bengaluru live grid active corridor"
                      src="https://lh3.googleusercontent.com/aida-public/AB6AXuDSY3yHPtA3oCxCUHmdxSa6B54fQbi7i7zoH9qVcAdpqkVmZ7-W4fAjFFB5T0PyMpkChCn3IBc5o0mJWMYfuizt1Ih3KlWVFraR8ygwzub8MX7dSj5XcOvbX9F3MuDSmEd20spbmUwj9764r2SEfyd4liCrGgkKPcMoUHTlBQYafIzRqnfE1Aha6qd1BE50CjrMGhs0xULElrYwa34NgezRUE5KfAJAA95bROiVIkA"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#131a33]/80 via-transparent to-transparent pointer-events-none"></div>
                    <div className="absolute top-4 left-4 inline-flex items-center gap-1 px-3 py-1 rounded-lg bg-[#131a33]/90 backdrop-blur-xs text-white shadow-md">
                      <span className="w-2 h-2 rounded-full bg-[#f59e0b] animate-pulse"></span>
                      <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider">
                        BENGALURU LIVE GRID · UNIT KA-01-G-4821
                      </span>
                    </div>
                    <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between gap-2 text-white">
                      <div className="flex flex-col">
                        <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold text-[#ffb95f] uppercase tracking-wider">
                          ACTIVE CORRIDOR
                        </span>
                        <span className="font-['Inter',sans-serif] text-[16px] font-semibold">
                          Hebbal Flyover → Aster CMI
                        </span>
                      </div>
                      <div className="px-3 py-1.5 rounded-lg bg-[#f59e0b] text-[#131a33] font-['JetBrains_Mono',monospace] text-[14px] font-bold">
                        ETA 5.9 MIN
                      </div>
                    </div>
                  </div>

                  {/* What it runs on 4-metric card */}
                  <div className="bg-white rounded-xl p-6 shadow-md border border-[#efeeeb]">
                    <div className="flex items-center justify-between mb-4">
                      <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#534434]">
                        What it runs on
                      </span>
                      <span className="font-['JetBrains_Mono',monospace] text-[14px] font-medium text-[#855300]">
                        BLR-GRAPH v2.4
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-[#f4f3f1] rounded-lg p-4 flex flex-col gap-1">
                        <span className="font-['JetBrains_Mono',monospace] text-[24px] font-bold text-[#131a33]">
                          112,725
                        </span>
                        <span className="text-[12px] text-[#534434]">
                          OSM nodes · 178,089 edges / Bengaluru road graph
                        </span>
                      </div>
                      <div className="bg-[#ffddb8]/40 rounded-lg p-4 flex flex-col gap-1">
                        <span className="font-['JetBrains_Mono',monospace] text-[24px] font-bold text-[#2a1700]">
                          30
                        </span>
                        <span className="text-[12px] text-[#653e00]">
                          Facilities · curated capability profiles, coords via OSM
                        </span>
                      </div>
                      <div className="bg-[#dbe1ff]/50 rounded-lg p-4 flex flex-col gap-1">
                        <span className="font-['JetBrains_Mono',monospace] text-[24px] font-bold text-[#131a33]">
                          6
                        </span>
                        <span className="text-[12px] text-[#3e4660]">
                          Agent steps per alert · observe, detect, explain, predict, options, advise
                        </span>
                      </div>
                      <div className="bg-[#ffdad7]/40 rounded-lg p-4 flex flex-col gap-1">
                        <span className="font-['JetBrains_Mono',monospace] text-[24px] font-bold text-[#410004]">
                          &lt; 2 s
                        </span>
                        <span className="text-[12px] text-[#930013]">
                          Per alert · routes, cause and backup worked out (measured offline)
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 2. HOSPITAL COMPARISON SECTION */}
          <section className="w-full bg-[#f4f3f1] py-8">
            <div className="max-w-7xl mx-auto px-6 flex flex-col gap-6">
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2">
                <div className="flex flex-col gap-1">
                  <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#b91a24]">
                    CAPABILITY-FIRST ROUTING
                  </span>
                  <h2 className="font-['Space_Grotesk',sans-serif] text-[clamp(24px,3.5vw,32px)] font-bold text-[#131a33]">
                    Illustrative comparison · Cardiac · Hebbal, Bengaluru
                  </h2>
                </div>
                <span className="font-['JetBrains_Mono',monospace] text-[14px] text-[#5a627e] bg-white px-4 py-1.5 rounded-lg shadow-xs">
                  CASE: STEMI-04
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Left: Vibrant Signal Amber Card */}
                <div className="bg-[#f59e0b] rounded-xl p-6 shadow-md text-[#131a33] flex flex-col justify-between gap-6">
                  <div className="flex flex-col gap-2">
                    <div className="flex items-center justify-between">
                      <span className="inline-flex items-center gap-1 px-3 py-1 rounded-lg bg-[#131a33] text-white font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider">
                        <span className="material-symbols-outlined text-[14px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                          check_circle
                        </span>
                        Selected
                      </span>
                      <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#613b00]">
                        PRIMARY MATCH
                      </span>
                    </div>
                    <h3 className="font-['Space_Grotesk',sans-serif] text-[24px] font-semibold text-[#131a33] pt-1">
                      Aster CMI Hospital (Hebbal)
                    </h3>
                    <p className="text-[14px] text-[#2a1700]">Compared factor · Cath lab</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4 bg-white/90 rounded-lg p-4">
                    <div className="flex flex-col">
                      <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase text-[#534434]">
                        Score
                      </span>
                      <span className="font-['JetBrains_Mono',monospace] text-[24px] font-bold text-[#131a33]">
                        0.82
                      </span>
                    </div>
                    <div className="flex flex-col">
                      <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase text-[#534434]">
                        Road ETA
                      </span>
                      <span className="font-['JetBrains_Mono',monospace] text-[24px] font-bold text-[#131a33]">
                        5.9 min
                      </span>
                    </div>
                  </div>
                </div>

                {/* Right: Cool Slate/Ice Card */}
                <div className="bg-[#dbe1ff] rounded-xl p-6 shadow-xs text-[#131a33] flex flex-col justify-between gap-6">
                  <div className="flex flex-col gap-2">
                    <div className="flex items-center justify-between">
                      <span className="inline-flex items-center gap-1 px-3 py-1 rounded-lg bg-white text-[#3e4660] font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider">
                        Faster alternative
                      </span>
                      <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#5a627e]">
                        CANDIDATE #2
                      </span>
                    </div>
                    <h3 className="font-['Space_Grotesk',sans-serif] text-[24px] font-semibold text-[#131a33] pt-1">
                      MS Ramaiah Memorial Hospital
                    </h3>
                    <p className="text-[14px] text-[#3e4660]">
                      Alternative candidate · compare capability and travel time
                    </p>
                  </div>
                  <div className="grid grid-cols-2 gap-4 bg-white/90 rounded-lg p-4">
                    <div className="flex flex-col">
                      <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase text-[#534434]">
                        Score
                      </span>
                      <span className="font-['JetBrains_Mono',monospace] text-[24px] font-bold text-[#3e4660]">
                        0.76
                      </span>
                    </div>
                    <div className="flex flex-col">
                      <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase text-[#534434]">
                        Road ETA
                      </span>
                      <span className="font-['JetBrains_Mono',monospace] text-[24px] font-bold text-[#3e4660]">
                        6.4 min
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <p className="text-[12px] text-[#534434] bg-white px-4 py-2.5 rounded-lg shadow-xs border border-[#efeeeb]">
                This recommendation adds 0.5 minutes of estimated travel. The compared capability score
                is one part of the ranking; this is not a record of an ambulance journey.
              </p>
            </div>
          </section>

          {/* 3. CAPABILITIES GRID */}
          <section className="w-full bg-transparent py-8">
            <div className="max-w-7xl mx-auto px-6 flex flex-col gap-6">
              <div className="flex flex-col gap-1">
                <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#855300]">
                  SYSTEM ARCHITECTURE
                </span>
                <h2 className="font-['Space_Grotesk',sans-serif] text-[clamp(24px,3.5vw,32px)] font-bold text-[#131a33]">
                  Built for high-stakes dispatch
                </h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white rounded-xl p-6 shadow-xs hover:shadow-md transition-shadow border border-[#efeeeb] flex flex-col gap-4">
                  <div className="w-11 h-11 rounded-lg bg-[#f59e0b] text-[#131a33] flex items-center justify-center">
                    <span className="material-symbols-outlined text-[24px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                      visibility
                    </span>
                  </div>
                  <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                    An agent watches every unit on its route
                  </h3>
                  <p className="text-[14px] leading-relaxed text-[#534434]">
                    RapidGrid's monitoring agent tracks each active ambulance against its planned path.
                    When a unit slows, detours, or hits a blockage, it explains the cause, estimates
                    the delay, and recommends whether to hold or reassign.
                  </p>
                </div>

                <div className="bg-white rounded-xl p-6 shadow-xs hover:shadow-md transition-shadow border border-[#efeeeb] flex flex-col gap-4">
                  <div className="w-11 h-11 rounded-lg bg-[#ffdad7] text-[#930013] flex items-center justify-center">
                    <span className="material-symbols-outlined text-[24px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                      local_hospital
                    </span>
                  </div>
                  <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                    It routes on capability, not just proximity
                  </h3>
                  <p className="text-[14px] leading-relaxed text-[#534434]">
                    Sending a cardiac or trauma patient to the closest clinic wastes critical minutes.
                    RapidGrid scores 30 Bengaluru facilities on clinical capability, bed readiness, and
                    road ETA so each patient reaches a hospital that can treat them.
                  </p>
                </div>

                <div className="bg-white rounded-xl p-6 shadow-xs hover:shadow-md transition-shadow border border-[#efeeeb] flex flex-col gap-4">
                  <div className="w-11 h-11 rounded-lg bg-[#dbe1ff] text-[#131a33] flex items-center justify-center">
                    <span className="material-symbols-outlined text-[24px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                      hub
                    </span>
                  </div>
                  <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                    Its own road graph, no provider needed
                  </h3>
                  <p className="text-[14px] leading-relaxed text-[#534434]">
                    Built directly on OpenStreetMap's Bengaluru street network (112,725 nodes and
                    178,089 edges), RapidGrid computes turn-by-turn routes, alternate corridors, and
                    backup unit ETAs locally in under two seconds.
                  </p>
                </div>

                <div className="bg-white rounded-xl p-6 shadow-xs hover:shadow-md transition-shadow border border-[#efeeeb] flex flex-col gap-4">
                  <div className="w-11 h-11 rounded-lg bg-[#131a33] text-[#f59e0b] flex items-center justify-center">
                    <span className="material-symbols-outlined text-[24px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                      fact_check
                    </span>
                  </div>
                  <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                    It separates what it knows from what it models
                  </h3>
                  <p className="text-[14px] leading-relaxed text-[#534434]">
                    Real OpenStreetMap road geometry and curated hospital profiles are kept strictly
                    distinct from simulated traffic delays and modelled unit telemetry, giving
                    operators full clarity on what is live data versus demonstration state.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* 4. ONE INCIDENT, FOUR PORTALS */}
          <section className="w-full bg-[#f4f3f1] py-8">
            <div className="max-w-7xl mx-auto px-6 flex flex-col gap-6">
              <div className="flex flex-col gap-1">
                <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#565d79]">
                  MULTI-ROLE WORKFLOW
                </span>
                <h2 className="font-['Space_Grotesk',sans-serif] text-[clamp(24px,3.5vw,32px)] font-bold text-[#131a33]">
                  One incident, four portals
                </h2>
                <p className="text-[16px] text-[#534434]">
                  Open them in separate tabs and watch a single call move between them in real time.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <Link
                  to="/citizen"
                  className="group bg-white rounded-xl p-6 shadow-xs hover:shadow-lg transition-all flex flex-col justify-between gap-6 border border-[#efeeeb]"
                >
                  <div className="flex flex-col gap-4">
                    <div className="flex items-center justify-between">
                      <span className="w-10 h-10 rounded-lg bg-[#b91a24] text-white font-['Archivo_Narrow',sans-serif] text-[20px] font-bold flex items-center justify-center">
                        C
                      </span>
                      <span className="material-symbols-outlined text-[#534434] group-hover:translate-x-1 transition-transform">
                        arrow_forward
                      </span>
                    </div>
                    <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                      Citizen
                    </h3>
                    <p className="text-[14px] text-[#534434]">
                      Report an emergency, track the response.
                    </p>
                  </div>
                  <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#b91a24]">
                    OPEN PORTAL
                  </span>
                </Link>

                <Link
                  to="/dispatcher"
                  className="group bg-white rounded-xl p-6 shadow-xs hover:shadow-lg transition-all flex flex-col justify-between gap-6 border border-[#efeeeb]"
                >
                  <div className="flex flex-col gap-4">
                    <div className="flex items-center justify-between">
                      <span className="w-10 h-10 rounded-lg bg-[#f59e0b] text-[#131a33] font-['Archivo_Narrow',sans-serif] text-[20px] font-bold flex items-center justify-center">
                        D
                      </span>
                      <span className="material-symbols-outlined text-[#534434] group-hover:translate-x-1 transition-transform">
                        arrow_forward
                      </span>
                    </div>
                    <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                      City dispatch
                    </h3>
                    <p className="text-[14px] text-[#534434]">
                      Review, override, dispatch.
                    </p>
                  </div>
                  <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#855300]">
                    OPEN PORTAL
                  </span>
                </Link>

                <Link
                  to="/driver"
                  className="group bg-white rounded-xl p-6 shadow-xs hover:shadow-lg transition-all flex flex-col justify-between gap-6 border border-[#efeeeb]"
                >
                  <div className="flex flex-col gap-4">
                    <div className="flex items-center justify-between">
                      <span className="w-10 h-10 rounded-lg bg-[#131a33] text-white font-['Archivo_Narrow',sans-serif] text-[20px] font-bold flex items-center justify-center">
                        F
                      </span>
                      <span className="material-symbols-outlined text-[#534434] group-hover:translate-x-1 transition-transform">
                        arrow_forward
                      </span>
                    </div>
                    <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                      Field unit
                    </h3>
                    <p className="text-[14px] text-[#534434]">
                      Two-stage navigation and handover.
                    </p>
                  </div>
                  <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#131a33]">
                    OPEN PORTAL
                  </span>
                </Link>

                <Link
                  to="/hospital"
                  className="group bg-white rounded-xl p-6 shadow-xs hover:shadow-lg transition-all flex flex-col justify-between gap-6 border border-[#efeeeb]"
                >
                  <div className="flex flex-col gap-4">
                    <div className="flex items-center justify-between">
                      <span className="w-10 h-10 rounded-lg bg-[#565d79] text-white font-['Archivo_Narrow',sans-serif] text-[20px] font-bold flex items-center justify-center">
                        E
                      </span>
                      <span className="material-symbols-outlined text-[#534434] group-hover:translate-x-1 transition-transform">
                        arrow_forward
                      </span>
                    </div>
                    <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                      Emergency department
                    </h3>
                    <p className="text-[14px] text-[#534434]">
                      Inbound patients and capacity.
                    </p>
                  </div>
                  <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#565d79]">
                    OPEN PORTAL
                  </span>
                </Link>
              </div>
            </div>
          </section>

          {/* 5. WHAT IS REAL, AND WHAT IS NOT */}
          <section className="w-full bg-transparent py-8">
            <div className="max-w-7xl mx-auto px-6 flex flex-col gap-6">
              <div className="flex flex-col gap-1">
                <span className="font-['Archivo_Narrow',sans-serif] text-[11px] font-bold uppercase tracking-wider text-[#534434]">
                  TRANSPARENCY &amp; SCOPE
                </span>
                <h2 className="font-['Space_Grotesk',sans-serif] text-[clamp(24px,3.5vw,32px)] font-bold text-[#131a33]">
                  What is real, and what is not
                </h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Data sources and routing */}
                <div className="bg-white rounded-xl p-6 shadow-xs border border-[#efeeeb] flex flex-col gap-4">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[#565d79] text-[22px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                      verified
                    </span>
                    <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                      Data sources and routing
                    </h3>
                  </div>
                  <ul className="flex flex-col gap-4 text-[14px] text-[#534434]">
                    <li className="flex items-start gap-2">
                      <span className="material-symbols-outlined text-[#565d79] text-[20px] shrink-0" style={{ fontVariationSettings: "'FILL' 1" }}>
                        check_circle
                      </span>
                      <span>
                        Bengaluru road network extracted from OpenStreetMap (112,725 nodes, 178,089 directed edges).
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="material-symbols-outlined text-[#565d79] text-[20px] shrink-0" style={{ fontVariationSettings: "'FILL' 1" }}>
                        check_circle
                      </span>
                      <span>
                        30 Bengaluru hospitals with coordinates verified via OpenStreetMap and curated capability profiles.
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="material-symbols-outlined text-[#565d79] text-[20px] shrink-0" style={{ fontVariationSettings: "'FILL' 1" }}>
                        check_circle
                      </span>
                      <span>
                        Deterministic shortest-path routing and 6-step monitoring agent running locally in under 2 seconds per alert.
                      </span>
                    </li>
                  </ul>
                </div>

                {/* Modelled */}
                <div className="bg-[#ffddb8]/30 rounded-xl p-6 shadow-xs border border-[#efeeeb] flex flex-col gap-4">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[#855300] text-[22px]">
                      science
                    </span>
                    <h3 className="font-['Archivo_Narrow',sans-serif] text-[20px] font-bold text-[#131a33]">
                      Modelled
                    </h3>
                  </div>
                  <ul className="flex flex-col gap-4 text-[14px] text-[#653e00]">
                    <li className="flex items-start gap-2">
                      <span className="material-symbols-outlined text-[#855300] text-[20px] shrink-0">
                        radio_button_checked
                      </span>
                      <span>
                        Simulated ambulance GPS telemetry, speed drops, road closures, and detour events for demonstration.
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="material-symbols-outlined text-[#855300] text-[20px] shrink-0">
                        radio_button_checked
                      </span>
                      <span>
                        Synthetic emergency call intake, dispatch overrides, and hospital bed availability counts.
                      </span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="material-symbols-outlined text-[#855300] text-[20px] shrink-0">
                        radio_button_checked
                      </span>
                      <span>
                        Illustrative capability scores and estimated travel times; not a record of live clinical or ambulance operations.
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* FOOTER */}
      <footer className="w-full bg-[#f4f3f1] py-6 border-t border-[#efeeeb]">
        <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-[12px] text-[#534434]">
          <span>RapidGrid · Bengaluru emergency vehicle dispatch</span>
          <span>Road data © OpenStreetMap contributors</span>
        </div>
      </footer>
    </div>
  );
}

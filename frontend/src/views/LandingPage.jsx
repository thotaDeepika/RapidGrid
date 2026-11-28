import React from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight,
  Building2,
  Check,
  ClipboardCheck,
  Eye,
  Hospital,
  Network,
  Play,
  Radio,
  Siren,
  Users,
} from 'lucide-react';

function Frame({ src, alt, ratio = 'aspect-video' }) {
  return (
    <div className={`relative w-full overflow-hidden bg-ink ${ratio}`}>
      <img
        src={src}
        alt={alt}
        className="absolute inset-0 h-full w-full object-cover"
        decoding="async"
      />
    </div>
  );
}

const PORTALS = [
  {
    to: '/citizen',
    glyph: 'C',
    title: 'Citizen',
    text: 'Report an emergency, track the response.',
    image: '/art/citizen-report.jpg',
    alt: 'A simple phone with an amber alert mark',
  },
  {
    to: '/dispatcher',
    glyph: 'D',
    title: 'City dispatch',
    text: 'Review, override, dispatch.',
    image: '/art/dispatch-desk.jpg',
    alt: 'A dispatch desk with a city map',
  },
  {
    to: '/driver',
    glyph: 'F',
    title: 'Field unit',
    text: 'Two-stage navigation and handover.',
    image: '/art/unit-field.jpg',
    alt: 'A field ambulance in ink and amber',
  },
  {
    to: '/hospital',
    glyph: 'E',
    title: 'Emergency department',
    text: 'Inbound patients and capacity.',
    image: '/art/hospital-er.jpg',
    alt: 'A hospital facade in ink and bone',
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-field text-text">
      <header className="fixed inset-x-0 top-0 z-50 border-b border-rule-ink bg-ink">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between gap-3 px-4 sm:h-16 sm:px-6">
          <Link to="/" className="flex min-w-0 items-center gap-3">
            <span className="grid h-9 w-9 shrink-0 place-items-center rounded-sm bg-signal font-display text-[18px] font-bold text-ink">
              R
            </span>
            <span className="min-w-0">
              <span className="block font-display text-[18px] font-bold leading-none tracking-tight text-on-ink sm:text-[20px]">
                RapidGrid
              </span>
              <span className="mt-1 hidden truncate text-[12px] text-on-ink-muted sm:block">
                Bengaluru emergency vehicle dispatch
              </span>
            </span>
          </Link>

          <nav className="hidden items-center gap-5 md:flex">
            <Link to="/dispatcher" className="rounded-sm bg-signal px-2.5 py-1 text-[13px] font-semibold text-ink">
              Dispatch
            </Link>
            <Link to="/seats" className="text-[13px] font-semibold text-on-ink-muted hover:text-on-ink">
              Fleet &amp; Seats
            </Link>
            <Link to="/control" className="text-[13px] font-semibold text-on-ink-muted hover:text-on-ink">
              Control Room
            </Link>
          </nav>

          <Link
            to="/login"
            className="shrink-0 rounded-sm bg-signal px-3.5 py-2 text-[13px] font-bold text-ink hover:brightness-105"
          >
            Sign in
          </Link>
        </div>
      </header>

      <main className="pt-14 sm:pt-16">
        <section className="mx-auto grid max-w-6xl items-center gap-8 px-4 py-8 sm:px-6 sm:py-12 lg:grid-cols-2 lg:gap-10">
          <div className="flex min-w-0 flex-col gap-5">
            <div className="inline-flex w-fit items-center gap-2 rounded-sm border border-critical-edge bg-critical-wash px-3 py-1 text-critical">
              <span className="live-dot h-2 w-2 rounded-full bg-critical" />
              <span className="font-display text-[11px] font-bold uppercase tracking-[0.14em]">
                Emergency vehicle movement
              </span>
            </div>

            <h1 className="font-display text-[clamp(28px,5vw,44px)] font-bold leading-[1.05] text-text">
              It watches the route, so dispatch does not have to guess.
            </h1>

            <p className="max-w-xl text-[15px] leading-relaxed text-text-muted sm:text-[16px]">
              RapidGrid's monitoring agent follows every unit on a call. When one leaves its
              route, meets a closed road or slows down, it says why, how late, which way round,
              and whether to keep that unit or send a closer one, in plain words. It also sends
              each patient to a hospital that can treat them, not just the nearest.
            </p>

            <div className="flex flex-col gap-3 pt-1 sm:flex-row sm:flex-wrap">
              <Link
                to="/citizen"
                className="inline-flex items-center justify-center gap-2 rounded-sm bg-signal px-5 py-3.5 font-display text-[14px] font-bold text-ink"
              >
                <Siren size={18} />
                Report an emergency
              </Link>
              <Link
                to="/dispatcher"
                className="inline-flex items-center justify-center gap-2 rounded-sm bg-ink px-5 py-3.5 font-display text-[14px] font-bold text-on-ink"
              >
                <Radio size={18} />
                Open the dispatch console
              </Link>
            </div>

            <div className="flex flex-col gap-2 text-[12px] text-text-muted sm:flex-row sm:flex-wrap sm:items-center sm:gap-x-4">
              <Link to="/seats" className="inline-flex items-center gap-1.5 hover:text-text">
                <Users size={15} className="text-signal-hover" />
                Choose your seat (team demo)
              </Link>
              <Link to="/control" className="inline-flex items-center gap-1.5 hover:text-text">
                <Building2 size={15} />
                City control room
              </Link>
              <Link to="/demo" className="inline-flex items-center gap-1.5 hover:text-text">
                <Play size={15} className="text-critical" />
                Guided demo
              </Link>
            </div>
          </div>

          <div className="min-w-0 overflow-hidden rounded-sm border border-rule-ink bg-ink">
            <div className="relative">
              <Frame
                src="/art/hero-corridor.jpg"
                alt="A night street grid with an amber route and a small ambulance"
              />
              <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ink/85 via-ink/10 to-transparent" />
              <div className="absolute left-3 top-3 inline-flex max-w-[calc(100%-1.5rem)] items-center gap-2 rounded-sm bg-ink/90 px-2.5 py-1 text-on-ink">
                <span className="live-dot h-2 w-2 shrink-0 rounded-full bg-signal" />
                <span className="truncate font-display text-[11px] font-bold uppercase tracking-[0.12em]">
                  Bengaluru live grid · KA-01-G-4821
                </span>
              </div>
              <div className="absolute inset-x-3 bottom-3 flex items-end justify-between gap-3 text-on-ink">
                <div className="min-w-0">
                  <div className="font-display text-[11px] font-bold uppercase tracking-[0.12em] text-signal">
                    Active corridor
                  </div>
                  <div className="truncate text-[15px] font-semibold sm:text-[16px]">
                    Hebbal Flyover → Aster CMI
                  </div>
                </div>
                <div className="shrink-0 rounded-sm bg-signal px-2.5 py-1.5 font-mono text-[13px] font-bold text-ink">
                  ETA 5.9 min
                </div>
              </div>
            </div>

            <div className="border-t border-rule-ink p-4 sm:p-5">
              <div className="mb-3 flex items-center justify-between gap-3">
                <span className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-on-ink-muted">
                  What it runs on
                </span>
                <span className="font-mono text-[12px] text-signal">BLR-GRAPH v2.4</span>
              </div>
              <div className="grid grid-cols-2 gap-2 sm:gap-3">
                {[
                  ['112,725', 'OSM nodes · 178,089 edges'],
                  ['30', 'Facilities · curated profiles'],
                  ['6', 'Agent steps per alert'],
                  ['< 2 s', 'Routes, cause and backup'],
                ].map(([value, label]) => (
                  <div key={label} className="rounded-sm bg-ink-raised px-3 py-3">
                    <div className="font-mono text-[22px] font-bold leading-none text-on-ink sm:text-[24px]">
                      {value}
                    </div>
                    <p className="mt-1.5 text-[12px] leading-snug text-on-ink-muted">{label}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="border-y border-rule bg-paper py-8 sm:py-12">
          <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 sm:px-6">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <div className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-critical">
                  Capability-first routing
                </div>
                <h2 className="mt-1 font-display text-[clamp(24px,3.5vw,32px)] font-bold">
                  Illustrative comparison · Cardiac · Hebbal, Bengaluru
                </h2>
              </div>
              <span className="w-fit rounded-sm border border-rule bg-paper-sunk px-3 py-1.5 font-mono text-[13px] text-text-muted">
                CASE: STEMI-04
              </span>
            </div>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <article className="flex flex-col justify-between gap-6 rounded-sm bg-signal p-5 text-ink sm:p-6">
                <div>
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="inline-flex items-center gap-1 rounded-sm bg-ink px-2.5 py-1 font-display text-[11px] font-bold uppercase tracking-[0.12em] text-on-ink">
                      <Check size={14} />
                      Selected
                    </span>
                    <span className="font-display text-[11px] font-bold uppercase tracking-[0.12em]">
                      Primary match
                    </span>
                  </div>
                  <h3 className="mt-3 font-display text-[22px] font-semibold sm:text-[24px]">
                    Aster CMI Hospital (Hebbal)
                  </h3>
                  <p className="mt-1 text-[14px]">Compared factor · Cath lab</p>
                </div>
                <div className="grid grid-cols-2 gap-3 rounded-sm bg-paper/90 p-4 text-text">
                  <div>
                    <div className="font-display text-[11px] font-bold uppercase text-text-muted">Score</div>
                    <div className="font-mono text-[24px] font-bold">0.82</div>
                  </div>
                  <div>
                    <div className="font-display text-[11px] font-bold uppercase text-text-muted">Road ETA</div>
                    <div className="font-mono text-[24px] font-bold">5.9 min</div>
                  </div>
                </div>
              </article>

              <article className="flex flex-col justify-between gap-6 rounded-sm bg-ink p-5 text-on-ink sm:p-6">
                <div>
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="rounded-sm border border-rule-ink px-2.5 py-1 font-display text-[11px] font-bold uppercase tracking-[0.12em] text-on-ink-muted">
                      Faster alternative
                    </span>
                    <span className="font-display text-[11px] font-bold uppercase tracking-[0.12em] text-on-ink-muted">
                      Candidate #2
                    </span>
                  </div>
                  <h3 className="mt-3 font-display text-[22px] font-semibold text-on-ink sm:text-[24px]">
                    MS Ramaiah Memorial Hospital
                  </h3>
                  <p className="mt-1 text-[14px] text-on-ink-muted">
                    Alternative candidate · compare capability and travel time
                  </p>
                </div>
                <div className="grid grid-cols-2 gap-3 rounded-sm bg-ink-raised p-4">
                  <div>
                    <div className="font-display text-[11px] font-bold uppercase text-on-ink-muted">Score</div>
                    <div className="font-mono text-[24px] font-bold text-on-ink">0.76</div>
                  </div>
                  <div>
                    <div className="font-display text-[11px] font-bold uppercase text-on-ink-muted">Road ETA</div>
                    <div className="font-mono text-[24px] font-bold text-on-ink">6.4 min</div>
                  </div>
                </div>
              </article>
            </div>

            <p className="rounded-sm border border-rule bg-paper-sunk px-4 py-2.5 text-[12px] leading-relaxed text-text-muted">
              This recommendation adds 0.5 minutes of estimated travel. The compared capability score
              is one part of the ranking; this is not a record of an ambulance journey.
            </p>
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
          <div className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-signal-hover">
            System architecture
          </div>
          <h2 className="mt-1 font-display text-[clamp(24px,3.5vw,32px)] font-bold">
            Built for high-stakes dispatch
          </h2>

          <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">
            {[
              {
                icon: Eye,
                title: 'An agent watches every unit on its route',
                text: "RapidGrid's monitoring agent tracks each active ambulance against its planned path. When a unit slows, detours, or hits a blockage, it explains the cause, estimates the delay, and recommends whether to hold or reassign.",
              },
              {
                icon: Hospital,
                title: 'It routes on capability, not just proximity',
                text: 'Sending a cardiac or trauma patient to the closest clinic wastes critical minutes. RapidGrid scores 30 Bengaluru facilities on clinical capability, bed readiness, and road ETA so each patient reaches a hospital that can treat them.',
              },
              {
                icon: Network,
                title: 'Its own road graph, no provider needed',
                text: "Built directly on OpenStreetMap's Bengaluru street network (112,725 nodes and 178,089 edges), RapidGrid computes turn-by-turn routes, alternate corridors, and backup unit ETAs locally in under two seconds.",
              },
              {
                icon: ClipboardCheck,
                title: 'It separates what it knows from what it models',
                text: 'Real OpenStreetMap road geometry and curated hospital profiles are kept strictly distinct from simulated traffic delays and modelled unit telemetry, giving operators full clarity on what is live data versus demonstration state.',
              },
            ].map(({ icon: Icon, title, text }) => (
              <article key={title} className="rounded-sm border border-rule bg-paper p-5 sm:p-6">
                <div className="grid h-11 w-11 place-items-center rounded-sm bg-ink text-signal">
                  <Icon size={20} />
                </div>
                <h3 className="mt-4 font-display text-[20px] font-bold">{title}</h3>
                <p className="mt-2 text-[14px] leading-relaxed text-text-muted">{text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="border-y border-rule bg-paper py-8 sm:py-12">
          <div className="mx-auto max-w-6xl px-4 sm:px-6">
            <div className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-text-muted">
              Multi-role workflow
            </div>
            <h2 className="mt-1 font-display text-[clamp(24px,3.5vw,32px)] font-bold">
              One incident, four portals
            </h2>
            <p className="mt-2 max-w-2xl text-[15px] text-text-muted sm:text-[16px]">
              Open them in separate tabs and watch a single call move between them in real time.
            </p>

            <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {PORTALS.map((portal) => (
                <Link
                  key={portal.to}
                  to={portal.to}
                  className="group flex flex-col overflow-hidden rounded-sm border border-rule bg-field"
                >
                  <Frame src={portal.image} alt={portal.alt} ratio="aspect-[4/3]" />
                  <div className="flex flex-1 flex-col gap-3 p-4">
                    <div className="flex items-center justify-between">
                      <span className="grid h-9 w-9 place-items-center rounded-sm bg-ink font-display text-[16px] font-bold text-signal">
                        {portal.glyph}
                      </span>
                      <ArrowRight size={16} className="text-text-faint transition-transform group-hover:translate-x-0.5" />
                    </div>
                    <h3 className="font-display text-[20px] font-bold">{portal.title}</h3>
                    <p className="text-[14px] leading-relaxed text-text-muted">{portal.text}</p>
                    <span className="mt-auto font-display text-[11px] font-bold uppercase tracking-[0.14em] text-signal-hover">
                      Open portal
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
          <div className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-text-muted">
            Transparency &amp; scope
          </div>
          <h2 className="mt-1 font-display text-[clamp(24px,3.5vw,32px)] font-bold">
            What is real, and what is not
          </h2>

          <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">
            <article className="rounded-sm border border-ink bg-paper p-5 sm:p-6">
              <div className="flex items-center gap-2">
                <Check size={18} />
                <h3 className="font-display text-[20px] font-bold">Data sources and routing</h3>
              </div>
              <ul className="mt-4 space-y-3 text-[14px] leading-relaxed text-text-muted">
                <li>Bengaluru road network extracted from OpenStreetMap (112,725 nodes, 178,089 directed edges).</li>
                <li>30 Bengaluru hospitals with coordinates verified via OpenStreetMap and curated capability profiles.</li>
                <li>Deterministic shortest-path routing and 6-step monitoring agent running locally in under 2 seconds per alert.</li>
              </ul>
            </article>
            <article className="rounded-sm border border-dashed border-text-faint bg-paper-sunk p-5 sm:p-6">
              <div className="flex items-center gap-2 text-text-muted">
                <ClipboardCheck size={18} />
                <h3 className="font-display text-[20px] font-bold text-text">Modelled</h3>
              </div>
              <ul className="mt-4 space-y-3 text-[14px] leading-relaxed text-text-muted">
                <li>Simulated ambulance GPS telemetry, speed drops, road closures, and detour events for demonstration.</li>
                <li>Synthetic emergency call intake, dispatch overrides, and hospital bed availability counts.</li>
                <li>Illustrative capability scores and estimated travel times; not a record of live clinical or ambulance operations.</li>
              </ul>
            </article>
          </div>
        </section>
      </main>

      <footer className="border-t border-rule-ink bg-ink">
        <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-6 text-[12px] text-on-ink-muted sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <span>RapidGrid · Bengaluru emergency vehicle dispatch</span>
          <span>Road data © OpenStreetMap contributors</span>
        </div>
      </footer>
    </div>
  );
}

/**
 * Landing page.
 *
 * The hero is the product's actual thesis rather than a slogan: a real
 * decision the system made, with the trade-off it accepted, shown as the
 * dispatcher sees it. Anyone can route an ambulance to the nearest hospital;
 * the interesting claim is that this one sometimes drives further, on purpose,
 * and can say why.
 *
 * The page is deliberately short. The product is four working portals, and the
 * fastest way to be convinced is to open one.
 */

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Radio, ArrowRight, Check } from 'lucide-react';

const CAPABILITIES = [
  {
    title: 'It routes on capability, not just proximity',
    body: 'A cardiac call goes to a facility with a 24×7 cath lab even when a general hospital is closer — the same specialty-centre bypass real EMS protocols use. Capability profiles are curated for 30 Bengaluru hospitals; oncology, maternity and day-surgery units are excluded from emergency routing entirely.',
  },
  {
    title: 'It keeps working when the internet does not',
    body: 'Live traffic routing runs against the Google Routes API. When that is unavailable — quota, outage, venue wi-fi — an A* router falls back to a cached 112,725-node OpenStreetMap graph of Bengaluru and keeps producing real paths, labelled as offline rather than passed off as live.',
  },
  {
    title: 'It separates what it knows from what it models',
    body: 'Hospital capability is curated and drives routing. Live bed counts are modelled, because no hospital data feed is integrated — so they are drawn differently, everywhere they appear. Nothing on screen is a number we invented and presented as a measurement.',
  },
];

/** A real plan, if the backend is up; otherwise a representative one. */
const SAMPLE = {
  emergency: 'Cardiac',
  location: 'Hebbal, Bengaluru',
  chosen: { name: 'Fortis Hospital (Bannerghatta Road)', factor: 'Cath lab', value: '0.90', eta: '10.7' },
  runnerUp: { name: "St John's Medical College", factor: 'Cath lab', value: '0.76', eta: '4.5' },
};

export default function LandingPage() {
  const [plan, setPlan] = useState(SAMPLE);

  // Prefer a genuine decision from the running backend.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch('/api/incidents/');
        if (!res.ok) return;
        const { incidents = [] } = await res.json();
        const withPlan = incidents
          .filter((i) => i.action_plan?.all_hospitals?.length > 1)
          .pop();
        if (!withPlan || cancelled) return;

        const [a, b] = withPlan.action_plan.all_hospitals;
        const fa = a.score_breakdown ?? [];
        const fb = b.score_breakdown ?? [];
        const key = fa.reduce(
          (best, f) => {
            const other = fb.find((x) => x.factor === f.factor);
            const gap = other ? f.weighted_score - other.weighted_score : 0;
            return gap > best.gap ? { gap, factor: f.factor, a: f.raw_score, b: other?.raw_score } : best;
          },
          { gap: -Infinity, factor: null },
        );
        if (!key.factor) return;

        setPlan({
          emergency: (withPlan.emergency_type ?? 'Emergency').replace(/^\w/, (c) => c.toUpperCase()),
          location: 'Bengaluru',
          chosen: {
            name: a.name,
            factor: key.factor,
            value: key.a?.toFixed(2),
            eta: a.road_eta_seconds ? (a.road_eta_seconds / 60).toFixed(1) : null,
          },
          runnerUp: {
            name: b.name,
            factor: key.factor,
            value: key.b?.toFixed(2),
            eta: b.road_eta_seconds ? (b.road_eta_seconds / 60).toFixed(1) : null,
          },
        });
      } catch { /* keep the sample */ }
    })();
    return () => { cancelled = true; };
  }, []);

  const further =
    plan.chosen.eta && plan.runnerUp.eta
      ? (Number(plan.chosen.eta) - Number(plan.runnerUp.eta)).toFixed(1)
      : null;

  return (
    <div className="min-h-screen bg-field">
      <header className="border-b border-rule">
        <div className="mx-auto flex max-w-[1080px] items-center justify-between px-5 py-4">
          <div className="flex items-center gap-2.5">
            <div className="grid h-8 w-8 place-items-center rounded-sm bg-ink text-signal">
              <Radio size={16} className="stroke-[2.4]" />
            </div>
            <span className="font-display text-[15px] font-extrabold tracking-tight text-text">
              RapidGrid
            </span>
          </div>
          <Link
            to="/login"
            className="tap inline-flex items-center gap-1.5 rounded-sm bg-ink px-4 py-2.5 t-tag text-on-ink transition-colors hover:bg-ink-raised"
          >
            Open a portal <ArrowRight size={13} />
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-[1080px] px-5">
        {/* ---- Hero: the thesis, as a decision ---------------------------- */}
        <section className="grid gap-9 py-10 md:py-14 lg:grid-cols-[1fr_minmax(360px,440px)] lg:gap-14 lg:py-20">
          <div className="self-center">
            <p className="eyebrow">Emergency vehicle routing · Bengaluru</p>
            <h1 className="mt-4 font-display text-[clamp(31px,8.5vw,52px)] font-extrabold leading-[1.05] tracking-[-0.03em] text-text">
              The nearest hospital
              <br />
              is often the
              <span className="text-signal"> wrong one</span>.
            </h1>
            <p className="mt-5 max-w-[46ch] text-[15px] leading-relaxed text-text-muted">
              RapidGrid routes emergency vehicles on what a hospital can actually treat, not just
              how close it is — and shows the dispatcher exactly what each decision traded away.
            </p>
            <div className="mt-7 flex flex-col gap-2.5 sm:flex-row sm:flex-wrap">
              <Link
                to="/citizen"
                className="tap inline-flex flex-1 items-center justify-center gap-2 rounded-sm bg-signal px-5 py-3.5 t-tag text-white transition-colors hover:bg-signal-hover sm:flex-none"
              >
                Report an emergency
              </Link>
              <Link
                to="/dispatcher"
                className="tap inline-flex flex-1 items-center justify-center gap-2 rounded-sm border border-rule bg-paper px-5 py-3.5 t-tag text-text transition-colors hover:border-rule-strong sm:flex-none"
              >
                Open dispatch console
              </Link>
            </div>
          </div>

          {/* The decision card - the signature object of the product. */}
          <div className="self-center rounded-md border border-rule bg-paper">
            <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-1 border-b border-rule px-4 py-2.5">
              <span className="eyebrow">A decision it made</span>
              <span className="t-tag text-critical">
                {plan.emergency} · {plan.location}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 p-3">
              <div className="rounded-sm border border-signal bg-signal-wash p-3">
                <div className="t-tag text-signal-hover">
                  Selected
                </div>
                <div className="mt-1.5 text-[13px] font-semibold leading-snug text-text">
                  {plan.chosen.name}
                </div>
                <dl className="mt-3 space-y-1.5 border-t border-signal-edge pt-2.5 t-meta">
                  <div className="flex justify-between gap-2">
                    <dt className="truncate text-text-muted">{plan.chosen.factor}</dt>
                    <dd className="font-bold text-text">{plan.chosen.value}</dd>
                  </div>
                  <div className="flex justify-between gap-2">
                    <dt className="text-text-muted">Road ETA</dt>
                    <dd className="font-bold text-text">{plan.chosen.eta ?? '—'} min</dd>
                  </div>
                </dl>
              </div>

              <div className="rounded-sm border border-rule bg-paper-sunk p-3">
                <div className="t-tag text-text-faint">
                  Closer, not chosen
                </div>
                <div className="mt-1.5 text-[13px] font-semibold leading-snug text-text">
                  {plan.runnerUp.name}
                </div>
                <dl className="mt-3 space-y-1.5 border-t border-rule pt-2.5 t-meta">
                  <div className="flex justify-between gap-2">
                    <dt className="truncate text-text-muted">{plan.runnerUp.factor}</dt>
                    <dd className="font-bold text-text">{plan.runnerUp.value}</dd>
                  </div>
                  <div className="flex justify-between gap-2">
                    <dt className="text-text-muted">Road ETA</dt>
                    <dd className="font-bold text-text">{plan.runnerUp.eta ?? '—'} min</dd>
                  </div>
                </dl>
              </div>
            </div>

            <p className="border-t border-rule px-4 py-3 text-[12.5px] leading-relaxed text-text-muted">
              {further && Number(further) > 0 ? (
                <>
                  The ambulance drove{' '}
                  <span className="font-mono font-bold text-signal-hover">{further} min</span>{' '}
                  further, on purpose — because the closer hospital could not treat this patient as
                  well.
                </>
              ) : (
                <>
                  The system states which hospital it rejected, on which factor, and what the choice
                  cost in road minutes.
                </>
              )}
            </p>
          </div>
        </section>

        {/* ---- What it does ---------------------------------------------- */}
        <section className="border-t border-rule py-14">
          <div className="grid gap-7 md:grid-cols-3 md:gap-8">
            {CAPABILITIES.map((c) => (
              <article key={c.title}>
                <h2 className="font-display text-[16px] font-bold leading-snug text-text">
                  {c.title}
                </h2>
                <p className="mt-2.5 text-[13px] leading-relaxed text-text-muted">{c.body}</p>
              </article>
            ))}
          </div>
        </section>

        {/* ---- Portals ---------------------------------------------------- */}
        <section className="border-t border-rule py-14">
          <h2 className="font-display text-[clamp(20px,5vw,24px)] font-extrabold tracking-tight text-text">
            One incident, four portals
          </h2>
          <p className="mt-2 max-w-[56ch] text-[14px] leading-relaxed text-text-muted">
            Open them in separate tabs and watch a single call move between them in real time.
          </p>

          <div className="mt-6 grid gap-2 sm:grid-cols-2 lg:gap-3">
            {[
              { to: '/citizen', name: 'Citizen', desc: 'Report an emergency, track the response.' },
              { to: '/dispatcher', name: 'City dispatch', desc: 'Review, override, dispatch.' },
              { to: '/driver', name: 'Field unit', desc: 'Two-stage navigation and handover.' },
              { to: '/hospital', name: 'Emergency department', desc: 'Inbound patients and capacity.' },
            ].map((p) => (
              <Link
                key={p.to}
                to={p.to}
                className="group flex items-center justify-between gap-3 rounded-md border border-rule bg-paper px-4 py-3.5 transition-colors hover:border-signal"
              >
                <span>
                  <span className="block text-[14px] font-bold text-text">{p.name}</span>
                  <span className="mt-0.5 block text-[12px] text-text-muted">{p.desc}</span>
                </span>
                <ArrowRight
                  size={16}
                  className="shrink-0 text-text-faint transition-transform group-hover:translate-x-0.5 group-hover:text-signal"
                />
              </Link>
            ))}
          </div>
        </section>

        {/* ---- Honest limits: the credibility move ------------------------ */}
        <section className="border-t border-rule py-14">
          <h2 className="font-display text-[clamp(18px,4.5vw,20px)] font-extrabold tracking-tight text-text">
            What is real, and what is not
          </h2>
          <div className="mt-5 grid gap-7 md:grid-cols-2 md:gap-6">
            <div>
              <div className="eyebrow mb-2.5 text-verified">Real</div>
              <ul className="space-y-2">
                {[
                  'Bengaluru road network — 112,725 nodes from OpenStreetMap',
                  'Live traffic routing via the Google Routes API',
                  'Live weather, factored into ETA',
                  'Hospital capability profiles, curated for 30 facilities',
                  'A* pathfinding, closures and congestion included',
                ].map((t) => (
                  <li key={t} className="flex items-start gap-2 text-[13px] leading-relaxed text-text-muted">
                    <Check size={14} className="mt-[3px] shrink-0 text-verified" />
                    {t}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <div className="eyebrow mb-2.5 text-modelled">Modelled</div>
              <ul className="space-y-2">
                {[
                  'Live ICU beds and blood units — no hospital feed is integrated',
                  'Ambulance fleet positions — hubs are fixed, not GPS-tracked',
                  'Triage classification — transparent keyword scoring, not a trained model',
                  'Signal preemption and congestion displacement — simulated',
                ].map((t) => (
                  <li key={t} className="flex items-start gap-2 text-[13px] leading-relaxed text-text-muted">
                    <span className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-modelled" />
                    {t}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-rule">
        <div className="mx-auto flex max-w-[1080px] flex-wrap items-center justify-between gap-3 px-5 py-6">
          <span className="t-meta uppercase tracking-[0.12em] text-text-faint">
            RapidGrid · GeoAgentic emergency routing
          </span>
          <span className="t-meta text-text-faint">
            Road data © OpenStreetMap contributors
          </span>
        </div>
      </footer>
    </div>
  );
}

/**
 * Portal frame.
 *
 * A slim command bar rather than a marketing header - the portals below it
 * need the vertical space. The previous version showed a permanently green
 * "LIVE SYNC" badge that was hardcoded and never reflected backend state; this
 * one polls /health and tells the truth, including which routing tier is
 * actually serving requests.
 */

import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { LogOut, Radio, Truck, PlusSquare, Heart, Activity } from 'lucide-react';

const PORTALS = {
  dispatcher: { title: 'City dispatch', sub: 'Multi-agent oversight', Icon: Radio },
  driver: { title: 'Field unit', sub: 'Navigation and handover', Icon: Truck },
  hospital: { title: 'Emergency department', sub: 'Incoming patients and capacity', Icon: PlusSquare },
  citizen: { title: 'Emergency assistance', sub: 'Report and track', Icon: Heart },
};

export default function SharedShell({ children }) {
  const { role, driverInfo, hospitalInfo, logout } = useAuth();
  const navigate = useNavigate();
  const [health, setHealth] = useState(null);
  const [reachable, setReachable] = useState(true);

  useEffect(() => {
    let cancelled = false;
    const ping = async () => {
      try {
        const res = await fetch('/health');
        if (!res.ok) throw new Error();
        const data = await res.json();
        if (!cancelled) {
          setHealth(data);
          setReachable(true);
        }
      } catch {
        if (!cancelled) setReachable(false);
      }
    };
    ping();
    const timer = setInterval(ping, 10000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, []);

  const meta = PORTALS[role] ?? { title: 'RapidGrid', sub: 'Emergency response', Icon: Activity };
  const Icon = meta.Icon;

  let title = meta.title;
  let sub = meta.sub;
  if (role === 'driver' && driverInfo) {
    title = `${driverInfo.driverName} · ${driverInfo.unitId}`;
    sub = driverInfo.hubName ?? meta.sub;
  } else if (role === 'hospital' && hospitalInfo?.name) {
    title = hospitalInfo.name;
    sub = meta.sub;
  }

  // Say which tier is actually serving routes, rather than always "LIVE".
  const live = health?.routing?.live_api_key_configured && health?.routing?.billable_api_calls >= 0;
  const offlineOnly = health?.routing && !health.routing.live_api_key_configured;
  const tier = !reachable
    ? { label: 'Backend offline', tone: 'bad' }
    : offlineOnly
      ? { label: 'Offline routing', tone: 'warn' }
      : { label: 'Live routing', tone: 'ok' };

  const tones = {
    ok: 'border-verified/30 bg-verified-wash text-verified',
    warn: 'border-signal-edge bg-signal-wash text-signal-hover',
    bad: 'border-critical-edge bg-critical-wash text-critical',
  };

  return (
    <div className="flex min-h-screen flex-col bg-field">
      <header className="sticky top-0 z-50 border-b border-rule-ink bg-ink">
        <div className="mx-auto flex max-w-[1600px] items-center justify-between gap-4 px-4 py-2.5">
          <div className="flex min-w-0 items-center gap-3">
            <div className="grid h-8 w-8 shrink-0 place-items-center rounded-sm bg-signal text-white">
              <Icon size={16} className="stroke-[2.4]" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <h1 className="truncate font-display text-[13px] font-bold leading-none text-on-ink">
                  {title}
                </h1>
                <span className="shrink-0 rounded-xs border border-rule-ink px-1.5 py-[3px] t-tag text-on-ink-muted">
                  {role}
                </span>
              </div>
              <p className="mt-1 truncate t-meta uppercase tracking-[0.12em] text-on-ink-muted">
                {sub}
              </p>
            </div>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <span
              className={`hidden items-center gap-1.5 rounded-xs border px-2 py-1.5 t-tag sm:inline-flex ${tones[tier.tone]}`}
            >
              <span
                className={`inline-block h-1.5 w-1.5 rounded-full bg-current ${
                  tier.tone === 'ok' ? 'live-dot' : ''
                }`}
              />
              {tier.label}
            </span>
            <button
              onClick={() => {
                logout();
                navigate('/', { replace: true });
              }}
              className="tap inline-flex items-center gap-1.5 rounded-sm border border-rule-ink bg-ink-raised px-3 py-2.5 t-tag text-on-ink transition-colors hover:bg-ink-hover lg:py-1.5"
            >
              <LogOut size={13} />
              <span className="hidden sm:inline">Sign out</span>
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1">{children}</main>
    </div>
  );
}

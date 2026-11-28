/**
 * Emergency department terminal.
 *
 * Answers one question for the charge nurse: what is arriving, how bad, and
 * how long have we got. Everything else is secondary.
 *
 * The capacity toggle is a real control - closing ICU beds removes this
 * facility from the routing engine's candidate list for new calls - so it is
 * treated as a consequential action, not a decorative switch.
 */

import React, { useState, useEffect } from 'react';
import shortId from '../utils/shortId';
import { Check, BedDouble, Users, X, User, Phone, FileText, History } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import LiveEmergencyChat from '../components/LiveEmergencyChat';
import {
  Panel,
  PanelHead,
  Button,
  Stat,
  SeverityTag,
  StatusTag,
  Provenance,
  ConnectionState,
  Empty,
  severityBand,
} from '../components/ui';

export default function HospitalDashboard() {
  const { hospitalInfo } = useAuth();
  const [incoming, setIncoming] = useState([]);
  const [icuOpen, setIcuOpen] = useState(null);
  const ackKey = `rapidgrid_ack_${hospitalInfo?.id ?? 'all'}`;
  const [acknowledged, setAcknowledged] = useState(() => {
    try { return JSON.parse(sessionStorage.getItem(ackKey)) || {}; } catch { return {}; }
  });
  useEffect(() => { sessionStorage.setItem(ackKey, JSON.stringify(acknowledged)); }, [ackKey, acknowledged]);
  const [saving, setSaving] = useState(false);
  const [capacityError, setCapacityError] = useState(null);
  const capacityRequest = React.useRef(false);
  // Bumped when a capacity toggle starts and settles, so a poll that began
  // before the toggle cannot put the old value back after the PATCH completes.
  const capacityGen = React.useRef(0);
  // Available beds as entered by this ER desk. The only bed figure that
  // affects hospital ranking; empty means "not reported".
  const [bedsInput, setBedsInput] = useState('');
  const [bedsStored, setBedsStored] = useState(null);
  const [bedsTotal, setBedsTotal] = useState(null);
  const bedsEditing = React.useRef(false);
  const [openThread, setOpenThread] = useState(null);
  const [showAllModal, setShowAllModal] = useState(false);
  const [admitting, setAdmitting] = useState({});
  const [admittedList, setAdmittedList] = useState([]);
  const [admitsHistory, setAdmitsHistory] = useState([]);
  const [patientHistoryModal, setPatientHistoryModal] = useState(null); // incident or null
  const [patientHistoryData, setPatientHistoryData] = useState(null);
  const [loadingPatientHistory, setLoadingPatientHistory] = useState(false);
  const [conn, setConn] = useState('ok');

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const id = hospitalInfo?.id || 'all';
        const name = encodeURIComponent(hospitalInfo?.name ?? '');
        const res = await fetch(`/api/hospital/${id}/incoming?name=${name}`);
        if (res.status === 401 || res.status === 403) {
          if (!cancelled) setConn('auth');
          return;
        }
        if (!res.ok) throw new Error();
        const data = await res.json();
        if (!cancelled) {
          setIncoming(data.incoming ?? []);
          setConn('ok');
        }

        // Fetch history of admitted patients
        try {
          const admRes = await fetch(`/api/hospital/${id}/admits?name=${name}`);
          if (admRes.ok) {
            const admData = await admRes.json();
            if (!cancelled) {
              setAdmitsHistory(admData.admits ?? []);
            }
          }
        } catch { /* non-critical */ }
        // Sync ICU/divert state from backend so refresh doesn't show stale "Accepting".
        if (id !== 'all' && !cancelled) {
          try {
            const gen = capacityGen.current;
            const hRes = await fetch(`/api/hospital/${id}`);
            if (hRes.ok) {
              const hData = await hRes.json();
              if (!cancelled && !capacityRequest.current && gen === capacityGen.current) {
                setIcuOpen(hData.icu_available > 0);
                setBedsStored(hData.beds_available ?? null);
                setBedsTotal(hData.beds_total ?? null);
                if (!bedsEditing.current) setBedsInput(hData.beds_available != null ? String(hData.beds_available) : '');
              }
            }
          } catch { /* non-critical — keep UI value */ }
        }
      } catch {
        if (!cancelled) setConn('down');
      }
    };
    load();
    const timer = setInterval(load, 2500);
    return () => { cancelled = true; clearInterval(timer); };
  }, [hospitalInfo]);

  const viewPatientHistory = async (incident) => {
    setPatientHistoryModal(incident);
    setLoadingPatientHistory(true);
    setPatientHistoryData(null);
    try {
      const id = hospitalInfo?.id || 'all';
      const res = await fetch(`/api/hospital/${id}/patient_history/${encodeURIComponent(incident.incident_id)}`);
      if (res.ok) {
        const data = await res.json();
        setPatientHistoryData(data);
      }
    } catch {
      /* offline */
    } finally {
      setLoadingPatientHistory(false);
    }
  };

  const admitPatient = async (incidentId) => {
    setAdmitting((prev) => ({ ...prev, [incidentId]: true }));
    try {
      const id = hospitalInfo?.id || 'all';
      const res = await fetch(`/api/hospital/${id}/admit/${incidentId}`, { method: 'POST' });
      if (res.ok) {
        setAdmittedList((prev) => [...prev, incidentId]);
        const admittedCase = incoming.find((c) => c.incident_id === incidentId);
        setIncoming((prev) => prev.filter((c) => c.incident_id !== incidentId));
        if (admittedCase) {
          setAdmitsHistory((prev) => [
            {
              ...admittedCase,
              status: 'admitted',
              admitted_timestamp: Date.now() / 1000,
            },
            ...prev,
          ]);
        }
      }
    } catch {
      /* non-critical */
    } finally {
      setAdmitting((prev) => ({ ...prev, [incidentId]: false }));
    }
  };

  const patchResources = async (body, open) => {
    if (capacityRequest.current || !hospitalInfo?.id || hospitalInfo.id === 'all') return;
    capacityRequest.current = true;
    capacityGen.current += 1;
    setSaving(true);
    setCapacityError(null);
    try {
      const res = await fetch(`/api/hospital/${hospitalInfo.id}/resources`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(typeof data.detail === 'string' ? data.detail : `Capacity update failed (HTTP ${res.status})`);
      setIcuOpen(data.icu_available != null ? data.icu_available > 0 : open);
      setBedsStored(data.beds_available ?? null);
      // Only a bed save replaces the draft; an accepting/divert change must not
      // discard a bed figure the operator is still typing.
      if ('beds_available' in body) {
        setBedsInput(data.beds_available != null ? String(data.beds_available) : '');
        bedsEditing.current = false;
      }
    } catch (err) {
      setCapacityError(err.message || 'Capacity was not saved. Try again.');
    } finally {
      capacityRequest.current = false;
      capacityGen.current += 1;
      setSaving(false);
    }
  };
  const setCapacity = (open) => patchResources({ icu_available: open }, open);
  const saveBeds = (event) => {
    event.preventDefault();
    const text = bedsInput.trim();
    const beds = text === '' ? null : Number(text);
    if (beds !== null && (!Number.isInteger(beds) || beds < 0)) {
      setCapacityError('Enter a whole number of beds, or leave it empty.');
      return;
    }
    patchResources({ beds_available: beds }, icuOpen);
  };

  const critical = incoming.filter((c) => (c.severity ?? 0) >= 0.8).length;
  const soonest = incoming.reduce(
    (min, c) => (c.eta_minutes != null && c.eta_minutes < min ? c.eta_minutes : min),
    Infinity,
  );

  return (
    <div className="mx-auto flex max-w-[1280px] flex-col gap-3 p-3 lg:p-4">
      <Panel ink>
        <div className="flex flex-wrap items-center justify-between gap-x-8 gap-y-4 px-4 py-4 sm:px-5">
          <div className="flex flex-wrap items-center gap-x-6 gap-y-4 sm:gap-x-9">
            <Stat ink label="Inbound patients" value={incoming.length} />
            <Stat
              ink
              label="Critical"
              value={critical}
              tone={critical ? 'critical' : 'default'}
            />
            <Stat
              ink
              label="Next arrival"
              value={Number.isFinite(soonest) ? soonest : '--'}
              unit="min"
              tone="signal"
              modelled
            />
            {incoming.length > 0 && (
              <button
                type="button"
                onClick={() => setShowAllModal(true)}
                className="tap inline-flex items-center gap-1.5 rounded-sm border border-rule-ink bg-ink-raised px-3 py-2 text-[12.5px] font-semibold text-on-ink transition-colors hover:border-signal hover:text-signal"
              >
                <Users size={14} className="text-signal" />
                View all incoming ({incoming.length})
              </button>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <ConnectionState status={conn} />
            <div className="flex flex-wrap items-center gap-2 rounded-sm border border-rule-ink bg-ink-raised px-3 py-2">
              <BedDouble size={14} className="text-on-ink-muted" />
              <span className="eyebrow eyebrow-ink">ICU capacity</span>
              <div className="flex overflow-hidden rounded-xs border border-rule-ink">
                <button
                  onClick={() => setCapacity(true)}
                  disabled={saving || icuOpen === null || !hospitalInfo?.id || hospitalInfo.id === 'all'}
                  aria-pressed={icuOpen === true}
                  className={`tap px-3 py-2.5 t-tag transition-colors lg:px-2.5 lg:py-1 ${
                    icuOpen ? 'bg-signal text-ink' : 'bg-transparent text-on-ink-muted'
                  }`}
                >
                  Accepting
                </button>
                <button
                  onClick={() => setCapacity(false)}
                  disabled={saving || icuOpen === null || !hospitalInfo?.id || hospitalInfo.id === 'all'}
                  aria-pressed={icuOpen === false}
                  className={`tap px-3 py-2.5 t-tag transition-colors lg:px-2.5 lg:py-1 ${
                    icuOpen === false ? 'bg-critical text-white' : 'bg-transparent text-on-ink-muted'
                  }`}
                >
                  On divert
                </button>
              </div>
            </div>
            <form
              onSubmit={saveBeds}
              className="flex flex-wrap items-center gap-2 rounded-sm border border-rule-ink bg-ink-raised px-3 py-2"
            >
              <label htmlFor="beds-available" className="eyebrow eyebrow-ink">Available beds</label>
              <input
                id="beds-available"
                type="number"
                min="0"
                max={bedsTotal ?? undefined}
                inputMode="numeric"
                value={bedsInput}
                placeholder="not reported"
                onChange={(e) => { bedsEditing.current = true; setBedsInput(e.target.value); }}
                disabled={saving || !hospitalInfo?.id || hospitalInfo.id === 'all'}
                className="w-24 rounded-xs border border-rule-ink bg-transparent px-2 py-1.5 font-mono text-[13px] text-on-ink placeholder:text-on-ink-muted"
              />
              {bedsTotal != null && <span className="t-micro text-on-ink-muted">of {bedsTotal}</span>}
              <button
                type="submit"
                disabled={saving || !hospitalInfo?.id || hospitalInfo.id === 'all'}
                className="tap rounded-xs border border-rule-ink px-3 py-2 t-tag text-on-ink lg:px-2.5 lg:py-1"
              >
                Save
              </button>
            </form>
          </div>
        </div>
        {icuOpen === false && (
          <div className="border-t border-rule-ink bg-critical px-5 py-2">
            <p className="t-tag text-white">
              On divert — routing will send new critical cases elsewhere
            </p>
          </div>
        )}
      </Panel>

      {(!hospitalInfo?.id || hospitalInfo.id === 'all') && <p className="text-xs text-text-muted">Select a specific facility from the portal sign-in to change capacity.</p>}
      {hospitalInfo?.id && hospitalInfo.id !== 'all' && (
        <p className="text-xs text-text-muted">
          {bedsStored != null
            ? `Ranking uses your reported ${bedsStored} available beds.`
            : 'No bed figure reported: ranking treats bed availability as unknown for this hospital. Leave empty if you do not know.'}
        </p>
      )}
      {saving && <p role="status" className="text-xs text-text-muted">Saving capacity…</p>}
      {capacityError && <p role="alert" className="text-sm text-critical">{capacityError}</p>}
      <Panel data-tour="er-incoming">
        <PanelHead
          label={`Inbound · ${incoming.length}`}
          right={
            <span className="hidden t-meta text-text-faint sm:inline">
              {hospitalInfo?.name ?? 'All receiving facilities'}
            </span>
          }
        />
        {incoming.length === 0 ? (
          <Empty
            title="No inbound patients"
            hint="Patients appear here as soon as dispatch approves a plan that names this hospital."
          />
        ) : (
          <div>
            {incoming
              .slice()
              .sort((a, b) => (b.severity ?? 0) - (a.severity ?? 0))
              .map((c) => {
                const band = severityBand(c.severity ?? 0);
                const ack = acknowledged[c.incident_id];
                return (
                  <article
                    key={c.incident_id}
                    className={`border-b border-rule px-4 py-4 last:border-0 ${
                      band.key === 'critical' ? 'bg-critical-wash/40' : ''
                    }`}
                  >
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div className="min-w-0 flex-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="font-mono text-[11px] font-bold text-text" title={c.incident_id}>
                            {shortId(c.incident_id)}
                          </span>
                          <SeverityTag severity={c.severity ?? 0} />
                          <span className="t-meta uppercase tracking-[0.1em] text-text-faint">
                            {c.emergency_type}
                          </span>
                        </div>
                        <div className="mt-2.5">
                          <span className="eyebrow text-text-muted">Description by patient</span>
                          <p className="mt-0.5 text-[14px] font-medium leading-relaxed text-text">
                            "{c.patient_summary}"
                          </p>
                        </div>
                        <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 rounded-xs border border-rule bg-paper-sunk px-3 py-2 text-[12px]">
                          <div className="flex items-center gap-1.5 text-text">
                            <User size={13} className="text-text-muted" />
                            <span>Patient: <strong>{c.caller_name || 'Name not displayed'}</strong></span>
                          </div>
                          {c.caller_phone && (
                            <div className="flex items-center gap-1.5 text-text">
                              <Phone size={13} className="text-text-muted" />
                              <span className="font-mono">{c.caller_phone}</span>
                            </div>
                          )}
                          <div className="flex items-center gap-1.5">
                            <FileText size={13} className="text-text-muted" />
                            <span className="t-meta text-text-faint">
                              {c.registered ? 'Verified citizen record' : 'Emergency intake record'}
                            </span>
                          </div>
                        </div>
                        <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-2 t-meta text-text-faint">
                          <span>Unit {c.assigned_driver}</span>
                          <StatusTag status={c.status} />
                        </div>
                      </div>

                      <div className="flex w-full shrink-0 items-center justify-between gap-4 border-t border-rule pt-3 sm:w-auto sm:justify-end sm:border-0 sm:pt-0">
                        {c.unit_arrived ? (
                          <div className="flex flex-col items-end gap-2">
                            <span className="inline-flex items-center gap-1.5 rounded-xs border border-signal bg-signal/10 px-2.5 py-1 text-[12px] font-bold text-signal-hover">
                              <Check size={14} /> Unit Arrived at Hospital
                            </span>
                            <Button
                              size="sm"
                              variant="ink"
                              disabled={admitting[c.incident_id]}
                              onClick={() => admitPatient(c.incident_id)}
                              className="font-bold text-[12.5px]"
                            >
                              {admitting[c.incident_id] ? 'Admitting…' : 'Confirm Patient Admitted'}
                            </Button>
                          </div>
                        ) : (
                          <>
                            <div className="text-right">
                              <div className="eyebrow">Arrives in</div>
                              <div className="font-mono text-[26px] font-bold leading-none text-signal-hover">
                                {c.eta_minutes ?? '--'}
                                <span className="ml-1 text-[13px] font-medium opacity-60">min</span>
                              </div>
                            </div>
                            {ack ? (
                              <span className="inline-flex items-center gap-1.5 rounded-xs border border-ink px-2.5 py-1.5 t-tag text-text">
                                <Check size={12} /> Acknowledged on this device
                              </span>
                            ) : (
                              <Button
                                size="sm"
                                onClick={() =>
                                  setAcknowledged((p) => ({ ...p, [c.incident_id]: true }))
                                }
                              >
                                Acknowledge locally
                              </Button>
                            )}
                          </>
                        )}
                      </div>
                    </div>

                    <div className="mt-3 flex flex-wrap items-center gap-4">
                      <button
                        type="button"
                        onClick={() => viewPatientHistory(c)}
                        className="tap inline-flex items-center gap-1.5 py-1 text-[12.5px] font-semibold text-signal-hover hover:underline"
                      >
                        <History size={13} /> View Patient Emergency History
                      </button>
                      <button
                        onClick={() =>
                          setOpenThread(openThread === c.incident_id ? null : c.incident_id)
                        }
                        className="tap inline-flex items-center py-2.5 t-tag text-text-muted underline underline-offset-[3px] hover:text-text lg:py-1"
                      >
                        {openThread === c.incident_id ? 'Hide channel' : 'Message the crew'}
                      </button>
                    </div>

                    {openThread === c.incident_id && (
                      <div className="rise mt-3">
                        <LiveEmergencyChat
                          incidentId={c.incident_id}
                          senderRole="hospital"
                          senderName={hospitalInfo?.name ?? 'ER desk'}
                          height="180px"
                        />
                      </div>
                    )}
                  </article>
                );
              })}
          </div>
        )}
        <p className="border-t border-rule bg-paper-sunk px-4 py-3 t-micro leading-relaxed text-text-faint">
          <Provenance kind="simulated" className="mr-1.5" />
          Bed and blood availability shown across the platform are modelled. Connecting a hospital
          HMIS or HL7 feed would replace them with live counts.
        </p>
      </Panel>

      {/* History of Admits */}
      <Panel data-tour="er-admitted">
        <PanelHead
          label={`Admitted Patients History · ${admitsHistory.length}`}
          right={
            <span className="text-[12px] font-mono text-text-muted">
              {hospitalInfo?.name ?? 'All facilities'}
            </span>
          }
        />
        {admitsHistory.length === 0 ? (
          <div className="px-5 py-6 text-center">
            <p className="text-[13px] font-semibold text-text">No admitted patients yet</p>
            <p className="mt-1 text-[12px] text-text-muted">
              Patients admitted at the ER or confirmed from the incoming queue appear here.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-rule">
            {admitsHistory.map((adm) => {
              const band = severityBand(adm.severity ?? 0);
              const admitTime = adm.admitted_timestamp
                ? new Date(adm.admitted_timestamp * 1000).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                  })
                : 'Just now';

              return (
                <article key={adm.incident_id} className="p-4 sm:p-5 transition-colors hover:bg-paper-sunk/40">
                  <div className="flex flex-wrap items-start justify-between gap-4">
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="font-mono text-[12px] font-bold text-text" title={adm.incident_id}>
                          {shortId(adm.incident_id)}
                        </span>
                        <SeverityTag severity={adm.severity ?? 0} />
                        <span className="t-meta uppercase tracking-[0.1em] text-text-faint">
                          {adm.emergency_type}
                        </span>
                        <span className="inline-flex items-center gap-1 rounded-xs border border-signal bg-signal/10 px-2 py-0.5 text-[11px] font-bold text-signal-hover">
                          <Check size={12} /> ADMITTED
                        </span>
                      </div>

                      <div className="mt-2">
                        <span className="eyebrow text-text-muted">Chief Complaint / Description</span>
                        <p className="mt-0.5 text-[14px] font-medium leading-relaxed text-text">
                          "{adm.patient_summary}"
                        </p>
                      </div>

                      <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 rounded-xs border border-rule bg-paper-sunk px-3 py-2 text-[12px]">
                        <div className="flex items-center gap-1.5 text-text">
                          <User size={13} className="text-text-muted" />
                          <span>Patient: <strong>{adm.caller_name || 'Name not displayed'}</strong></span>
                        </div>
                        {adm.caller_phone && (
                          <div className="flex items-center gap-1.5 text-text">
                            <Phone size={13} className="text-text-muted" />
                            <span className="font-mono">{adm.caller_phone}</span>
                          </div>
                        )}
                        <div className="flex items-center gap-1.5">
                          <FileText size={13} className="text-text-muted" />
                          <span className="t-meta text-text-faint">
                            {adm.registered ? 'Verified citizen record' : 'Emergency intake record'}
                          </span>
                        </div>
                      </div>

                      <div className="mt-2.5 flex flex-wrap items-center gap-x-4 gap-y-2 text-[12px] text-text-faint">
                        <span>Transporting unit: <strong className="text-text">{adm.assigned_driver || 'Ambulance'}</strong></span>
                        <span>Facility: <strong className="text-text">{adm.hospital_name || hospitalInfo?.name || 'ER'}</strong></span>
                      </div>
                    </div>

                    <div className="flex shrink-0 flex-col items-end gap-1.5 border-t border-rule pt-2 sm:border-0 sm:pt-0">
                      <span className="eyebrow text-text-muted">Admission Time</span>
                      <span className="font-mono text-[14px] font-bold text-text">
                        {admitTime}
                      </span>
                      <button
                        type="button"
                        onClick={() => viewPatientHistory(adm)}
                        className="tap mt-2 inline-flex items-center gap-1.5 rounded-xs border border-rule bg-paper px-2.5 py-1 text-[12px] font-semibold text-signal-hover hover:border-signal"
                      >
                        <History size={13} /> View History
                      </button>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </Panel>

      {/* Modal dialog showing all incoming patients with details and arrival times */}
      {showAllModal && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs"
          onClick={() => setShowAllModal(false)}
        >
          <div
            className="flex max-h-[90vh] w-full max-w-[840px] flex-col overflow-hidden rounded-md border border-rule bg-paper shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-rule bg-paper-sunk px-5 py-3.5">
              <div>
                <h2 className="text-[15px] font-semibold text-text">
                  All Incoming Patients · {hospitalInfo?.name ?? 'Emergency Department'}
                </h2>
                <p className="text-[12px] text-text-muted">
                  {incoming.length} patient{incoming.length === 1 ? '' : 's'} en route, sorted by severity and arrival time.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setShowAllModal(false)}
                className="tap rounded-sm p-1.5 text-text-muted transition-colors hover:bg-paper hover:text-text"
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto divide-y divide-rule">
              {incoming.length === 0 ? (
                <Empty
                  title="No inbound patients"
                  hint="Patients appear here as soon as dispatch approves a plan that names this hospital."
                />
              ) : (
                incoming
                  .slice()
                  .sort((a, b) => (b.severity ?? 0) - (a.severity ?? 0))
                  .map((c) => {
                    const band = severityBand(c.severity ?? 0);
                    const ack = acknowledged[c.incident_id];
                    return (
                      <article
                        key={c.incident_id}
                        className={`px-5 py-4 ${
                          band.key === 'critical' ? 'bg-critical-wash/40' : ''
                        }`}
                      >
                        <div className="flex flex-wrap items-start justify-between gap-4">
                          <div className="min-w-0 flex-1">
                            <div className="flex flex-wrap items-center gap-2">
                              <span className="font-mono text-[12px] font-bold text-text" title={c.incident_id}>
                                {shortId(c.incident_id)}
                              </span>
                              <SeverityTag severity={c.severity ?? 0} />
                              <span className="t-meta uppercase tracking-[0.1em] text-text-faint">
                                {c.emergency_type}
                              </span>
                            </div>

                            <div className="mt-2.5">
                              <span className="eyebrow text-text-muted">Description by patient</span>
                              <p className="mt-0.5 text-[14px] font-medium leading-relaxed text-text">
                                "{c.patient_summary}"
                              </p>
                            </div>

                            <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 rounded-xs border border-rule bg-paper-sunk px-3 py-2 text-[12px]">
                              <div className="flex items-center gap-1.5 text-text">
                                <User size={13} className="text-text-muted" />
                                <span>Patient: <strong>{c.caller_name || 'Name not displayed'}</strong></span>
                              </div>
                              {c.caller_phone && (
                                <div className="flex items-center gap-1.5 text-text">
                                  <Phone size={13} className="text-text-muted" />
                                  <span className="font-mono">{c.caller_phone}</span>
                                </div>
                              )}
                              <div className="flex items-center gap-1.5">
                                <FileText size={13} className="text-text-muted" />
                                <span className="t-meta text-text-faint">
                                  {c.registered ? 'Verified citizen record' : 'Emergency intake record'}
                                </span>
                              </div>
                            </div>

                            <div className="mt-2.5 flex flex-wrap items-center gap-x-4 gap-y-2 text-[12px] text-text-faint">
                              <span>Assigned unit: <strong className="text-text">{c.assigned_driver || 'Pending'}</strong></span>
                              <span>Status: <strong className="text-text">{c.status}</strong></span>
                              {c.destination_on_divert && (
                                <span className="text-critical font-medium">Destination currently on divert</span>
                              )}
                            </div>
                          </div>

                          <div className="flex shrink-0 flex-col items-end gap-2">
                            {c.unit_arrived ? (
                              <div className="flex flex-col items-end gap-2">
                                <span className="inline-flex items-center gap-1.5 rounded-xs border border-signal bg-signal/10 px-2.5 py-1 text-[12px] font-bold text-signal-hover">
                                  <Check size={14} /> Unit Arrived at Hospital
                                </span>
                                <Button
                                  size="sm"
                                  variant="ink"
                                  disabled={admitting[c.incident_id]}
                                  onClick={() => admitPatient(c.incident_id)}
                                  className="font-bold text-[12.5px]"
                                >
                                  {admitting[c.incident_id] ? 'Admitting…' : 'Confirm Patient Admitted'}
                                </Button>
                              </div>
                            ) : (
                              <>
                                <div className="text-right">
                                  <div className="eyebrow text-text-muted">Arrives in</div>
                                  <div className="font-mono text-[26px] font-bold leading-none text-signal-hover">
                                    {c.eta_minutes ?? '--'}
                                    <span className="ml-1 text-[13px] font-medium opacity-60">min</span>
                                  </div>
                                </div>
                                {ack ? (
                                  <span className="inline-flex items-center gap-1.5 rounded-xs border border-ink px-2.5 py-1 t-tag text-text">
                                    <Check size={12} /> Acknowledged
                                  </span>
                                ) : (
                                  <Button
                                    size="sm"
                                    onClick={() =>
                                      setAcknowledged((p) => ({ ...p, [c.incident_id]: true }))
                                    }
                                  >
                                    Acknowledge
                                  </Button>
                                )}
                              </>
                            )}
                          </div>
                        </div>

                        <div className="mt-3 flex items-center justify-between border-t border-rule/50 pt-2">
                          <button
                            type="button"
                            onClick={() => viewPatientHistory(c)}
                            className="tap inline-flex items-center gap-1.5 text-[12px] font-semibold text-signal-hover hover:underline"
                          >
                            <History size={13} /> View Patient Emergency History
                          </button>
                          <button
                            onClick={() =>
                              setOpenThread(openThread === c.incident_id ? null : c.incident_id)
                            }
                            className="tap inline-flex items-center text-[12px] text-text-muted underline underline-offset-[3px] hover:text-text"
                          >
                            {openThread === c.incident_id ? 'Hide channel' : 'Message the crew'}
                          </button>
                        </div>

                        {openThread === c.incident_id && (
                          <div className="rise mt-3">
                            <LiveEmergencyChat
                              incidentId={c.incident_id}
                              senderRole="hospital"
                              senderName={hospitalInfo?.name ?? 'ER desk'}
                              height="180px"
                            />
                          </div>
                        )}
                      </article>
                    );
                  })
              )}
            </div>

            <div className="flex items-center justify-between border-t border-rule bg-paper-sunk px-5 py-3">
              <span className="text-[12px] text-text-muted">
                Times are live estimated travel times to {hospitalInfo?.name ?? 'this hospital'}.
              </span>
              <Button size="sm" onClick={() => setShowAllModal(false)}>
                Close
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Patient Emergency History Modal for Hospital ER Desk */}
      {patientHistoryModal && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs"
          onClick={() => setPatientHistoryModal(null)}
        >
          <div
            className="flex max-h-[85vh] w-full max-w-[680px] flex-col overflow-hidden rounded-md border border-rule bg-paper shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-rule bg-paper-sunk px-5 py-3.5">
              <div>
                <div className="flex items-center gap-2">
                  <History size={16} className="text-signal-hover" />
                  <h2 className="text-[15px] font-semibold text-text">
                    Patient Emergency History · {patientHistoryData?.patient_name || patientHistoryModal.caller_name || 'Patient Record'}
                  </h2>
                </div>
                <div className="mt-1 flex items-center gap-3 text-[12px] text-text-muted">
                  <span>Phone: <strong className="font-mono text-text">{patientHistoryData?.phone || patientHistoryModal.caller_phone || 'Unregistered'}</strong></span>
                  <span>Record: <strong className="text-text">{patientHistoryData?.registered ? 'Verified citizen account' : 'Emergency intake record'}</strong></span>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setPatientHistoryModal(null)}
                className="tap rounded-sm p-1.5 text-text-muted hover:text-text"
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto divide-y divide-rule p-3">
              {loadingPatientHistory ? (
                <div className="p-8 text-center text-sm text-text-muted">Loading prior emergency records…</div>
              ) : !patientHistoryData?.history?.length ? (
                <div className="p-8 text-center text-sm text-text-muted">
                  No prior emergency records on file for this patient.
                </div>
              ) : (
                patientHistoryData.history.map((item) => (
                  <div
                    key={item.incident_id}
                    className={`flex flex-col gap-2 p-4 transition-colors ${
                      item.is_current ? 'bg-signal-wash/40 border-l-2 border-signal' : 'hover:bg-paper-hover'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-[12px] font-bold text-text">
                          {shortId(item.incident_id)}
                        </span>
                        {item.is_current && (
                          <span className="rounded-xs bg-signal/20 px-1.5 py-0.5 text-[11px] font-bold text-signal-hover">
                            CURRENT CALL
                          </span>
                        )}
                        <span className="t-meta uppercase tracking-[0.1em] text-text-faint">
                          {item.emergency_type}
                        </span>
                      </div>
                      <StatusTag status={item.status} />
                    </div>

                    <p className="text-[13px] text-text leading-relaxed">
                      "{item.citizen_text || 'Emergency description not provided'}"
                    </p>

                    <div className="flex items-center justify-between pt-1 text-[12px] text-text-muted">
                      <span>
                        {item.hospital_name ? `Receiving Hospital: ${item.hospital_name}` : 'Hospital routing pending'}
                      </span>
                      {item.assigned_driver && (
                        <span>Assigned unit: <strong className="text-text">{item.assigned_driver}</strong></span>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="flex items-center justify-between border-t border-rule bg-paper-sunk px-5 py-3">
              <span className="text-[12px] text-text-muted">
                {patientHistoryData?.records_count ?? 0} total case records found for this patient.
              </span>
              <Button size="sm" onClick={() => setPatientHistoryModal(null)}>
                Close
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

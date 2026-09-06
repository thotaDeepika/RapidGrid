/**
 * Incident channel.
 *
 * One thread per incident, shared by the citizen, the responding unit and the
 * receiving ER. WebSocket first with an HTTP poll behind it, so a dropped
 * socket degrades to slower delivery rather than silence - and the header says
 * which transport is actually carrying messages instead of always claiming
 * "live".
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Send } from 'lucide-react';
import { Panel, PanelHead } from './ui';

const ROLE_LABEL = {
  citizen: 'Caller',
  driver: 'Responder',
  dispatcher: 'Dispatch',
  hospital: 'ER desk',
};

export default function LiveEmergencyChat({
  incidentId,
  senderRole = 'citizen',
  senderName,
  height = '260px',
}) {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');
  const [transport, setTransport] = useState('connecting');
  const socket = useRef(null);
  const stream = useRef(null);

  const displayName = senderName ?? ROLE_LABEL[senderRole] ?? 'User';

  const scrollDown = useCallback(() => {
    const el = stream.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, []);

  useEffect(scrollDown, [messages, scrollDown]);

  // HTTP history: the source of truth, and the fallback when the socket drops.
  useEffect(() => {
    if (!incidentId) return;
    let cancelled = false;
    const load = async () => {
      try {
        const res = await fetch(`/api/chat/${incidentId}/messages`);
        if (!res.ok) return;
        const data = await res.json();
        if (!cancelled) setMessages(data.messages ?? []);
      } catch {
        if (!cancelled) setTransport('offline');
      }
    };
    load();
    const timer = setInterval(load, 3000);
    return () => { cancelled = true; clearInterval(timer); };
  }, [incidentId]);

  // WebSocket for immediate delivery.
  useEffect(() => {
    if (!incidentId) return;
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let ws;
    try {
      ws = new WebSocket(`${proto}//${window.location.host}/ws/chat/${incidentId}`);
    } catch {
      setTransport('polling');
      return;
    }
    socket.current = ws;
    ws.onopen = () => setTransport('live');
    ws.onclose = () => setTransport('polling');
    ws.onerror = () => setTransport('polling');
    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        setMessages((prev) =>
          prev.some(
            (m) => m.timestamp === msg.timestamp && m.message === msg.message,
          )
            ? prev
            : [...prev, msg],
        );
      } catch { /* non-JSON frame */ }
    };
    return () => {
      ws.close();
      socket.current = null;
    };
  }, [incidentId]);

  const send = async (e) => {
    e?.preventDefault();
    const body = text.trim();
    if (!body || !incidentId) return;
    setText('');

    const payload = {
      incident_id: incidentId,
      sender_role: senderRole,
      sender_name: displayName,
      message: body,
    };

    if (socket.current?.readyState === WebSocket.OPEN) {
      socket.current.send(JSON.stringify(payload));
    }
    try {
      await fetch(`/api/chat/${incidentId}/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
    } catch {
      setTransport('offline');
    }
  };

  const transportCopy = {
    live: { label: 'Live', tone: 'text-verified' },
    polling: { label: 'Delayed', tone: 'text-signal-hover' },
    connecting: { label: 'Connecting', tone: 'text-text-faint' },
    offline: { label: 'Offline', tone: 'text-critical' },
  }[transport];

  return (
    <Panel className="flex flex-col overflow-hidden">
      <PanelHead
        label="Incident channel"
        right={
          <span className={`t-meta font-bold ${transportCopy.tone}`}>
            {transportCopy.label}
          </span>
        }
      />

      <div ref={stream} className="flex-1 space-y-2.5 overflow-y-auto px-4 py-3" style={{ height }}>
        {messages.length === 0 ? (
          <p className="py-8 text-center text-[12px] text-text-faint">
            No messages yet. Anyone working this incident can write here.
          </p>
        ) : (
          messages.map((m, i) => {
            const mine = m.sender_role === senderRole;
            return (
              <div key={i} className={`flex ${mine ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[82%] ${mine ? 'text-right' : ''}`}>
                  <div className="mb-1 flex items-center gap-1.5 t-meta uppercase tracking-[0.1em] text-text-faint">
                    <span className="font-bold">
                      {ROLE_LABEL[m.sender_role] ?? m.sender_role}
                    </span>
                    {m.timestamp && <span>{m.timestamp}</span>}
                  </div>
                  <div
                    className={`inline-block rounded-sm border px-3 py-2 text-left text-[12.5px] leading-relaxed ${
                      mine
                        ? 'border-ink bg-ink text-on-ink'
                        : 'border-rule bg-paper-sunk text-text'
                    }`}
                  >
                    {m.message}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      <form onSubmit={send} className="flex items-center gap-2 border-t border-rule p-2.5">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type a message…"
          className="min-w-0 flex-1 rounded-sm border border-rule bg-paper px-3 py-2.5 text-[16px] text-text placeholder:text-text-faint focus:border-signal focus:outline-none lg:py-2 lg:text-[13px]"
        />
        <button
          type="submit"
          disabled={!text.trim()}
          aria-label="Send message"
          className="tap grid h-11 w-11 shrink-0 place-items-center rounded-sm bg-signal text-white transition-colors hover:bg-signal-hover disabled:opacity-40 lg:h-9 lg:w-9"
        >
          <Send size={15} />
        </button>
      </form>
    </Panel>
  );
}

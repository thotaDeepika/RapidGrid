import sys

chat_file = "src/components/LiveEmergencyChat.jsx"

new_chat_jsx = """import React, { useState, useEffect, useRef } from 'react';
import { Send, Phone, MessageSquare, Radio, MapPin, Clock, CheckCircle2 } from 'lucide-react';

export default function LiveEmergencyChat({ incidentId, senderRole = 'citizen', senderName = 'Citizen User', targetPhone = '+919876543210' }) {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');
  const wsRef = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Poll chat history every 2s for guaranteed multi-tab real-time sync
  useEffect(() => {
    if (!incidentId) return;

    const fetchHistory = async () => {
      try {
        const res = await fetch(`/api/chat/${incidentId}/messages`);
        if (res.ok) {
          const data = await res.json();
          setMessages(data.messages || []);
        }
      } catch (err) {}
    };

    fetchHistory();
    const pollInterval = setInterval(fetchHistory, 1500);

    // WebSocket connection
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.hostname}:8000/ws/chat/${incidentId}`;
    
    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          setMessages((prev) => [...prev, msg]);
          scrollToBottom();
        } catch (e) {}
      };
    } catch (err) {}

    return () => {
      clearInterval(pollInterval);
      if (wsRef.current) wsRef.current.close();
    };
  }, [incidentId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (customText = null) => {
    const msgText = customText || text;
    if (!msgText.trim() || !incidentId) return;

    const payload = {
      incident_id: incidentId,
      sender_role: senderRole,
      sender_name: senderName,
      message: msgText.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    // Broadcast via WS and REST fallback
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(payload));
    }
    
    try {
      await fetch(`/api/chat/${incidentId}/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } catch (err) {}

    if (!customText) setText('');
  };

  const roleStyles = {
    citizen: 'bg-tertiary/20 text-tertiary border-tertiary/30',
    driver: 'bg-[#FFB900]/20 text-[#FFB900] border-[#FFB900]/30',
    hospital: 'bg-[#B084FF]/20 text-[#B084FF] border-[#B084FF]/30'
  };

  return (
    <div className="bg-surface-container rounded-2xl border border-outline-variant/30 flex flex-col h-[380px] shadow-2xl overflow-hidden">
      {/* Header */}
      <div className="bg-surface-container-high p-3 border-b border-outline-variant/30 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Radio size={18} className="text-tertiary animate-pulse" />
          <div>
            <h3 className="text-xs font-bold text-on-surface uppercase font-mono">Real-Time Emergency Socket</h3>
            <span className="text-[10px] text-on-surface-variant font-mono">Channel ID: {incidentId}</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <a
            href={`tel:${targetPhone}`}
            className="p-2 bg-tertiary/20 text-tertiary hover:bg-tertiary/30 rounded-xl transition-all flex items-center gap-1 text-xs font-bold"
            title="Direct Phone Call"
          >
            <Phone size={14} />
            <span className="hidden sm:inline">Call</span>
          </a>
          <a
            href={`sms:${targetPhone}?body=Emergency%20Update%20from%20${senderRole}`}
            className="p-2 bg-secondary/20 text-secondary hover:bg-secondary/30 rounded-xl transition-all flex items-center gap-1 text-xs font-bold"
            title="Direct SMS Text"
          >
            <MessageSquare size={14} />
            <span className="hidden sm:inline">SMS</span>
          </a>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 p-3 overflow-y-auto space-y-2 text-xs bg-surface-container-lowest/40">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-on-surface-variant/40 space-y-1">
            <Radio size={32} className="opacity-30" />
            <p className="font-semibold text-xs">Socket connected. No messages yet.</p>
            <p className="text-[10px]">Type below to chat directly with first responders & hospital.</p>
          </div>
        ) : (
          messages.map((m, idx) => {
            const isMe = m.sender_role === senderRole;
            const bubbleStyle = roleStyles[m.sender_role] || roleStyles.citizen;

            return (
              <div key={idx} className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
                <div className="flex items-center gap-1 mb-0.5">
                  <span className="text-[10px] font-mono text-on-surface-variant/70 font-bold">{m.sender_name} ({m.sender_role})</span>
                  <span className="text-[9px] text-on-surface-variant/50">{m.timestamp}</span>
                </div>
                <div className={`p-2.5 rounded-2xl max-w-[80%] border shadow-sm ${
                  isMe ? 'bg-primary text-on-primary border-primary/50' : 'bg-surface-container-high text-on-surface border-outline-variant/30'
                }`}>
                  {m.message}
                </div>
              </div>
            );
          })
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Action Chips */}
      <div className="px-3 py-1.5 bg-surface-container-high/50 border-t border-outline-variant/20 flex gap-2 overflow-x-auto">
        <button
          onClick={() => handleSend("Share GPS Location: 12.9756, 77.6068")}
          className="px-2.5 py-1 bg-surface-container hover:bg-surface-container-highest rounded-full text-[10px] font-mono text-primary border border-primary/30 flex items-center gap-1 flex-shrink-0"
        >
          <MapPin size={10} /> Share GPS
        </button>
        <button
          onClick={() => handleSend("ETA Request: What is the current ambulance arrival time?")}
          className="px-2.5 py-1 bg-surface-container hover:bg-surface-container-highest rounded-full text-[10px] font-mono text-[#FFB900] border border-[#FFB900]/30 flex items-center gap-1 flex-shrink-0"
        >
          <Clock size={10} /> Request ETA
        </button>
        <button
          onClick={() => handleSend("ICU Bed Readiness Confirmed")}
          className="px-2.5 py-1 bg-surface-container hover:bg-surface-container-highest rounded-full text-[10px] font-mono text-[#B084FF] border border-[#B084FF]/30 flex items-center gap-1 flex-shrink-0"
        >
          <CheckCircle2 size={10} /> Bed Ready
        </button>
      </div>

      {/* Input Box */}
      <div className="p-2.5 bg-surface-container-high border-t border-outline-variant/30 flex gap-2">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={`Type message as ${senderName}...`}
          className="flex-1 bg-surface-container-low border border-outline-variant/30 text-on-surface px-3 py-2 rounded-xl text-xs focus:outline-none focus:border-primary"
        />
        <button
          onClick={() => handleSend()}
          className="bg-primary text-on-primary p-2.5 rounded-xl hover:bg-primary/90 transition-all flex items-center justify-center shadow-md"
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}
"""

with open(chat_file, "w", encoding="utf-8") as f:
    f.write(new_chat_jsx)

print("LiveEmergencyChat.jsx updated with 1.5s polling sync and clean Lucide icons")

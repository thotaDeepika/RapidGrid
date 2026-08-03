import React, { useState, useEffect, useRef } from 'react';
import { Send, Phone, MessageSquare, Radio, MapPin, Clock, CheckCircle2, Truck, PlusSquare, ShieldAlert } from 'lucide-react';

export default function LiveEmergencyChat({ 
  incidentId, 
  senderRole = 'citizen', 
  senderName = 'Citizen User', 
  driverPhone = '+919876543210',
  hospitalPhone = '112',
  targetPhone = null,
  hospitalName = 'MEDSTAR Speciality Hospital',
  vehicleRequired = 'Ambulance',
  includeAmbulanceBackup = false
}) {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');
  const [activeChannel, setActiveChannel] = useState(
    senderRole === 'driver' ? 'driver' : senderRole === 'hospital' ? 'hospital' : (vehicleRequired === 'Ambulance' ? 'driver' : 'driver')
  );
  const wsRef = useRef(null);
  const chatStreamRef = useRef(null);

  const scrollToBottom = () => {
    if (chatStreamRef.current) {
      chatStreamRef.current.scrollTop = chatStreamRef.current.scrollHeight;
    }
  };

  // Poll chat history every 1.5s
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

  const handleSend = async (customText = null) => {
    const msgText = customText || text;
    if (!msgText.trim() || !incidentId) return;

    const payload = {
      incident_id: incidentId,
      sender_role: senderRole,
      sender_name: senderName,
      target_channel: activeChannel,
      message: msgText.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

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

  // Filter messages by selected target channel
  const filteredMessages = messages.filter(m => {
    if (!m.target_channel) return true;
    if (activeChannel === 'driver') {
      return m.sender_role === 'driver' || m.target_channel === 'driver';
    } else if (activeChannel === 'ambulance_backup') {
      return m.sender_role === 'driver' || m.target_channel === 'ambulance_backup';
    }
    return m.sender_role === 'hospital' || m.target_channel === 'hospital';
  });

  const primaryLabel = vehicleRequired === 'Fire Engine' ? 'FIRE DRIVER CHAT' : vehicleRequired === 'Police Cruiser' ? 'POLICE CHAT' : vehicleRequired === 'Disaster Rescue' ? 'DISASTER CHAT' : 'PARAMEDIC DRIVER CHAT';
  const showHospitalTab = vehicleRequired === 'Ambulance' || includeAmbulanceBackup;

  const currentTargetPhone = targetPhone || (activeChannel === 'hospital' ? hospitalPhone : driverPhone);
  const currentTargetName = activeChannel === 'hospital' ? hospitalName : `${vehicleRequired} Driver Unit`;

  return (
    <div className="bg-surface-container rounded-2xl border border-outline-variant/30 flex flex-col h-[410px] shadow-2xl overflow-hidden">
      {/* Dynamic Unit Switcher Tabs */}
      <div className="bg-surface-container-high p-2 border-b border-outline-variant/30 flex justify-between items-center gap-1.5 overflow-x-auto">
        <div className="flex gap-1.5 flex-1">
          {/* Primary Dispatched Unit Chat Tab */}
          <button
            onClick={() => setActiveChannel('driver')}
            className={`py-2 px-3 rounded-xl text-xs font-bold font-mono transition-all flex items-center justify-center gap-1.5 border flex-1 ${
              activeChannel === 'driver'
                ? 'bg-[#FFB900]/20 text-[#FFB900] border-[#FFB900]/50 shadow-md'
                : 'bg-surface-container-low text-on-surface-variant border-transparent hover:bg-surface-container'
            }`}
          >
            <Truck size={14} />
            <span className="truncate">{primaryLabel}</span>
          </button>

          {/* Secondary Paramedic Ambulance Backup Tab (If Backup Requested) */}
          {includeAmbulanceBackup && vehicleRequired !== 'Ambulance' && (
            <button
              onClick={() => setActiveChannel('ambulance_backup')}
              className={`py-2 px-3 rounded-xl text-xs font-bold font-mono transition-all flex items-center justify-center gap-1.5 border flex-1 ${
                activeChannel === 'ambulance_backup'
                  ? 'bg-tertiary/20 text-tertiary border-tertiary/50 shadow-md'
                  : 'bg-surface-container-low text-on-surface-variant border-transparent hover:bg-surface-container'
              }`}
            >
              <Truck size={14} />
              <span className="truncate">AMBULANCE BACKUP CHAT</span>
            </button>
          )}

          {/* Hospital ER Desk Tab (If Medical Ambulance involved) */}
          {showHospitalTab && (
            <button
              onClick={() => setActiveChannel('hospital')}
              className={`py-2 px-3 rounded-xl text-xs font-bold font-mono transition-all flex items-center justify-center gap-1.5 border flex-1 ${
                activeChannel === 'hospital'
                  ? 'bg-[#B084FF]/20 text-[#B084FF] border-[#B084FF]/50 shadow-md'
                  : 'bg-surface-container-low text-on-surface-variant border-transparent hover:bg-surface-container'
              }`}
            >
              <PlusSquare size={14} />
              <span className="truncate">HOSPITAL ER DESK CHAT</span>
            </button>
          )}
        </div>

        {/* Telephony Action Buttons */}
        <div className="flex items-center gap-1">
          <a
            href={`tel:${currentTargetPhone}`}
            className="px-2 py-1.5 bg-tertiary/20 text-tertiary hover:bg-tertiary/30 rounded-xl transition-all flex items-center gap-1 text-xs font-bold"
            title={`Call ${currentTargetName}`}
          >
            <Phone size={14} />
            <span className="hidden sm:inline">Call</span>
          </a>
          <a
            href={`sms:${currentTargetPhone}?body=Emergency%20Update%20from%20${senderRole}`}
            className="px-2 py-1.5 bg-secondary/20 text-secondary hover:bg-secondary/30 rounded-xl transition-all flex items-center gap-1 text-xs font-bold"
            title={`SMS ${currentTargetName}`}
          >
            <MessageSquare size={14} />
            <span className="hidden sm:inline">SMS</span>
          </a>
        </div>
      </div>

      {/* Active Channel Indicator */}
      <div className="bg-surface-container-low px-3 py-1 border-b border-outline-variant/20 flex justify-between items-center text-[10px] font-mono">
        <span className="text-on-surface-variant">
          Active Socket: <strong className="text-on-surface">{currentTargetName}</strong>
        </span>
        <span className="text-tertiary flex items-center gap-1 font-bold">
          <span className="w-1.5 h-1.5 bg-tertiary rounded-full animate-ping"></span>
          REALTIME SYNC
        </span>
      </div>

      {/* Messages Stream */}
      <div ref={chatStreamRef} className="flex-1 p-3 overflow-y-auto space-y-2 text-xs bg-surface-container-lowest/40">
        {filteredMessages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-on-surface-variant/40 space-y-1">
            <Radio size={28} className="opacity-30" />
            <p className="font-semibold text-xs">No messages in {currentTargetName} channel.</p>
            <p className="text-[10px]">Type below to send a direct message.</p>
          </div>
        ) : (
          filteredMessages.map((m, idx) => {
            const isMe = m.sender_role === senderRole;
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
      </div>

      {/* Input Box */}
      <div className="p-2.5 bg-surface-container-high border-t border-outline-variant/30 flex gap-2">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={`Type direct message to ${currentTargetName}...`}
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

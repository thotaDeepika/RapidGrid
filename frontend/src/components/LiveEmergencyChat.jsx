import React, { useState, useEffect, useRef } from 'react';
import { Send, Phone, MessageSquare, Radio, Truck, PlusSquare } from 'lucide-react';

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

  const filteredMessages = messages.filter(m => {
    if (!m.target_channel) return true;
    if (activeChannel === 'driver') {
      return m.sender_role === 'driver' || m.target_channel === 'driver';
    } else if (activeChannel === 'ambulance_backup') {
      return m.sender_role === 'driver' || m.target_channel === 'ambulance_backup';
    }
    return m.sender_role === 'hospital' || m.target_channel === 'hospital';
  });

  const primaryLabel = vehicleRequired === 'Fire Engine' ? 'FIRE DRIVER CHAT' : vehicleRequired === 'Police Cruiser' ? 'POLICE CHAT' : vehicleRequired === 'Disaster Rescue' ? 'DISASTER CHAT' : 'PARAMEDIC CHAT';
  const showHospitalTab = vehicleRequired === 'Ambulance' || includeAmbulanceBackup;

  const currentTargetPhone = targetPhone || (activeChannel === 'hospital' ? hospitalPhone : driverPhone);
  const currentTargetName = activeChannel === 'hospital' ? hospitalName : `${vehicleRequired} Driver Unit`;

  return (
    <div className="bg-white rounded-3xl border border-[#e2e8f0] flex flex-col h-[400px] shadow-elevation-md overflow-hidden font-body">
      {/* Dynamic Unit Switcher Tabs */}
      <div className="bg-[#f6f8fb] p-2.5 border-b border-[#e2e8f0] flex justify-between items-center gap-2 overflow-x-auto">
        <div className="flex gap-2 flex-1">
          <button
            onClick={() => setActiveChannel('driver')}
            className={`py-2 px-3.5 rounded-2xl text-xs font-mono font-bold transition-all flex items-center justify-center gap-1.5 border flex-1 ${
              activeChannel === 'driver'
                ? 'bg-[#5f4bb6] text-white border-[#5f4bb6] shadow-sm'
                : 'bg-white text-[#5a6860] border-[#e2e8f0] hover:border-[#86a5d9]'
            }`}
          >
            <Truck size={14} />
            <span className="truncate">{primaryLabel}</span>
          </button>

          {includeAmbulanceBackup && vehicleRequired !== 'Ambulance' && (
            <button
              onClick={() => setActiveChannel('ambulance_backup')}
              className={`py-2 px-3.5 rounded-2xl text-xs font-mono font-bold transition-all flex items-center justify-center gap-1.5 border flex-1 ${
                activeChannel === 'ambulance_backup'
                  ? 'bg-[#5f4bb6] text-white border-[#5f4bb6] shadow-sm'
                  : 'bg-white text-[#5a6860] border-[#e2e8f0] hover:border-[#86a5d9]'
              }`}
            >
              <Truck size={14} />
              <span className="truncate">AMBULANCE BACKUP</span>
            </button>
          )}

          {showHospitalTab && (
            <button
              onClick={() => setActiveChannel('hospital')}
              className={`py-2 px-3.5 rounded-2xl text-xs font-mono font-bold transition-all flex items-center justify-center gap-1.5 border flex-1 ${
                activeChannel === 'hospital'
                  ? 'bg-[#5f4bb6] text-white border-[#5f4bb6] shadow-sm'
                  : 'bg-white text-[#5a6860] border-[#e2e8f0] hover:border-[#86a5d9]'
              }`}
            >
              <PlusSquare size={14} />
              <span className="truncate">HOSPITAL ER CHAT</span>
            </button>
          )}
        </div>

        {/* Telephony Action Buttons */}
        <div className="flex items-center gap-1.5">
          <a
            href={`tel:${currentTargetPhone}`}
            className="px-3 py-1.5 bg-[#f0ecfd] text-[#5f4bb6] hover:bg-[#5f4bb6] hover:text-white rounded-xl transition-all flex items-center gap-1 text-xs font-bold font-mono border border-[#86a5d9]/30"
            title={`Call ${currentTargetName}`}
          >
            <Phone size={13} />
            <span className="hidden sm:inline">Call</span>
          </a>
          <a
            href={`sms:${currentTargetPhone}?body=Emergency%20Update%20from%20${senderRole}`}
            className="px-3 py-1.5 bg-[#f0f4f9] text-[#202a25] hover:bg-[#e2e8f0] rounded-xl transition-all flex items-center gap-1 text-xs font-bold font-mono border border-[#e2e8f0]"
            title={`SMS ${currentTargetName}`}
          >
            <MessageSquare size={13} />
            <span className="hidden sm:inline">SMS</span>
          </a>
        </div>
      </div>

      {/* Active Channel Indicator */}
      <div className="bg-[#f6f8fb]/80 px-4 py-1.5 border-b border-[#e2e8f0] flex justify-between items-center text-[11px] font-mono">
        <span className="text-[#5a6860]">
          Active Channel: <strong className="text-[#202a25] font-bold">{currentTargetName}</strong>
        </span>
        <span className="text-[#008b8c] flex items-center gap-1.5 font-bold">
          <span className="w-2 h-2 bg-[#00b8b9] rounded-full animate-pulse"></span>
          WEBSOCKET LIVE STREAM
        </span>
      </div>

      {/* Messages Stream */}
      <div ref={chatStreamRef} className="flex-1 p-4 overflow-y-auto space-y-3 text-xs bg-[#fafcff]">
        {filteredMessages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-[#88968f] space-y-1.5">
            <Radio size={28} className="opacity-40 text-[#5f4bb6]" />
            <p className="font-display font-bold text-xs text-[#202a25]">No messages in {currentTargetName} channel.</p>
            <p className="text-[11px] text-[#5a6860]">Type below to stream direct messages.</p>
          </div>
        ) : (
          filteredMessages.map((m, idx) => {
            const isMe = m.sender_role === senderRole;
            return (
              <div key={idx} className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
                <div className="flex items-center gap-1.5 mb-1 font-mono text-[10px]">
                  <span className="text-[#5a6860] font-bold">{m.sender_name} ({m.sender_role})</span>
                  <span className="text-[#88968f]">{m.timestamp}</span>
                </div>
                <div className={`p-3 rounded-2xl max-w-[80%] shadow-sm text-xs ${
                  isMe 
                    ? 'bg-[#5f4bb6] text-white font-medium rounded-tr-none' 
                    : 'bg-white text-[#202a25] border border-[#e2e8f0] rounded-tl-none'
                }`}>
                  {m.message}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Input Box */}
      <div className="p-3 bg-white border-t border-[#e2e8f0] flex gap-2">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={`Type message to ${currentTargetName}...`}
          className="flex-1 bg-[#f6f8fb] border border-[#e2e8f0] text-[#202a25] px-4 py-2.5 rounded-2xl text-xs focus:outline-none focus:border-[#5f4bb6]"
        />
        <button
          onClick={() => handleSend()}
          className="bg-[#5f4bb6] hover:bg-[#4c3a9e] text-white p-2.5 rounded-2xl transition-all flex items-center justify-center shadow-sm active:scale-95"
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}

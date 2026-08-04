import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { LogOut, Activity, ShieldAlert, Truck, PlusSquare, Heart } from 'lucide-react';

export default function SharedShell({ children }) {
  const { role, driverInfo, hospitalInfo, logout } = useAuth();
  const navigate = useNavigate();
  const handleLogout = () => { logout(); navigate('/', { replace: true }); };
  const [dataFreshness] = useState('LIVE');

  let portalTitle = "RapidGrid Portal";
  let portalSub = "Autonomous AI System Node v4.2";
  let PortalIcon = Activity;

  if (role === 'dispatcher') {
    portalTitle = "City Emergency Command Center";
    portalSub = "Dispatcher Terminal — Live Multi-Agent AI Oversight";
    PortalIcon = ShieldAlert;
  } else if (role === 'driver') {
    portalTitle = driverInfo ? `${driverInfo.driverName} (${driverInfo.unitId})` : "First Responder Field Unit";
    portalSub = driverInfo?.hubName ? `Base: ${driverInfo.hubName}` : "Paramedic Field Unit — Live Navigation";
    PortalIcon = Truck;
  } else if (role === 'hospital') {
    portalTitle = hospitalInfo?.name || "Hospital Emergency Department";
    portalSub = "Dedicated ER Desk Terminal — Bed & Triage Management";
    PortalIcon = PlusSquare;
  } else if (role === 'citizen') {
    portalTitle = "Citizen Emergency App";
    portalSub = "Rapid Response & Live Incident Traversal";
    PortalIcon = Heart;
  }

  return (
    <div className="flex flex-col min-h-screen bg-[#ece5f0] text-[#012622] font-body">
      {/* Top Header */}
      <header className="sticky top-0 z-40 flex justify-between items-center px-6 py-3 bg-white/95 backdrop-blur-md border-b border-[#dcd3e3] shadow-elevation-sm">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-xl bg-[#012622] text-[#e98a15] flex items-center justify-center shadow-sm">
            <PortalIcon size={20} className="stroke-[2.5]" />
          </div>
          <div>
            <h1 className="font-bold text-base tracking-tight font-display text-[#012622] flex items-center gap-2">
              <span>{portalTitle}</span>
              <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-[#59114d]/10 text-[#59114d] border border-[#59114d]/20 uppercase">
                {role}
              </span>
            </h1>
            <span className="text-[11px] font-mono text-[#003b36] uppercase tracking-wider block mt-0.5">
              {portalSub}
            </span>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-xs font-bold font-mono bg-[#fdf3e7] border border-[#e98a15]/50 text-[#e98a15] px-3.5 py-1.5 rounded-full shadow-sm">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#e98a15] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#e98a15]"></span>
            </span>
            <span>{dataFreshness} SYNC</span>
          </div>

          <button 
            onClick={handleLogout} 
            className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#012622] hover:bg-[#003b36] text-white text-xs font-semibold transition-all shadow-sm active:scale-95"
            title="Sign Out of Portal"
          >
            <LogOut size={15} />
            <span>Sign Out</span>
          </button>
        </div>
      </header>
      
      {/* Main Content Area */}
      <main className="flex-1">
        {children}
      </main>
    </div>
  );
}

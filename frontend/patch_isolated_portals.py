import sys

# 1. Update CitizenDashboard.jsx to remove cross-role shortcuts
cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace header Logout button with clean Citizen Sign Out
old_cit_logout = """          <button
            onClick={handleLogout}
            className="flex items-center gap-1 px-3 py-1.5 rounded-full bg-surface-container-highest text-on-surface hover:bg-surface-variant transition-colors text-xs font-semibold ml-2"
            title="Return to Main Role Dashboard"
          >
            <span className="material-symbols-outlined text-[18px]">logout</span>
            <span>Switch Role</span>
          </button>"""

new_cit_logout = """          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-surface-container-highest text-on-surface hover:bg-surface-variant transition-colors text-xs font-semibold ml-2 border border-outline-variant/30"
            title="Sign Out of Citizen App"
          >
            <span className="material-symbols-outlined text-[16px]">person</span>
            <span>Sign Out</span>
          </button>"""

content = content.replace(old_cit_logout, new_cit_logout)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(content)


# 2. Update SharedShell.jsx to format role titles as authentic enterprise portals
shell_file = "src/components/SharedShell.jsx"

new_shell_code = """import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { LogOut, Activity, ShieldAlert, Truck, PlusSquare } from 'lucide-react';

export default function SharedShell({ children }) {
  const { role, hospitalInfo, logout } = useAuth();
  const navigate = useNavigate();
  const handleLogout = () => { logout(); navigate('/', { replace: true }); };
  const [dataFreshness, setDataFreshness] = useState('LIVE');

  useEffect(() => {
    document.body.className = `theme-${role}`;
  }, [role]);

  // Determine portal title & icon based on role
  let portalTitle = "GeoAgentic Portal";
  let portalSub = "System Node v4.2";
  let PortalIcon = Activity;

  if (role === 'dispatcher') {
    portalTitle = "City Emergency Command Center";
    portalSub = "Dispatcher Terminal - System Node v4.2";
    PortalIcon = ShieldAlert;
  } else if (role === 'driver') {
    portalTitle = "Ambulance Paramedic Unit (AMB-UNIT-04)";
    portalSub = "First Responder Field Unit - Live Navigation";
    PortalIcon = Truck;
  } else if (role === 'hospital') {
    portalTitle = hospitalInfo?.name || "Hospital Emergency Department";
    portalSub = "Dedicated ER Desk Terminal - Capacity Management";
    PortalIcon = PlusSquare;
  }

  return (
    <div className="flex flex-col min-h-screen bg-background text-on-background">
      {/* Top Professional Portal Header */}
      <header className="flex justify-between items-center px-6 py-3 bg-surface-container-lowest border-b border-outline-variant/30 text-on-surface shadow-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 text-primary rounded-xl flex items-center justify-center">
            <PortalIcon size={22} />
          </div>
          <div>
            <h1 className="font-bold text-base tracking-tight font-headline-md text-on-surface">{portalTitle}</h1>
            <span className="text-[10px] font-mono text-on-surface-variant uppercase tracking-wider block">
              {portalSub}
            </span>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-xs font-bold font-mono bg-tertiary/10 border border-tertiary/30 text-tertiary px-3 py-1.5 rounded-full">
            <Activity size={14} className={dataFreshness === 'LIVE' ? 'animate-pulse' : ''} />
            <span>{dataFreshness} SYNC</span>
          </div>

          <button 
            onClick={handleLogout} 
            className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-surface-container-highest hover:bg-surface-variant text-on-surface text-xs font-semibold transition-colors border border-outline-variant/30"
            title="Sign Out of Portal"
          >
            <LogOut size={16} />
            <span>Sign Out</span>
          </button>
        </div>
      </header>
      
      {/* Main Content Area */}
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  );
}
"""

with open(shell_file, "w", encoding="utf-8") as f:
    f.write(new_shell_code)

print("CitizenDashboard.jsx and SharedShell.jsx updated with clean, isolated portal headers")

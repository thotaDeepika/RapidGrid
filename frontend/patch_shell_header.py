import sys

shell_file = "src/components/SharedShell.jsx"
with open(shell_file, "r", encoding="utf-8") as f:
    content = f.read()

old_header = """      <header className="flex justify-between items-center p-4 bg-accent text-white shadow-md">
        <div className="flex items-center gap-4">
          <div className="font-bold text-xl tracking-tight">GeoAgentic</div>
          <div className="badge bg-white bg-opacity-20">{role}</div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm bg-white bg-opacity-20 p-2 rounded-lg">
            <Activity size={16} className={dataFreshness === 'LIVE' ? 'animate-pulse' : ''} />
            {dataFreshness}
          </div>
          <button onClick={handleLogout} className="flex items-center gap-2 hover:opacity-80 transition-opacity p-2">
            <LogOut size={18} />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </header>"""

new_header = """      <header className="flex justify-between items-center px-6 py-3 bg-surface-container-lowest border-b border-outline-variant/30 text-on-surface shadow-md">
        <div className="flex items-center gap-3">
          <div className="font-bold text-xl tracking-tight font-headline-md text-on-surface flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-[24px]">monitor_heart</span>
            <span>GeoAgentic</span>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-bold uppercase bg-surface-container-highest border border-outline-variant/40 text-on-surface-variant font-mono">
            ROLE: {role}
          </span>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-xs font-bold font-mono bg-tertiary/10 border border-tertiary/30 text-tertiary px-3 py-1.5 rounded-full">
            <Activity size={14} className={dataFreshness === 'LIVE' ? 'animate-pulse' : ''} />
            <span>{dataFreshness} SYNC</span>
          </div>

          <button 
            onClick={handleLogout} 
            className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-surface-container-highest hover:bg-surface-variant text-on-surface text-xs font-semibold transition-colors border border-outline-variant/30"
          >
            <LogOut size={16} />
            <span>Logout</span>
          </button>
        </div>
      </header>"""

content = content.replace(old_header, new_header)

with open(shell_file, "w", encoding="utf-8") as f:
    f.write(content)

print("SharedShell header styled cleanly - white boxes removed")

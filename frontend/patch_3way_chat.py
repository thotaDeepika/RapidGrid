import sys

# 1. Update LiveEmergencyChat.jsx to display 3-way recipient badge bar
chat_file = "src/components/LiveEmergencyChat.jsx"
with open(chat_file, "r", encoding="utf-8") as f:
    content = f.read()

badge_bar = """
      {/* 3-Way Emergency Channel Recipients Badge Bar */}
      <div className="bg-surface-container-low px-3 py-1.5 border-b border-outline-variant/20 flex justify-between items-center text-[10px] font-mono">
        <span className="text-tertiary font-bold uppercase flex items-center gap-1">
          <span className="w-1.5 h-1.5 bg-tertiary rounded-full animate-ping"></span>
          Unified Emergency Broadcast:
        </span>
        <div className="flex gap-2">
          <span className="bg-[#FFB900]/20 text-[#FFB900] px-2 py-0.5 rounded-full font-bold">?? Paramedic Unit</span>
          <span className="bg-[#B084FF]/20 text-[#B084FF] px-2 py-0.5 rounded-full font-bold">?? Hospital ER Desk</span>
        </div>
      </div>"""

if "Unified Emergency Broadcast" not in content:
    content = content.replace(
        "{/* Header */}\n      <div className=\"bg-surface-container-high p-3 border-b border-outline-variant/30 flex justify-between items-center\">",
        "{/* Header */}\n      <div className=\"bg-surface-container-high p-3 border-b border-outline-variant/30 flex justify-between items-center\">"
    )
    content = content.replace("</div>\n\n      {/* Messages */}", "</div>" + badge_bar + "\n\n      {/* Messages */}")

with open(chat_file, "w", encoding="utf-8") as f:
    f.write(content)


# 2. Update CitizenDashboard.jsx to add Call/SMS Hospital ER Desk button
cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

hosp_comm_bar = """
          {/* Dedicated Hospital ER Desk Call Button */}
          <div className="bg-surface-container rounded-xl p-stack-md flex flex-col gap-2 border border-[#B084FF]/30">
            <div className="text-xs font-bold font-mono text-[#B084FF] uppercase flex items-center gap-2">
              <span className="material-symbols-outlined text-[18px]">local_hospital</span>
              Direct Hospital ER Desk Contact ({hospitalName})
            </div>
            <div className="grid grid-cols-2 gap-2 mt-1">
              <a 
                href="tel:112" 
                className="bg-[#B084FF] text-white font-bold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-2 shadow-md hover:bg-[#B084FF]/90 transition-all text-center"
              >
                <span className="material-symbols-outlined text-[18px]">call</span>
                Call Hospital ER
              </a>
              <a 
                href="sms:112?body=Emergency%20Update%20from%20Citizen" 
                className="bg-surface-container-highest text-on-surface font-bold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-2 border border-outline-variant/30 hover:bg-surface-variant transition-all text-center"
              >
                <span className="material-symbols-outlined text-[18px]">sms</span>
                SMS Hospital ER
              </a>
            </div>
          </div>"""

if "Direct Hospital ER Desk Contact" not in c_content:
    c_content = c_content.replace(
        "{/* Hospital info */}",
        hosp_comm_bar + "\n\n          {/* Hospital info */}"
    )

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(c_content)

print("Unified 3-way recipient badge and Hospital ER direct call/SMS added successfully")

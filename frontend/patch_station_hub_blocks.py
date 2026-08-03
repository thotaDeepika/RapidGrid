import sys

# 1. Update CitizenDashboard.jsx with Station Hub Info Block
cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    c_content = f.read()

old_cit_hub_spot = """            {/* Dynamic Single vs Dual Emergency Unit Status Cards */}"""

new_cit_hub_block = """            {/* Station Base Hub Info Block */}
            <div className="bg-surface-container-low p-3.5 rounded-xl border border-[#FFB900]/30 flex items-center justify-between shadow-md mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#FFB900]/20 text-[#FFB900] flex items-center justify-center font-bold">
                  <span className="material-symbols-outlined text-[22px]">local_convenience_store</span>
                </div>
                <div>
                  <div className="text-[10px] font-mono font-bold text-[#FFB900] uppercase tracking-wider">
                    DISPATCHED FROM STATION HUB
                  </div>
                  <div className="text-xs font-bold text-on-surface font-mono">
                    {citizenView?.phase1_hub?.name || 'Hebbal Emergency Response Station'}
                  </div>
                </div>
              </div>
              <div className="text-right font-mono">
                <div className="text-xs font-bold text-[#FFB900]">{citizenView?.phase1_eta_minutes || 5}m Response</div>
                <div className="text-[9px] text-on-surface-variant uppercase">Phase 1 Route</div>
              </div>
            </div>

            {/* Dynamic Single vs Dual Emergency Unit Status Cards */}"""

if "DISPATCHED FROM STATION HUB" not in c_content:
    c_content = c_content.replace(old_cit_hub_spot, new_cit_hub_block)
    with open(cit_file, "w", encoding="utf-8") as f:
        f.write(c_content)


# 2. Update DriverDashboard.jsx to auto-set filter based on logged-in vehicleType and display Station Hub badges
drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

# Add useEffect for auto vehicle filter preselection
old_drv_hooks = """  const [driverStage, setDriverStage] = useState('pickup'); // 'pickup' | 'hospital'"""

new_drv_hooks = """  const [driverStage, setDriverStage] = useState('pickup'); // 'pickup' | 'hospital'

  useEffect(() => {
    if (driverData?.vehicleType) {
      setDriverVehicleFilter(driverData.vehicleType);
    }
  }, [driverData?.vehicleType]);"""

if "useEffect" not in d_content:
    d_content = d_content.replace("import React, { useState } from 'react';", "import React, { useState, useEffect } from 'react';")

d_content = d_content.replace(old_drv_hooks, new_drv_hooks)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("CitizenDashboard.jsx and DriverDashboard.jsx patched with Station Hub Blocks and Filter pre-selection")

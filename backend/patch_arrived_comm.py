import sys

# 1. Update CitizenDashboard.jsx
cit_file = "../frontend/src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    content = f.read()

# Update poll condition to include completed
content = content.replace(
    """        if (
          data.status === 'awaiting_dispatcher_approval' ||
          data.status === 'dispatched'
        ) {""",
    """        if (
          data.status === 'awaiting_dispatcher_approval' ||
          data.status === 'dispatched' ||
          data.status === 'completed'
        ) {"""
)

# Update headline and status rendering for completed state
old_headline = """                <div>
                  <h2 className="font-headline-md text-headline-md text-on-surface">Ambulance En Route</h2>
                  <p className="font-status-code text-status-code text-primary">
                    {incidentData?.status === 'dispatched' ? 'Driver Assigned' : 'Awaiting Dispatcher'}
                  </p>
                </div>"""

new_headline = """                <div>
                  <h2 className="font-headline-md text-headline-md text-on-surface">
                    {incidentData?.status === 'completed' ? 'Ambulance Arrived - On Site' : 'Ambulance En Route'}
                  </h2>
                  <p className="font-status-code text-status-code text-primary">
                    {incidentData?.status === 'completed' ? 'Arrived at Destination Hospital' : incidentData?.status === 'dispatched' ? 'Driver Assigned - En Route' : 'Awaiting Dispatcher'}
                  </p>
                </div>"""

content = content.replace(old_headline, new_headline)

# Update ETA text for completed status
old_eta_box = """              <div className="text-right">
                <div className="font-black text-[32px] text-primary leading-none" style={{ fontFamily: 'Inter' }}>
                  {etaMinutes}m
                </div>
                <p className="font-label-caps text-label-caps text-on-surface-variant uppercase">Arrival</p>
              </div>"""

new_eta_box = """              <div className="text-right">
                <div className="font-black text-[32px] text-primary leading-none" style={{ fontFamily: 'Inter' }}>
                  {incidentData?.status === 'completed' ? '0m' : `${etaMinutes}m`}
                </div>
                <p className="font-label-caps text-label-caps text-on-surface-variant uppercase">
                  {incidentData?.status === 'completed' ? 'ARRIVED' : 'Arrival'}
                </p>
              </div>"""

content = content.replace(old_eta_box, new_eta_box)

# Update timeline line width & step 3 styling for completed status
old_timeline = """              <div
                className="absolute top-1/2 left-0 h-0.5 bg-secondary -translate-y-1/2 transition-all duration-1000"
                style={{ width: incidentData?.status === 'dispatched' ? '66%' : '33%' }}
              ></div>
              <div className="relative flex justify-between">
                <div className="flex flex-col items-center gap-1">
                  <div className="w-3 h-3 bg-secondary rounded-full ring-4 ring-surface-container-high z-10"></div>
                  <span className="font-label-caps text-label-caps text-secondary">REPORTED</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-3 h-3 rounded-full ring-4 ring-surface-container-high z-10 ${incidentData?.status === 'dispatched' ? 'bg-secondary animate-pulse' : 'bg-outline'}`}></div>
                  <span className="font-label-caps text-label-caps text-secondary">DISPATCHED</span>
                </div>
                <div className="flex flex-col items-center gap-1 opacity-40">
                  <div className="w-3 h-3 bg-surface-container-lowest rounded-full ring-4 ring-surface-container-high z-10"></div>
                  <span className="font-label-caps text-label-caps text-on-surface">ON SITE</span>
                </div>
              </div>"""

new_timeline = """              <div
                className="absolute top-1/2 left-0 h-0.5 bg-tertiary -translate-y-1/2 transition-all duration-1000"
                style={{ width: incidentData?.status === 'completed' ? '100%' : incidentData?.status === 'dispatched' ? '66%' : '33%' }}
              ></div>
              <div className="relative flex justify-between">
                <div className="flex flex-col items-center gap-1">
                  <div className="w-3 h-3 bg-tertiary rounded-full ring-4 ring-surface-container-high z-10"></div>
                  <span className="font-label-caps text-label-caps text-tertiary">REPORTED</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-3 h-3 rounded-full ring-4 ring-surface-container-high z-10 ${incidentData?.status === 'dispatched' || incidentData?.status === 'completed' ? 'bg-tertiary' : 'bg-outline'}`}></div>
                  <span className="font-label-caps text-label-caps text-tertiary">DISPATCHED</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <div className={`w-3 h-3 rounded-full ring-4 ring-surface-container-high z-10 ${incidentData?.status === 'completed' ? 'bg-tertiary animate-pulse' : 'bg-outline'}`}></div>
                  <span className={`font-label-caps text-label-caps ${incidentData?.status === 'completed' ? 'text-tertiary font-bold' : 'text-on-surface opacity-40'}`}>ON SITE</span>
                </div>
              </div>"""

content = content.replace(old_timeline, new_timeline)

# Add Two-Way Communication Bar (Call/SMS Paramedic) inside Citizen App
cit_comm_bar = """
          {/* Direct Paramedic Communication Card */}
          <div className="bg-surface-container rounded-xl p-stack-md flex flex-col gap-2 border border-tertiary/30">
            <div className="text-xs font-bold font-mono text-tertiary uppercase flex items-center gap-2">
              <span className="material-symbols-outlined text-[18px]">support_agent</span>
              Direct First Responder Contact (Unit AMB-UNIT-04)
            </div>
            <div className="grid grid-cols-2 gap-2 mt-1">
              <a 
                href="tel:+919876543210" 
                className="bg-tertiary text-on-tertiary font-bold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-2 shadow-md hover:bg-tertiary/90 transition-all text-center"
              >
                <span className="material-symbols-outlined text-[18px]">call</span>
                Call Paramedic
              </a>
              <a 
                href="sms:+919876543210?body=Emergency%20Update%20from%20Citizen" 
                className="bg-surface-container-highest text-on-surface font-bold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-2 border border-outline-variant/30 hover:bg-surface-variant transition-all text-center"
              >
                <span className="material-symbols-outlined text-[18px]">sms</span>
                Send SMS Text
              </a>
            </div>
          </div>"""

if "Direct First Responder Contact" not in content:
    content = content.replace("          {/* Hospital info */}", cit_comm_bar + "\n\n          {/* Hospital info */}")

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(content)


# 2. Update DriverDashboard.jsx to add Direct Call/SMS Patient buttons
drv_file = "../frontend/src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    d_content = f.read()

drv_patient_comm = """
            <div className="pt-3 border-t border-outline-variant/20 space-y-2">
              <span className="text-on-surface-variant font-bold block text-[11px] uppercase">Direct Patient Contact ({selectedIncident.citizen_name || 'Citizen'}):</span>
              <div className="grid grid-cols-2 gap-2">
                <a 
                  href={`tel:${selectedIncident.citizen_phone || '+919876543210'}`} 
                  className="bg-primary text-on-primary font-bold py-2 px-3 rounded-xl text-xs flex items-center justify-center gap-1.5 shadow-md hover:bg-primary/90 text-center"
                >
                  <Phone size={14} /> Call Patient
                </a>
                <a 
                  href={`sms:${selectedIncident.citizen_phone || '+919876543210'}?body=Ambulance%20Unit%20AMB-UNIT-04%20is%20en%20route%20to%20your%20location.`} 
                  className="bg-surface-container-highest text-on-surface font-bold py-2 px-3 rounded-xl text-xs flex items-center justify-center gap-1.5 border border-outline-variant/30 hover:bg-surface-variant text-center"
                >
                  <MessageSquare size={14} /> SMS Patient
                </a>
              </div>
            </div>"""

if "Direct Patient Contact" not in d_content:
    d_content = d_content.replace(
        '<div className="pt-2 border-t border-outline-variant/20">',
        drv_patient_comm + '\n\n            <div className="pt-2 border-t border-outline-variant/20">'
    )
    # Add MessageSquare import if not present
    if "MessageSquare" not in d_content:
        d_content = d_content.replace("Phone, Clock,", "Phone, MessageSquare, Clock,")

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(d_content)

print("Arrived status fix & Two-Way Call/SMS communication patched successfully")

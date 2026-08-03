import sys

hosp_file = "src/views/HospitalDashboard.jsx"
with open(hosp_file, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "export default function HospitalDashboard() {",
    "export default function HospitalDashboard() {\n  const { hospitalInfo } = useAuth();"
)

# Add useAuth import if not present
if "useAuth" not in content:
    content = content.replace(
        "import React, { useState, useEffect } from 'react';",
        "import React, { useState, useEffect } from 'react';\nimport { useAuth } from '../context/AuthContext';"
    )

content = content.replace(
    "fetch('/api/hospital/incoming/all')",
    "fetch(`/api/hospital/${hospitalInfo?.id || 'all'}/incoming`)"
)

content = content.replace(
    '<h1 className="font-headline-md text-base font-bold text-on-surface">Emergency Department</h1>',
    '<h1 className="font-headline-md text-base font-bold text-on-surface">{hospitalInfo?.name || "Bangalore Central ER Desk"}</h1>'
)

with open(hosp_file, "w", encoding="utf-8") as f:
    f.write(content)

print("HospitalDashboard.jsx updated to track specific logged-in hospital")

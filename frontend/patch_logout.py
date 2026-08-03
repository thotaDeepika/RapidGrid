import sys

# 1. Patch CitizenDashboard.jsx to import useAuth and add Logout button in TopHeader
cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    cit_content = f.read()

# Add useAuth import
if "useAuth" not in cit_content:
    cit_content = cit_content.replace(
        "import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';",
        "import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';\nimport { useAuth } from '../context/AuthContext';"
    )

# Add logout hook call inside component
if "const { logout } = useAuth();" not in cit_content:
    cit_content = cit_content.replace(
        "export default function CitizenDashboard() {",
        "export default function CitizenDashboard() {\n  const { logout } = useAuth();"
    )

# Add Logout / Role Switch button inside TopHeader
old_header_end = """          {title === 'Home' && (
            <div className="w-8 h-8 rounded-full bg-primary-container flex items-center justify-center">
              <span className="material-symbols-outlined text-on-primary-container text-[16px]">person</span>
            </div>
          )}
        </div>
      </div>
    </header>"""

new_header_end = """          <button
            onClick={logout}
            className="flex items-center gap-1 px-3 py-1.5 rounded-full bg-surface-container-highest text-on-surface hover:bg-surface-variant transition-colors text-xs font-semibold ml-auto"
            title="Return to Main Role Dashboard"
          >
            <span className="material-symbols-outlined text-[18px]">logout</span>
            <span>Switch Role</span>
          </button>
        </div>
      </div>
    </header>"""

cit_content = cit_content.replace(old_header_end, new_header_end)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(cit_content)

# 2. Patch App.jsx to fix ProtectedRoute useEffect hook warning
app_file = "src/App.jsx"
with open(app_file, "r", encoding="utf-8") as f:
    app_content = f.read()

new_protected = """function ProtectedRoute({ allowedRoles, children }) {
  const { role, login } = useAuth();
  const location = window.location.pathname.replace('/', '');
  
  useEffect(() => {
    if (allowedRoles && allowedRoles.includes(location) && role !== location) {
      login(location);
    }
  }, [allowedRoles, location, role, login]);

  return children;
}"""

import re
app_content = re.sub(r'function ProtectedRoute\(\{ allowedRoles, children \}\) \{[\s\S]*?\n\}', new_protected, app_content)

with open(app_file, "w", encoding="utf-8") as f:
    f.write(app_content)

print("CitizenDashboard logout and App.jsx clean route hooks patched successfully")

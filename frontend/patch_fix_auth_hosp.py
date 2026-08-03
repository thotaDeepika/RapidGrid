import sys

# 1. Update AuthContext.jsx
auth_file = "src/context/AuthContext.jsx"
new_auth_py = """import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [role, setRole] = useState(sessionStorage.getItem('geoagentic_role') || null);
  
  const [hospitalInfo, setHospitalInfo] = useState(() => {
    try {
      return JSON.parse(sessionStorage.getItem('geoagentic_hosp')) || { id: 'all', name: 'Bangalore Central ER Desk' };
    } catch {
      return { id: 'all', name: 'Bangalore Central ER Desk' };
    }
  });

  const [citizenInfo, setCitizenInfo] = useState(() => {
    try {
      return JSON.parse(sessionStorage.getItem('geoagentic_citizen')) || { name: 'Ananya Sharma', phone: '+91 98765 43210' };
    } catch {
      return { name: 'Ananya Sharma', phone: '+91 98765 43210' };
    }
  });

  const login = (selectedRole, extraData = null) => {
    setRole(selectedRole);
    sessionStorage.setItem('geoagentic_role', selectedRole);
    if (selectedRole === 'hospital' && extraData) {
      setHospitalInfo(extraData);
      sessionStorage.setItem('geoagentic_hosp', JSON.stringify(extraData));
    } else if (selectedRole === 'citizen' && extraData) {
      setCitizenInfo(extraData);
      sessionStorage.setItem('geoagentic_citizen', JSON.stringify(extraData));
    }
  };

  const logout = () => {
    setRole(null);
    sessionStorage.removeItem('geoagentic_role');
  };

  return (
    <AuthContext.Provider value={{ role, hospitalInfo, citizenInfo, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
"""

with open(auth_file, "w", encoding="utf-8") as f:
    f.write(new_auth_py)

# 2. Fix HospitalDashboard.jsx missing import of useAuth
hosp_file = "src/views/HospitalDashboard.jsx"
with open(hosp_file, "r", encoding="utf-8") as f:
    h_content = f.read()

if "import { useAuth }" not in h_content:
    h_content = h_content.replace(
        "import React, { useState, useEffect } from 'react';",
        "import React, { useState, useEffect } from 'react';\nimport { useAuth } from '../context/AuthContext';"
    )
    with open(hosp_file, "w", encoding="utf-8") as f:
        f.write(h_content)

print("AuthContext and HospitalDashboard import fixed")

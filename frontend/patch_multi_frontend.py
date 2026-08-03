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

  const login = (selectedRole, extraData = null) => {
    setRole(selectedRole);
    sessionStorage.setItem('geoagentic_role', selectedRole);
    if (extraData) {
      setHospitalInfo(extraData);
      sessionStorage.setItem('geoagentic_hosp', JSON.stringify(extraData));
    }
  };

  const logout = () => {
    setRole(null);
    sessionStorage.removeItem('geoagentic_role');
  };

  return (
    <AuthContext.Provider value={{ role, hospitalInfo, login, logout }}>
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

# 2. Update Login.jsx to add Hospital Credentials Selector Modal
login_file = "src/views/Login.jsx"
with open(login_file, "r", encoding="utf-8") as f:
    l_content = f.read()

# Add hospital selection modal state & logic
old_login_start = """export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleRoleLogin = (roleId) => {
    login(roleId);
    navigate(`/${roleId}`);
  };"""

new_login_start = """export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [showHospModal, setShowHospModal] = React.useState(false);

  const bangaloreHospitals = [
    { id: 'all', name: 'Bangalore Central ER Desk (All Incidents)' },
    { id: 'blr-007', name: 'Aster CMI Hospital (Hebbal)' },
    { id: 'blr-001', name: 'Manipal Hospital (Old Airport Road)' },
    { id: 'blr-002', name: 'Fortis Hospital (Bannerghatta Road)' },
    { id: 'blr-003', name: 'Apollo Hospital (Bannerghatta Road)' },
    { id: 'blr-005', name: "St. John's Medical College Hospital" },
    { id: 'blr-012', name: 'Columbia Asia Hospital (Hebbal)' },
    { id: 'medstar', name: 'MEDSTAR Speciality Hospital' },
    { id: 'prolife', name: 'Prolife Hospital' }
  ];

  const handleRoleLogin = (roleId, extraData = null) => {
    if (roleId === 'hospital' && !extraData) {
      setShowHospModal(true);
      return;
    }
    login(roleId, extraData);
    navigate(`/${roleId}`);
  };"""

l_content = l_content.replace(old_login_start, new_login_start)

# Add Hospital Modal JSX right before ending main tag
hosp_modal_jsx = """
      {/* Hospital Selection Modal */}
      {showHospModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-surface-container p-6 rounded-2xl border border-outline-variant/30 max-w-md w-full space-y-4 shadow-2xl animate-in zoom-in-95">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-lg font-bold text-on-surface">Select Hospital ER Credentials</h3>
                <p className="text-xs text-on-surface-variant">Pick a hospital to log into its dedicated ER Desk</p>
              </div>
              <button onClick={() => setShowHospModal(false)} className="text-on-surface-variant hover:text-on-surface font-bold text-sm">X</button>
            </div>

            <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
              {bangaloreHospitals.map(h => (
                <button
                  key={h.id}
                  onClick={() => {
                    setShowHospModal(false);
                    handleRoleLogin('hospital', h);
                  }}
                  className="w-full p-3 bg-surface-container-high hover:bg-primary-container/20 rounded-xl border border-outline-variant/20 hover:border-primary text-left text-xs font-bold transition-all flex justify-between items-center"
                >
                  <span>{h.name}</span>
                  <span className="text-[10px] text-primary font-mono">LOGIN &rarr;</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}"""

l_content = l_content.replace("    </div>\n  );\n}", hosp_modal_jsx)

with open(login_file, "w", encoding="utf-8") as f:
    f.write(l_content)

print("AuthContext and Login.jsx updated with hospital credential selection")

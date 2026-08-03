import sys

# Patch AuthContext.jsx to use sessionStorage (tab-specific) instead of localStorage
auth_file = "src/context/AuthContext.jsx"
with open(auth_file, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("localStorage", "sessionStorage")

with open(auth_file, "w", encoding="utf-8") as f:
    f.write(content)

# Patch App.jsx so ProtectedRoute doesn't forcibly block or redirect when navigating directly to role URLs
app_file = "src/App.jsx"
with open(app_file, "r", encoding="utf-8") as f:
    app_content = f.read()

new_protected = """function ProtectedRoute({ allowedRoles, children }) {
  const { role, login } = useAuth();
  const location = window.location.pathname.replace('/', '');
  
  // Auto-login to the role specified by URL path if role is missing or mismatched in tab
  if (allowedRoles && allowedRoles.includes(location) && role !== location) {
    login(location);
  }

  return children;
}"""

# Find old ProtectedRoute definition and replace
import re
app_content = re.sub(r'function ProtectedRoute\(\{ allowedRoles, children \}\) \{[\s\S]*?\n\}', new_protected, app_content)

with open(app_file, "w", encoding="utf-8") as f:
    f.write(app_content)

print("AuthContext and App.jsx patched for Multi-Tab support")

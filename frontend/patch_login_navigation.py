import sys

# 1. Patch Login.jsx to use useNavigate and immediately navigate when clicking role buttons
login_file = "src/views/Login.jsx"
with open(login_file, "r", encoding="utf-8") as f:
    l_content = f.read()

if "useNavigate" not in l_content:
    l_content = l_content.replace(
        "import React, { useRef } from 'react';",
        "import React, { useRef } from 'react';\nimport { useNavigate } from 'react-router-dom';"
    )

l_content = l_content.replace(
    "export default function Login() {\n  const { login } = useAuth();",
    "export default function Login() {\n  const { login } = useAuth();\n  const navigate = useNavigate();\n\n  const handleRoleLogin = (roleId) => {\n    login(roleId);\n    navigate(`/${roleId}`);\n  };"
)

l_content = l_content.replace(
    "onClick={() => login(r.id)}",
    "onClick={() => handleRoleLogin(r.id)}"
)

# Also wire "Get Started" button in Hero section to handleRoleLogin('citizen')
l_content = l_content.replace(
    """<button 
                onClick={scrollToSystemAccess}
                className="h-14 px-8 bg-primary text-on-primary font-bold text-base rounded-full shadow-[0_4px_16px_rgba(255,84,81,0.4)] active:translate-y-0.5 transition-all flex items-center gap-2 hover:bg-primary/90"
              >""",
    """<button 
                onClick={() => handleRoleLogin('citizen')}
                className="h-14 px-8 bg-primary text-on-primary font-bold text-base rounded-full shadow-[0_4px_16px_rgba(255,84,81,0.4)] active:translate-y-0.5 transition-all flex items-center gap-2 hover:bg-primary/90"
              >"""
)

with open(login_file, "w", encoding="utf-8") as f:
    f.write(l_content)

print("Login.jsx navigation patched successfully")

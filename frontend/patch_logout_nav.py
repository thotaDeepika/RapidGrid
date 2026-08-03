import sys

# 1. Update CitizenDashboard.jsx
cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    cit_content = f.read()

if "useNavigate" not in cit_content:
    cit_content = cit_content.replace(
        "import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';",
        "import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';\nimport { useNavigate } from 'react-router-dom';"
    )

cit_content = cit_content.replace(
    "  const { logout } = useAuth();",
    "  const { logout } = useAuth();\n  const navigate = useNavigate();\n  const handleLogout = () => { logout(); navigate('/', { replace: true }); };"
)

cit_content = cit_content.replace(
    "onClick={logout}",
    "onClick={handleLogout}"
)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(cit_content)

# 2. Update SharedShell.jsx
shell_file = "src/components/SharedShell.jsx"
with open(shell_file, "r", encoding="utf-8") as f:
    shell_content = f.read()

if "useNavigate" not in shell_content:
    shell_content = shell_content.replace(
        "import { useAuth } from '../context/AuthContext';",
        "import { useAuth } from '../context/AuthContext';\nimport { useNavigate } from 'react-router-dom';"
    )

shell_content = shell_content.replace(
    "export default function SharedShell({ children }) {\n  const { role, logout } = useAuth();",
    "export default function SharedShell({ children }) {\n  const { role, logout } = useAuth();\n  const navigate = useNavigate();\n  const handleLogout = () => { logout(); navigate('/', { replace: true }); };"
)

shell_content = shell_content.replace(
    "onClick={logout}",
    "onClick={handleLogout}"
)

with open(shell_file, "w", encoding="utf-8") as f:
    f.write(shell_content)

print("Logout navigation patched successfully in CitizenDashboard and SharedShell")

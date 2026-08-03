import sys

cit_file = "src/views/CitizenDashboard.jsx"
with open(cit_file, "r", encoding="utf-8") as f:
    content = f.read()

# Consume citizenInfo from useAuth
content = content.replace(
    "export default function CitizenDashboard() {\n  const { logout } = useAuth();",
    "export default function CitizenDashboard() {\n  const { citizenInfo, logout } = useAuth();"
)

# Display citizen credentials in header next to Sign Out button
old_cit_badge = """          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-surface-container-highest text-on-surface hover:bg-surface-variant transition-colors text-xs font-semibold ml-2 border border-outline-variant/30"
            title="Sign Out of Citizen App"
          >
            <span className="material-symbols-outlined text-[16px]">person</span>
            <span>Sign Out</span>
          </button>"""

new_cit_badge = """          <div className="hidden sm:flex items-center gap-2 bg-tertiary/10 border border-tertiary/30 px-3 py-1 rounded-full text-xs font-mono text-tertiary font-bold ml-2">
            <span className="material-symbols-outlined text-[16px]">account_circle</span>
            <span>{citizenInfo?.name || "Ananya Sharma"}</span>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-surface-container-highest text-on-surface hover:bg-surface-variant transition-colors text-xs font-semibold ml-2 border border-outline-variant/30"
            title="Sign Out of Citizen App"
          >
            <span className="material-symbols-outlined text-[16px]">logout</span>
            <span>Sign Out</span>
          </button>"""

content = content.replace(old_cit_badge, new_cit_badge)

with open(cit_file, "w", encoding="utf-8") as f:
    f.write(content)

print("CitizenDashboard.jsx updated to display citizen profile credentials")

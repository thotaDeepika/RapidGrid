import sys

file_path = "src/views/CitizenDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'className="px-margin-mobile -mt-6 relative z-10 space-y-stack-md pb-8"',
    'className="px-margin-mobile mt-4 relative z-10 space-y-stack-md pb-8"'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

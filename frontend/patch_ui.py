import sys

file_path = "src/views/CitizenDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "const mapContainerStyle = { width: '100%', height: '100%' };",
    "const mapContainerStyle = { width: '100%', height: '100%', zIndex: 0 };"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

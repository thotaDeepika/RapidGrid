import sys

file_path = "src/views/CitizenDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    '<button className="flex flex-col items-center justify-center bg-secondary-container text-on-secondary-container h-24 rounded-xl active:scale-95 transition-transform">',
    '<button onClick={() => window.location.href="tel:112"} className="flex flex-col items-center justify-center bg-secondary-container text-on-secondary-container h-24 rounded-xl active:scale-95 transition-transform hover:bg-secondary hover:text-on-secondary">'
)

content = content.replace(
    '<button className="flex flex-col items-center justify-center bg-surface-container-highest text-on-surface h-24 rounded-xl active:scale-95 transition-transform">',
    '<button onClick={() => window.location.href="sms:112"} className="flex flex-col items-center justify-center bg-surface-container-highest text-on-surface h-24 rounded-xl active:scale-95 transition-transform hover:bg-surface-variant">'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

import sys
import urllib.parse

file_path = "src/views/CitizenDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

msg = urllib.parse.quote("EMERGENCY! I need immediate assistance. An ambulance has been dispatched to my location.")
new_href = f'sms:112,+919876543210,+919988776655?body={msg}'

content = content.replace(
    'onClick={() => window.location.href="sms:112"}',
    f'onClick={{() => window.location.href="{new_href}"}}'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

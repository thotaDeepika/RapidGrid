import sys

chat_file = "src/components/LiveEmergencyChat.jsx"
with open(chat_file, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "const [activeChannel, setActiveChannel] = useState('driver');",
    "const [activeChannel, setActiveChannel] = useState(senderRole === 'driver' ? 'driver' : 'hospital');"
)

with open(chat_file, "w", encoding="utf-8") as f:
    f.write(content)

print("LiveEmergencyChat.jsx default activeChannel updated by role")

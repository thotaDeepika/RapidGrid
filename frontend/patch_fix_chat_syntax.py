import sys

chat_file = "src/components/LiveEmergencyChat.jsx"
with open(chat_file, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("# 2. Open WebSocket connection", "// 2. Open WebSocket connection")

with open(chat_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed syntax error in LiveEmergencyChat.jsx")

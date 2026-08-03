import sys

chat_file = "src/components/LiveEmergencyChat.jsx"
with open(chat_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace messagesEndRef with chatStreamRef
content = content.replace("const messagesEndRef = useRef(null);", "const chatStreamRef = useRef(null);")

old_scroll = """  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };"""

new_scroll = """  const scrollToBottom = () => {
    if (chatStreamRef.current) {
      chatStreamRef.current.scrollTop = chatStreamRef.current.scrollHeight;
    }
  };"""

content = content.replace(old_scroll, new_scroll)

# Remove useEffect([messages]) auto-scroll into view that was hijacking the main browser window scroll
content = content.replace("""  useEffect(() => {
    scrollToBottom();
  }, [messages]);""", "")

# Attach ref={chatStreamRef} to the messages stream div
content = content.replace(
    '<div className="flex-1 p-3 overflow-y-auto space-y-2 text-xs bg-surface-container-lowest/40">',
    '<div ref={chatStreamRef} className="flex-1 p-3 overflow-y-auto space-y-2 text-xs bg-surface-container-lowest/40">'
)

# Remove <div ref={messagesEndRef} />
content = content.replace('<div ref={messagesEndRef} />', '')

with open(chat_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed window scroll hijacking in LiveEmergencyChat.jsx")

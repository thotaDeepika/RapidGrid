import requests

# We know the incidents are stored in memory in incident.py
# If we just restart the backend, they are cleared.
# But since the user ran uvicorn --reload, if we touch main.py or incident.py,
# uvicorn will automatically reload the server!

# Let's just touch incident.py to trigger a hot-reload.
import os
import time

filepath = "backend/routers/incident.py"
os.utime(filepath, (time.time(), time.time()))
print("Touched incident.py to trigger uvicorn reload.")

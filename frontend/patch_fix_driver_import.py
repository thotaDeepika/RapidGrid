import sys

drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "import { Truck, Navigation, Phone,",
    "import { Truck, Navigation, Phone, MessageSquare,"
)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(content)

print("DriverDashboard.jsx fixed by adding missing MessageSquare import")

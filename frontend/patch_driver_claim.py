import sys

drv_file = "src/views/DriverDashboard.jsx"
with open(drv_file, "r", encoding="utf-8") as f:
    content = f.read()

# Add claim API call inside Accept button click
old_claim_handler = """                      onClick={() => {
                        setSelectedIncident(inc);
                        setIsNavigating(true);
                      }}"""

new_claim_handler = """                      onClick={async () => {
                        try {
                          const res = await fetch('/api/driver/claim', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                              incident_id: inc.incident_id,
                              driver_id: 'AMB-UNIT-04'
                            })
                          });

                          if (res.status === 409) {
                            alert(`Incident ${inc.incident_id} has already been claimed by another driver!`);
                            return;
                          }

                          setSelectedIncident(inc);
                          setIsNavigating(true);
                        } catch (err) {
                          console.error('Error claiming dispatch:', err);
                        }
                      }}"""

content = content.replace(old_claim_handler, new_claim_handler)

with open(drv_file, "w", encoding="utf-8") as f:
    f.write(content)

print("DriverDashboard.jsx updated for first-come-first-served claiming")

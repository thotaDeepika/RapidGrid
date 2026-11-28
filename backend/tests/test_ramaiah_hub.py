"""MS Ramaiah Memorial Hospital has its own ambulance hub on the demo map.

A short production contacts file used to list the hospital but no unit at
that hub, so a call next to Ramaiah fell back to Manipal / Aster. The demo
fleet expand fills AMB-21 in; these tests lock that behaviour.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import contacts
import fleet
from agents.route_optimization import find_nearest_hub

RAMAIAH = {"lat": 13.0283, "lng": 77.5698}
SHORT = {
    "dispatch": {"name": "City dispatch", "staff_pin": "111111"},
    "units": [
        {"unit_id": "AMB-01", "type": "Ambulance", "station": "Aster CMI Emergency Ambulance Hub",
         "staff_pin": "222222"},
        {"unit_id": "AMB-02", "type": "Ambulance", "station": "Manipal Ambulance Base Depot",
         "staff_pin": "333333"},
        {"unit_id": "AMB-03", "type": "Ambulance", "station": "Victoria Hospital Paramedic Base",
         "staff_pin": "444444"},
    ],
    "hospitals": [
        {"hospital_id": "blr-009", "name": "MS Ramaiah Memorial Hospital", "staff_pin": "555555"},
        {"hospital_id": "blr-001", "name": "Manipal Hospital (Old Airport Road)", "staff_pin": "666666"},
    ],
}


def test_the_nearest_hub_beside_ramaiah_is_the_ramaiah_ambulance_hub():
    hub = find_nearest_hub("Ambulance", RAMAIAH["lat"], RAMAIAH["lng"])
    assert hub["name"] == "MS Ramaiah Memorial Hospital Emergency Ambulance Hub"
    assert hub["id"] == "AMB-HUB-15"


def test_the_example_fleet_assigns_the_ramaiah_unit_at_that_hub():
    unit = fleet.assign("INC-ramaiah", "Ambulance", RAMAIAH,
                        prefer_station="MS Ramaiah Memorial Hospital Emergency Ambulance Hub")
    assert unit["unit_id"] == "AMB-21"
    assert "Ramaiah" in unit["station"]


def test_demo_expand_adds_the_ramaiah_unit_to_a_short_contacts_file(monkeypatch):
    monkeypatch.setenv("RAPIDGRID_MODE", "demo")
    monkeypatch.setenv("RAPIDGRID_EXPAND_DEMO_FLEET", "1")
    monkeypatch.setenv("RAPIDGRID_CONTACTS", json.dumps(SHORT))
    monkeypatch.delenv("RAPIDGRID_CONTACTS_FILE", raising=False)
    contacts.directory.cache_clear()
    fleet._units.clear()
    fleet._loaded = False

    directory = contacts.directory()
    assert any(u.unit_id == "AMB-21" for u in directory.units)
    unit = next(u for u in directory.units if u.unit_id == "AMB-21")
    assert unit.station == "MS Ramaiah Memorial Hospital Emergency Ambulance Hub"
    assert unit.staff_pin == "222222"  # same PIN as the rest of the fleet for the picker

    assigned = fleet.assign("INC-ramaiah-live", "Ambulance", RAMAIAH,
                            prefer_station=unit.station)
    assert assigned["unit_id"] == "AMB-21"

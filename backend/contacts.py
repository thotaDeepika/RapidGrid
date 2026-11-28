"""Contacts directory: units, crews, hospitals, dispatch and the 112 line.

Real phone numbers and staff PINs never live in the repository. The directory
is read, in order, from:

1. ``RAPIDGRID_CONTACTS``: the JSON itself (a Render secret).
2. ``RAPIDGRID_CONTACTS_FILE``: a path to a JSON file.
3. ``backend/contacts.json``: a git-ignored local file.
4. ``backend/contacts.example.json``: committed placeholders, with no PINs.

Without any staff PIN (the example file), staff sign-in is off and the app
behaves as an open local demo. ``public_*`` helpers return what any screen
may show; phone numbers and PINs are only returned by the staff-scoped
helpers.
"""

from __future__ import annotations

import json
import logging
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

logger = logging.getLogger("geoagentic.contacts")

_HERE = Path(__file__).resolve().parent
_ID = r"^[A-Za-z0-9_-]{1,40}$"
UnitType = Literal["Ambulance", "Fire Engine", "Police Cruiser", "Disaster Rescue"]


def _phone(value: Optional[str]) -> Optional[str]:
    if value in (None, ""):
        return None
    value = str(value).strip()
    if not re.fullmatch(r"\+?[0-9 ()-]{6,20}", value):
        raise ValueError("phone numbers may contain digits, spaces, brackets, '-' and a leading '+'")
    return value


def _pin(value: Optional[str]) -> Optional[str]:
    if value in (None, ""):
        return None
    value = str(value).strip()
    if not re.fullmatch(r"[0-9]{6,12}", value):
        raise ValueError("staff PINs must be 6 to 12 digits")
    return value


def _tracker_key(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if not re.fullmatch(r"[A-Za-z0-9_-]{24,128}", value):
        raise ValueError("tracker keys must be 24 to 128 letters, digits, '-' or '_'")
    if len(set(value)) < 10:
        # It is the vehicle's only credential: "aaaa..." or a short pattern
        # repeated is guessable. Make one with: openssl rand -hex 16
        raise ValueError("tracker keys must be random (use: openssl rand -hex 16)")
    return value


class Person(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    phone: Optional[str] = None
    _check_phone = field_validator("phone")(_phone)


class Dispatch(Person):
    staff_pin: Optional[str] = None
    _check_pin = field_validator("staff_pin")(_pin)


class Unit(BaseModel):
    unit_id: str = Field(pattern=_ID)
    type: UnitType
    station: str = Field(min_length=1, max_length=120)
    crew: str = Field(default="", max_length=80)
    phone: Optional[str] = None
    staff_pin: Optional[str] = None
    # The secret a tracker app on this vehicle's phone sends as its device
    # id (Traccar Client), so it can post fixes in the background with no
    # browser session. Never shown on any screen.
    tracker_key: Optional[str] = None
    _check_phone = field_validator("phone")(_phone)
    _check_pin = field_validator("staff_pin")(_pin)
    _check_tracker = field_validator("tracker_key")(_tracker_key)


class Hospital(BaseModel):
    hospital_id: str = Field(pattern=_ID)
    name: str = Field(min_length=1, max_length=120)
    emergency_phone: Optional[str] = None
    icu_phone: Optional[str] = None
    staff_pin: Optional[str] = None
    _check_phones = field_validator("emergency_phone", "icu_phone")(_phone)
    _check_pin = field_validator("staff_pin")(_pin)


class Directory(BaseModel):
    # Set when a configured directory could not be loaded. Staff sign-in then
    # stays ON with no valid PIN (fail closed), instead of looking like an
    # intentionally open demo.
    invalid: bool = False
    hotline_112: Optional[Person] = None
    dispatch: Optional[Dispatch] = None
    units: list[Unit] = Field(default_factory=list, max_length=200)
    hospitals: list[Hospital] = Field(default_factory=list, max_length=200)

    @field_validator("units")
    @classmethod
    def _unique_units(cls, units):
        ids = [u.unit_id for u in units]
        if len(ids) != len(set(ids)):
            raise ValueError("unit ids must be unique")
        return units


class _Missing(Exception):
    """A contacts source was configured but cannot be read."""


def _raw() -> tuple[str, str, bool]:
    """(text, source name, whether the source was configured explicitly)."""
    inline = os.getenv("RAPIDGRID_CONTACTS", "").strip()
    if inline:
        return inline, "RAPIDGRID_CONTACTS", True
    configured = os.getenv("RAPIDGRID_CONTACTS_FILE", "").strip()
    if configured:
        path = Path(configured)
        if not path.is_file():
            raise _Missing(path.name)
        return path.read_text(encoding="utf-8"), path.name, True
    private = _HERE / "contacts.json"
    if private.is_file():
        return private.read_text(encoding="utf-8"), private.name, True
    if os.getenv("RENDER", "").lower() == "true":
        # Hosted without the private directory: lock staff sign-in rather than
        # run with no PINs (everything open). Set RAPIDGRID_CONTACTS (A05).
        raise _Missing("RAPIDGRID_CONTACTS")
    example = _HERE / "contacts.example.json"
    if example.is_file():
        return example.read_text(encoding="utf-8"), example.name, False
    return "{}", "empty", False


def _demo_mode() -> bool:
    default = "operator" if os.getenv("RENDER", "").lower() == "true" else "demo"
    return os.getenv("RAPIDGRID_MODE", default).lower() == "demo"


def _expand_demo_fleet() -> bool:
    """Fill in showcase hubs (e.g. MS Ramaiah) the map already draws.

    Production often keeps a short contacts file with staff PINs while the
    code lists every ambulance hub. Without a unit at that hub, dispatch
    falls back to a far station (Manipal / Aster). In demo mode we merge
    the missing example units and hospitals so the projector and unit
    picker match the map. Set RAPIDGRID_EXPAND_DEMO_FLEET=0 to leave the
    contacts file exactly as written.
    """
    flag = os.getenv("RAPIDGRID_EXPAND_DEMO_FLEET", "1").lower()
    if flag in {"0", "false", "no"}:
        return False
    return _demo_mode()


def _merge_example_showcase(loaded: Directory) -> Directory:
    example_path = _HERE / "contacts.example.json"
    if not example_path.is_file():
        return loaded
    try:
        example = Directory.model_validate(json.loads(example_path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValidationError):
        logger.warning("Could not read contacts.example.json to expand the demo fleet")
        return loaded
    have_units = {u.unit_id for u in loaded.units}
    have_hospitals = {h.hospital_id for h in loaded.hospitals}
    donor_unit_pin = next((u.staff_pin for u in loaded.units if u.staff_pin), None)
    donor_hospital_pin = next((h.staff_pin for h in loaded.hospitals if h.staff_pin), None)
    extra_units = []
    for unit in example.units:
        if unit.unit_id in have_units:
            continue
        data = unit.model_dump()
        # Same staff PIN as the rest of the fleet so the unit picker works.
        if donor_unit_pin and not data.get("staff_pin"):
            data["staff_pin"] = donor_unit_pin
        extra_units.append(Unit.model_validate(data))
    extra_hospitals = []
    for hospital in example.hospitals:
        if hospital.hospital_id in have_hospitals:
            continue
        data = hospital.model_dump()
        if donor_hospital_pin and not data.get("staff_pin"):
            data["staff_pin"] = donor_hospital_pin
        extra_hospitals.append(Hospital.model_validate(data))
    if not extra_units and not extra_hospitals:
        return loaded
    merged = loaded.model_copy(update={
        "units": list(loaded.units) + extra_units,
        "hospitals": list(loaded.hospitals) + extra_hospitals,
    })
    logger.info("Demo fleet expanded from example: +%d units, +%d hospitals",
                len(extra_units), len(extra_hospitals))
    return merged


@lru_cache(maxsize=1)
def directory() -> Directory:
    try:
        text, source, configured = _raw()
    except (_Missing, OSError):
        logger.error("Configured contacts file cannot be read; staff sign-in locked")
        return Directory(invalid=True)
    try:
        loaded = Directory.model_validate(json.loads(text))
    except (json.JSONDecodeError, ValidationError) as error:
        # Never echo the content: it holds phone numbers and PINs.
        logger.error("Contacts directory from %s is invalid (%s error(s)); staff sign-in locked",
                     source, getattr(error, "error_count", lambda: 1)())
        return Directory(invalid=configured)
    if configured and _expand_demo_fleet():
        loaded = _merge_example_showcase(loaded)
    logger.info("Contacts directory loaded from %s: %d units, %d hospitals",
                source, len(loaded.units), len(loaded.hospitals))
    return loaded


def reload() -> Directory:
    directory.cache_clear()
    return directory()


def staff_pins_configured() -> bool:
    d = directory()
    if d.invalid:
        return True  # locked: sign-in required, and no PIN can match
    return bool((d.dispatch and d.dispatch.staff_pin)
                or any(u.staff_pin for u in d.units)
                or any(h.staff_pin for h in d.hospitals))


def staff_pin(role: str, subject: str) -> Optional[str]:
    d = directory()
    if role == "dispatcher":
        return d.dispatch.staff_pin if d.dispatch else None
    if role == "unit":
        return next((u.staff_pin for u in d.units if u.unit_id == subject), None)
    if role == "hospital":
        return next((h.staff_pin for h in d.hospitals if h.hospital_id == subject), None)
    return None


def unit(unit_id: str) -> Optional[Unit]:
    return next((u for u in directory().units if u.unit_id == unit_id), None)


def hospital(hospital_id: str) -> Optional[Hospital]:
    return next((h for h in directory().hospitals if h.hospital_id == hospital_id), None)


def unit_for_tracker(key: str) -> Optional[str]:
    """The unit whose tracker key this is (compared in constant time), or None."""
    import hmac

    found = None
    for u in directory().units:
        # surrogatepass: a lone surrogate in a request is a wrong key, not a server error.
        if u.tracker_key and hmac.compare_digest(
                u.tracker_key.encode("utf-8", "surrogatepass"), key.encode("utf-8", "surrogatepass")):
            found = u.unit_id
    return found


def trackers_configured() -> bool:
    return any(u.tracker_key for u in directory().units)


def public_units() -> list[dict]:
    """What any screen may show about the fleet: no crew phones, no PINs."""
    return [{"unit_id": u.unit_id, "type": u.type, "station": u.station} for u in directory().units]


def public_hospitals() -> list[dict]:
    return [{"hospital_id": h.hospital_id, "name": h.name} for h in directory().hospitals]


def hotline() -> Optional[dict]:
    h = directory().hotline_112
    return {"name": h.name, "phone": h.phone} if h else None

import hashlib
import json
import os
import platform
import uuid
from pathlib import Path


SEED_FILE = Path(__file__).resolve().parents[1] / ".hiveminde_device_seed"


def _read_or_create_seed() -> str:
    try:
        if SEED_FILE.exists():
            return SEED_FILE.read_text().strip()
        seed = uuid.uuid4().hex
        SEED_FILE.write_text(seed)
        return seed
    except Exception:
        # fallback
        return uuid.uuid4().hex


def generate_device_id() -> str:
    seed = _read_or_create_seed()
    hw = str(uuid.getnode())
    os_info = platform.uname().system + "-" + platform.uname().release
    raw = (hw + "|" + os_info + "|" + seed).encode("utf-8")
    dig = hashlib.sha256(raw).hexdigest()[:16]
    return f"hm_{dig}"


def get_device_metadata(device_name: str = None) -> dict:
    return {
        "device_id": generate_device_id(),
        "device_name": device_name or platform.node(),
        "latency_profile_ms": 50,
        "speaker_power_score": 0.5,
        "join_time": int(__import__('time').time()),
    }

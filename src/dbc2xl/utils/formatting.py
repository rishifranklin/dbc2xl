from __future__ import annotations

from typing import Mapping


def frame_id_hex(frame_id: int) -> str:
    # 29-bit IDs can be large; keep consistent hex formatting
    return f"0x{frame_id:X}"


def stringify_choices(choices: Mapping[int, str]) -> str:
    # Stable, readable: "0=Off; 1=On; 2=Fault"
    items = sorted(choices.items(), key=lambda kv: kv[0])
    return "; ".join([f"{k}={v}" for k, v in items])


def safe_str(v: object) -> str:
    if v is None:
        return ""
    return str(v)

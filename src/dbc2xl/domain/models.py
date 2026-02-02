from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class NodeExport:
    name: str
    comment: str | None
    attributes: Mapping[str, object]


@dataclass(frozen=True)
class MessageExport:
    name: str
    frame_id: int
    frame_id_hex: str
    is_extended_frame: bool | None
    length: int
    cycle_time_ms: int | None
    senders: Sequence[str]
    comment: str | None
    attributes: Mapping[str, object]


@dataclass(frozen=True)
class SignalExport:
    message_name: str
    message_frame_id: int
    message_frame_id_hex: str

    name: str
    start: int
    length: int
    byte_order: str | None
    is_signed: bool | None
    is_float: bool | None

    factor: float | None
    offset: float | None
    minimum: float | None
    maximum: float | None
    unit: str | None

    receivers: Sequence[str]
    comment: str | None

    is_multiplexer: bool | None
    multiplexer_ids: Sequence[int] | None
    multiplexer_signal: str | None

    choices: Mapping[int, str]  # value table/enum mapping
    attributes: Mapping[str, object]


@dataclass(frozen=True)
class AttributeExport:
    scope: str           # "node" | "message" | "signal"
    owner: str           # node name / message name / "Message.Signal"
    key: str
    value: object


@dataclass(frozen=True)
class DbcExport:
    nodes: Sequence[NodeExport]
    messages: Sequence[MessageExport]
    signals: Sequence[SignalExport]
    attributes: Sequence[AttributeExport]

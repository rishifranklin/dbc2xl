from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from ..domain.models import (
    AttributeExport,
    DbcExport,
    MessageExport,
    NodeExport,
    SignalExport,
)
from ..utils.formatting import frame_id_hex

logger = logging.getLogger(__name__)


def _get_comment(obj: Any) -> str | None:
    # cantools uses .comment on many objects; sometimes missing
    c = getattr(obj, "comment", None)
    if c is None:
        return None
    c = str(c).strip()
    return c if c else None


def _get_attributes(obj: Any) -> Mapping[str, object]:
    # cantools typically exposes .attributes dict for DBC entities
    attrs = getattr(obj, "attributes", None)
    if isinstance(attrs, dict):
        return attrs
    return {}


def _as_list(v: Any) -> List[str]:
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return [str(x) for x in v]
    return [str(v)]


def _signal_choices(sig: Any) -> Dict[int, str]:
    choices = getattr(sig, "choices", None)
    if isinstance(choices, dict):
        out: Dict[int, str] = {}
        for k, v in choices.items():
            try:
                ik = int(k)
            except Exception:
                continue
            out[ik] = str(v)
        return out
    return {}


def _multiplexer_ids(sig: Any) -> List[int] | None:
    mids = getattr(sig, "multiplexer_ids", None)
    if mids is None:
        return None
    if isinstance(mids, (list, tuple)):
        out: List[int] = []
        for x in mids:
            try:
                out.append(int(x))
            except Exception:
                pass
        return out
    try:
        return [int(mids)]
    except Exception:
        return None


@dataclass(frozen=True)
class CantoolsDbcParser:
    def parse(self, dbc_path: str, encoding: str | None) -> DbcExport:
        try:
            import cantools  # type: ignore
        except ImportError as e:
            raise RuntimeError(
                "cantools is required. Install with: pip install cantools"
            ) from e

        db = cantools.database.load_file(dbc_path, encoding=encoding)

        nodes: List[NodeExport] = []
        for n in getattr(db, "nodes", []) or []:
            nodes.append(
                NodeExport(
                    name=str(getattr(n, "name", "")),
                    comment=_get_comment(n),
                    attributes=_get_attributes(n),
                )
            )

        messages: List[MessageExport] = []
        signals: List[SignalExport] = []
        attributes: List[AttributeExport] = []

        for m in getattr(db, "messages", []) or []:
            fid = int(getattr(m, "frame_id", 0))
            msg_name = str(getattr(m, "name", ""))

            is_ext = getattr(m, "is_extended_frame", None)
            if isinstance(is_ext, bool) is False:
                # some versions may not expose it cleanly
                is_ext = None

            cycle_time = getattr(m, "cycle_time", None)
            cycle_time_ms: int | None
            try:
                cycle_time_ms = int(cycle_time) if cycle_time is not None else None
            except Exception:
                cycle_time_ms = None

            senders = _as_list(getattr(m, "senders", None))
            msg_attrs = _get_attributes(m)

            messages.append(
                MessageExport(
                    name=msg_name,
                    frame_id=fid,
                    frame_id_hex=frame_id_hex(fid),
                    is_extended_frame=is_ext,
                    length=int(getattr(m, "length", 0)),
                    cycle_time_ms=cycle_time_ms,
                    senders=senders,
                    comment=_get_comment(m),
                    attributes=msg_attrs,
                )
            )

            # message attributes flattened
            for k, v in msg_attrs.items():
                attributes.append(
                    AttributeExport(scope="message", owner=msg_name, key=str(k), value=v)
                )

            for s in getattr(m, "signals", []) or []:
                sig_name = str(getattr(s, "name", ""))

                byte_order = getattr(s, "byte_order", None)
                if byte_order is not None:
                    byte_order = str(byte_order)

                is_signed = getattr(s, "is_signed", None)
                if not isinstance(is_signed, bool):
                    is_signed = None

                is_float = getattr(s, "is_float", None)
                if not isinstance(is_float, bool):
                    is_float = None

                receivers = _as_list(getattr(s, "receivers", None))
                sig_attrs = _get_attributes(s)

                mux_sig = getattr(s, "multiplexer_signal", None)
                mux_sig_name = str(getattr(mux_sig, "name", "")) if mux_sig else None

                is_mux = getattr(s, "is_multiplexer", None)
                if not isinstance(is_mux, bool):
                    is_mux = None

                choices = _signal_choices(s)

                signals.append(
                    SignalExport(
                        message_name=msg_name,
                        message_frame_id=fid,
                        message_frame_id_hex=frame_id_hex(fid),
                        name=sig_name,
                        start=int(getattr(s, "start", 0)),
                        length=int(getattr(s, "length", 0)),
                        byte_order=byte_order,
                        is_signed=is_signed,
                        is_float=is_float,
                        factor=getattr(s, "scale", None),
                        offset=getattr(s, "offset", None),
                        minimum=getattr(s, "minimum", None),
                        maximum=getattr(s, "maximum", None),
                        unit=getattr(s, "unit", None),
                        receivers=receivers,
                        comment=_get_comment(s),
                        is_multiplexer=is_mux,
                        multiplexer_ids=_multiplexer_ids(s),
                        multiplexer_signal=mux_sig_name,
                        choices=choices,
                        attributes=sig_attrs,
                    )
                )

                # signal attributes flattened
                owner = f"{msg_name}.{sig_name}"
                for k, v in sig_attrs.items():
                    attributes.append(
                        AttributeExport(scope="signal", owner=owner, key=str(k), value=v)
                    )

        # node attributes flattened
        for n in nodes:
            for k, v in n.attributes.items():
                attributes.append(
                    AttributeExport(scope="node", owner=n.name, key=str(k), value=v)
                )

        return DbcExport(nodes=nodes, messages=messages, signals=signals, attributes=attributes)

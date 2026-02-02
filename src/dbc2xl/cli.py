from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .app import build_app


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="dbc2xlsx",
        description="Convert CAN DBC to an Excel (.xlsx) export.",
    )
    p.add_argument("-i", "--input", required=True, help="Path to input .dbc file")
    p.add_argument("-o", "--output", required=True, help="Path to output .xlsx file")
    p.add_argument(
        "--encoding",
        default=None,
        help="DBC file encoding (optional). Example: utf-8, latin-1",
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )
    return p


def main() -> int:
    args = _build_arg_parser().parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    app = build_app()

    app.convert(
        dbc_path=str(input_path),
        xlsx_path=str(output_path),
        encoding=args.encoding,
    )

    logging.getLogger(__name__).info("Wrote Excel export: %s", output_path)
    return 0

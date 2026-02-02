from __future__ import annotations

import logging
from dataclasses import dataclass

from ..domain.models import DbcExport

logger = logging.getLogger(__name__)


class DbcParser:
    def parse(self, dbc_path: str, encoding: str | None) -> DbcExport:
        raise NotImplementedError


class ExcelWriter:
    def write(self, export: DbcExport, xlsx_path: str) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class ConvertDbcToExcelUseCase:
    parser: DbcParser
    writer: ExcelWriter

    def execute(self, dbc_path: str, xlsx_path: str, encoding: str | None) -> None:
        logger.info("Parsing DBC: %s", dbc_path)
        export = self.parser.parse(dbc_path=dbc_path, encoding=encoding)

        logger.info(
            "Parsed: %d nodes, %d messages, %d signals, %d attributes",
            len(export.nodes),
            len(export.messages),
            len(export.signals),
            len(export.attributes),
        )

        logger.info("Writing XLSX: %s", xlsx_path)
        self.writer.write(export=export, xlsx_path=xlsx_path)

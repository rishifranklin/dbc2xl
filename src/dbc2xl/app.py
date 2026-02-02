from __future__ import annotations

from dataclasses import dataclass

from .adapters.dbc_parser_cantools import CantoolsDbcParser
from .adapters.excel_writer_openpyxl import OpenpyxlExcelWriter
from .use_cases.convert import ConvertDbcToExcelUseCase


@dataclass(frozen=True)
class Application:
    use_case: ConvertDbcToExcelUseCase

    def convert(self, dbc_path: str, xlsx_path: str, encoding: str | None) -> None:
        self.use_case.execute(dbc_path=dbc_path, xlsx_path=xlsx_path, encoding=encoding)


def build_app() -> Application:
    parser = CantoolsDbcParser()
    writer = OpenpyxlExcelWriter()
    use_case = ConvertDbcToExcelUseCase(parser=parser, writer=writer)
    return Application(use_case=use_case)

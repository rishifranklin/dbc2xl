from pathlib import Path

import pytest


def test_import():
    import dbc2xlsx  # noqa: F401


@pytest.mark.skip(reason="Provide a real DBC path to run locally")
def test_convert_smoke(tmp_path: Path):
    from dbc2xlsx.app import build_app

    app = build_app()
    in_dbc = Path("path/to/your.dbc").resolve()
    out_xlsx = tmp_path / "out.xlsx"

    app.convert(dbc_path=str(in_dbc), xlsx_path=str(out_xlsx), encoding=None)
    assert out_xlsx.exists()

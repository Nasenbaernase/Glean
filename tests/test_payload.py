import pathlib

import pandas as pd

from glean_excel.glean_client import build_analysis_payload


def test_build_analysis_payload_includes_metadata_and_records():
    df = pd.DataFrame(
        [
            {"Name": "Alice", "Score": 92},
            {"Name": "Bob", "Score": 88},
        ]
    )
    workbook_path = pathlib.Path("/tmp/report.xlsx")
    payload = build_analysis_payload(df, workbook_path=workbook_path, sheet_name="Results")

    assert payload["workbook"] == "report.xlsx"
    assert payload["sheet"] == "Results"
    assert payload["rowCount"] == 2
    assert payload["columnCount"] == 2
    assert payload["records"] == df.to_dict(orient="records")

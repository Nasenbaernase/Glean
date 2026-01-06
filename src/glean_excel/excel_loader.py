from __future__ import annotations

import pathlib
from typing import List

import pandas as pd


class ExcelLoader:
    """Helpers to inspect and load data from Excel workbooks."""

    @staticmethod
    def list_sheet_names(path: str | pathlib.Path) -> List[str]:
        workbook_path = pathlib.Path(path)
        if not workbook_path.exists():
            raise FileNotFoundError(f"Workbook not found: {workbook_path}")

        excel_file = pd.ExcelFile(workbook_path)
        return list(excel_file.sheet_names)

    @staticmethod
    def load_sheet(path: str | pathlib.Path, sheet_name: str) -> pd.DataFrame:
        workbook_path = pathlib.Path(path)
        if not workbook_path.exists():
            raise FileNotFoundError(f"Workbook not found: {workbook_path}")

        df = pd.read_excel(workbook_path, sheet_name=sheet_name)
        if df.empty:
            raise ValueError(f"Sheet '{sheet_name}' in {workbook_path} is empty.")
        return df


__all__ = ["ExcelLoader"]

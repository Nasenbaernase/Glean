from __future__ import annotations

import pathlib
from typing import Any, Dict, Iterable, List

import pandas as pd
import requests

from .config import GleanConfig


def build_analysis_payload(df: pd.DataFrame, *, workbook_path: pathlib.Path, sheet_name: str) -> Dict[str, Any]:
    """Create the JSON body sent to Glean for AI analysis.

    The payload captures high-level metadata plus the row-level data.
    """

    records: List[Dict[str, Any]] = df.to_dict(orient="records")
    return {
        "workbook": workbook_path.name,
        "sheet": sheet_name,
        "rowCount": len(records),
        "columnCount": len(df.columns),
        "records": records,
    }


class GleanClient:
    """Simple HTTP client for sending Excel data to Glean."""

    def __init__(self, config: GleanConfig):
        self.config = config

    @property
    def _analysis_url(self) -> str:
        return f"{self.config.base_url}/v1/ai/analyze"

    def send_analysis(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST the analysis request to Glean and return the JSON response."""

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "X-Glean-App-Id": self.config.app_id,
            "Content-Type": "application/json",
        }

        response = requests.post(
            self._analysis_url, json=payload, headers=headers, timeout=self.config.timeout
        )
        response.raise_for_status()
        return response.json()

    def send_dataframe(self, df: pd.DataFrame, *, workbook_path: pathlib.Path, sheet_name: str) -> Dict[str, Any]:
        payload = build_analysis_payload(df, workbook_path=workbook_path, sheet_name=sheet_name)
        return self.send_analysis(payload)


__all__ = ["GleanClient", "build_analysis_payload"]

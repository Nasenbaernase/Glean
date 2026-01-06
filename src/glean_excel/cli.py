from __future__ import annotations

import argparse
import json
import pathlib
from typing import List

from .config import GleanConfig
from .excel_loader import ExcelLoader
from .glean_client import GleanClient, build_analysis_payload


def _prompt_for_sheet(sheets: List[str]) -> str:
    print("Available sheets:")
    for idx, name in enumerate(sheets, start=1):
        print(f"  [{idx}] {name}")

    while True:
        choice = input("Select a sheet number to send to Glean: ").strip()
        if not choice.isdigit():
            print("Enter a number corresponding to the sheet.")
            continue
        index = int(choice) - 1
        if 0 <= index < len(sheets):
            return sheets[index]
        print("Selection out of range, try again.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send an Excel sheet to Glean for AI analysis.")
    parser.add_argument("file", type=pathlib.Path, help="Path to the Excel workbook (.xlsx)")
    parser.add_argument("--sheet", help="Worksheet name to send. If omitted, you will be prompted.")
    parser.add_argument("--base-url", help="Glean API base URL (defaults to $GLEAN_BASE_URL or https://api.glean.com)")
    parser.add_argument("--api-key", help="Glean API key (defaults to $GLEAN_API_KEY)")
    parser.add_argument("--app-id", help="Glean application ID (defaults to $GLEAN_APP_ID)")
    parser.add_argument(
        "--timeout", type=int, default=None, help="Request timeout in seconds (defaults to $GLEAN_TIMEOUT or 30)"
    )
    parser.add_argument("--list-sheets", action="store_true", help="Only list sheet names and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Build the payload but do not send it to Glean.")
    parser.add_argument("--output", type=pathlib.Path, help="Optional path to save the JSON payload before sending.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    sheets = ExcelLoader.list_sheet_names(args.file)
    if args.list_sheets:
        print("Sheets found:")
        for name in sheets:
            print(f"- {name}")
        return

    sheet_name = args.sheet or _prompt_for_sheet(sheets)
    if sheet_name not in sheets:
        raise ValueError(f"Sheet '{sheet_name}' not found in workbook. Available sheets: {', '.join(sheets)}")

    dataframe = ExcelLoader.load_sheet(args.file, sheet_name)
    payload = build_analysis_payload(dataframe, workbook_path=args.file, sheet_name=sheet_name)

    if args.output:
        args.output.write_text(json.dumps(payload, indent=2))
        print(f"Payload saved to {args.output}")

    if args.dry_run:
        print("Dry run complete. Preview of payload metadata:")
        print(json.dumps({k: v for k, v in payload.items() if k != "records"}, indent=2))
        return

    config = GleanConfig.from_env(
        base_url=args.base_url,
        api_key=args.api_key,
        app_id=args.app_id,
        timeout=args.timeout,
    )
    client = GleanClient(config)

    response = client.send_analysis(payload)
    print("Analysis request submitted. Response:")
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()

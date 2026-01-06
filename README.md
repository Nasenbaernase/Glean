# Glean Excel Uploader

A small Python CLI that loads data from an Excel workbook, lets you choose which worksheet to use, converts the data to JSON, and sends it to Glean for AI analysis.

## Features
- Lists available worksheets in a workbook and prompts you to choose when omitted.
- Converts the selected worksheet into a JSON payload with row and column metadata.
- Sends the payload to Glean via HTTP with API key and application ID authentication.
- Optional dry-run mode to inspect the payload before sending.
- Can also write the generated payload to disk.

## Requirements
- Python 3.10+
- Dependencies listed in `requirements.txt` (pandas, openpyxl, requests)

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Set your Glean credentials (or pass them as CLI flags):

```bash
export GLEAN_API_KEY="your-api-key"
export GLEAN_APP_ID="your-app-id"
# Optional: export GLEAN_BASE_URL and GLEAN_TIMEOUT
```

Run the CLI, providing your workbook:

```bash
python -m glean_excel path/to/workbook.xlsx
```

If `--sheet` is not specified, you will be prompted to select one. You can list sheets without sending anything:

```bash
python -m glean_excel path/to/workbook.xlsx --list-sheets
```

Send a specific sheet and save the payload locally:

```bash
python -m glean_excel path/to/workbook.xlsx \
  --sheet "Quarterly Forecast" \
  --output payload.json
```

Use dry-run mode to preview metadata without contacting Glean:

```bash
python -m glean_excel path/to/workbook.xlsx --sheet Sheet1 --dry-run
```

Override configuration via flags instead of environment variables:

```bash
python -m glean_excel path/to/workbook.xlsx \
  --sheet Data \
  --base-url https://api.glean.com \
  --api-key "$GLEAN_API_KEY" \
  --app-id "$GLEAN_APP_ID" \
  --timeout 20
```

## How it works
1. The CLI inspects the workbook to list sheet names (`ExcelLoader`).
2. The selected sheet is loaded into a pandas DataFrame.
3. The DataFrame is converted into a JSON payload with basic metadata (`build_analysis_payload`).
4. `GleanClient` sends the payload to `POST {base_url}/v1/ai/analyze` with the appropriate headers.

Customize the endpoint or headers inside `src/glean_excel/glean_client.py` if your Glean deployment expects a different path.

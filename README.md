
---

## Setup (Windows / PowerShell)

### 1. Requirements
- Python 3.12+
- A Gemini API key (free tier available at https://aistudio.google.com/apikey)

### 2. Install dependencies
```powershell
pip install fastapi uvicorn pydantic google-genai pandas pytest
```

### 3. Set your Gemini API key
```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "YOUR_KEY_HERE", "User")
```
**Important:** after setting this, fully close and reopen your terminal (and
VS Code, if you're using its integrated terminal) before the new value takes
effect. Environment variable changes don't apply to already-open sessions.

### 4. Generate the test dataset (if CSVs don't already exist)
```powershell
python generate_data.py
```

### 5. Run the backend
```powershell
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 6. Open the frontend
Just open `index.html` directly in your browser (double-click it, or
right-click → Open with → your browser). It calls the backend at
`http://127.0.0.1:8000/ask` automatically.

---

## Running Tests

```powershell
pytest -v
```

Expected result: **14 passed**.

Note: `test_ai_service.py` makes one real Gemini API call, so running the
full suite uses 1 of your daily Gemini free-tier requests (20/day per
Google account).

---

## Try It Out

In the **Investigate** page or **AI Chat** page, try questions like:

- `Why is TX0096 not settling?` → known amount mismatch (Gateway/Bank: 1000
  INR, Ledger: 950 INR)
- `What happened with TX0001?`
- Any transaction ID from `TX0001` to `TX0100`

Transaction categories in the dataset: `SUCCESS`, `BANK_DELAY`,
`GATEWAY_FAILURE`, `LEDGER_SYNC_ISSUE`, `MISSING_BANK`, `MISSING_LEDGER`,
`AMOUNT_MISMATCH`, `STATUS_MISMATCH`.

---

## Known Limitations

- **No authentication / access control.** Any caller can query any
  transaction ID — there's no per-user permission check. Acceptable for a
  student/demo project, but not production-ready.
- **No rate limiting.** Beyond Gemini's own free-tier quota (20
  requests/day), there's no additional throttling on the `/ask` endpoint.
- **`LEDGER_SYNC_ISSUE` vs `MISSING_LEDGER` are indistinguishable** in the
  current test data — both produce `ledger = None` in `generate_data.py`.
  Not fixed; not blocking normal use.
- **Single-transaction queries only.** The parser extracts one transaction
  ID per question; it doesn't support comparing multiple transactions in
  one request.
- **Gemini free-tier quota** is 20 requests/day per Google account. Each
  real investigation (not a `MISSING_TRANSACTION_ID` short-circuit) uses
  one request.

---

## Security Notes

- The Gemini API key is loaded via `os.getenv("GEMINI_API_KEY")` and is
  never hardcoded or logged.
- The system prompt instructs Gemini to treat transaction records as data
  only, never as instructions — mitigating prompt injection from record
  contents.
- User questions are validated with Pydantic (`min_length=1,
  max_length=500`) to reject empty or oversized input.
- Logs record transaction IDs and outcomes, never the API key or full raw
  records.
- CORS is currently open (`allow_origins=["*"]`) to allow the local
  frontend to call the API during development. Tighten this before any
  real deployment.

---

## License

Student / educational project. No license specified.
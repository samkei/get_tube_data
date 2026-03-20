## Cursor Cloud specific instructions

### Project overview
Get-Tube-Data is a single-file Python script (`get-tube-data.py`) that queries the YouTube Data API v3 to fetch trending video metadata. It also functions as an AWS Lambda handler. See `README.md` for resource type details.

### Running the application
```
. .venv/bin/activate
API_KEY=<your-youtube-api-key> python get-tube-data.py
```
The `API_KEY` environment variable (a Google YouTube Data API v3 key) is **required** for the script to return data. Without it, the script will execute but YouTube API calls will fail with `API_KEY_INVALID`.

### Dependencies
Dependencies are declared in `Pipfile` (requests, boto3, datetime). The `Pipfile.lock` pins versions targeting Python 3.8 that are **incompatible with Python 3.12** (the system Python). The update script uses a standard venv at `.venv/` with `pip install` instead of `pipenv install` from the lockfile to avoid urllib3/six compatibility issues.

### Gotchas
- **No test suite or linter is configured** in this repo. There are no test files, no pytest/unittest setup, and no flake8/pylint/mypy configuration.
- The script auto-executes `handler(None, None)` at the module level (line 267), so importing the module will trigger API calls.
- There are `SyntaxWarning`s on Python 3.12 for unescaped `\d` in regex strings (lines 60, 247) — these are harmless warnings in the existing code.
- The `get-tube-data-aws/` directory contains vendored boto3/botocore for Lambda deployment packaging; it is not used for local development.
- The YouTube Search endpoint (`order=viewCount`) may return empty results even with a valid API key due to quota or access restrictions. The Videos endpoint (`chart=mostPopular`) works reliably for fetching popular video statistics and snippets.
- The `Videos` class constructor always builds both a statistics URL and a snippets URL; when `id=None` (default), the snippets URL construction will fail because `build_url` concatenates `None` to a string.

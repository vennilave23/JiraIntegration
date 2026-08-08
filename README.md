# JiraIntegration

A small Python project to extract Jira issues and serve a basic Streamlit dashboard.

## Quick start

1. Copy `.env.example` to `.env` and set your Jira/Confluence credentials.
2. Create and activate a virtual environment:

```bash
cd /Users/vennilave23/Documents/VSCode_Workspace/JiraIntegration
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the extractor to populate the local SQLite database:

```bash
python -m src.extractor
```

4. Launch the dashboard from the project root:

```bash
streamlit run src/dashboard/streamlit_app.py --server.port 8501
```

5. Open the browser at:

```text
http://localhost:8501
```

## Notes

- `.env` is excluded from git, so put your API email and token there.
- The default local database is `data.db` in the project root.
- If Streamlit cannot find `src`, run from the repository root.

## Recommended workflow

- Set `DB_URL` in `.env` only if you want a custom database path.
- Use `python -m src.extractor` again whenever you want to refresh Jira issues.
- Use `git status` and `git diff` before committing code changes.

## Files of interest

- `architecture.md` — architecture and component overview
- `instructions.md` — workspace instructions and auth guidance
- `src/auth/token_manager.py` — central auth header builder
- `src/jira_client.py` — Jira API client and search logic
- `src/dashboard/streamlit_app.py` — interactive dashboard UI
- `.github/workflows/python-app.yml` — CI workflow

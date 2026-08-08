Jira & Confluence Integration — Architecture
==========================================

Overview
--------
This project extracts Jira issues (stories) and Confluence pages, stores normalized records in a database, and serves an interactive Streamlit dashboard.

Components
----------
- `src/auth/token_manager.py` — Centralized token acquisition, caching and refresh.
- `src/jira_client.py` — Jira API wrapper (uses token from token_manager).
- `src/confluence_client.py` — Confluence API wrapper.
- `src/extractor.py` — Orchestrates incremental fetch and normalization.
- `src/models.py` and `src/db.py` — SQLAlchemy models and DB helpers.
- `src/dashboard/streamlit_app.py` — Streamlit dashboard reading from DB.
- `instructions.md` — Workspace master instructions and token guidance.

Auth
----
Preferred model: service account (app-level) using OAuth2 with automatic refresh. For Jira Server/Data Center, verify supported flows; if OAuth2 client-credentials is not available, use an app password or OAuth1.0a as fallback. Never commit secrets.

Token storage and lifecycle
---------------------------
- Local dev: environment variables and `.env` file (see `.env.example`).
- Prod: use a secrets manager (HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault).
- Tokens are short-lived and refreshed automatically by `token_manager`.

Data flow
---------
1. `extractor` requests a token from `token_manager`.
2. Token is used by `jira_client`/`confluence_client` to query APIs.
3. Extracted objects are normalized and upserted into DB via SQLAlchemy.
4. Streamlit reads DB and builds visualizations.

Security
--------
- Do not commit `.env` or any secrets.
- Restrict local token cache files to user-only permissions when used.
- Use HTTPS endpoints and verify SSL.

Next steps
----------
- Implement clients and extractor, create tests and CI, and iterate on dashboard visuals.

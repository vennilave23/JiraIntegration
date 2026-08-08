# JiraIntegration Workspace Instructions (master)

This file documents workspace setup, token handling, and developer notes.

Token guidance
--------------
- For local development, copy `.env.example` to `.env` and set the values.
- Do not commit `.env`.
- For production, provision secrets in a secret manager and set the environment variables in your deployment environment.

API token notes
---------------
- You can provide an Atlassian Cloud API token (email + API token) for quick access. Add `JIRA_API_EMAIL` and `JIRA_API_TOKEN` to your local `.env` (or `CONFLUENCE_API_EMAIL` / `CONFLUENCE_API_TOKEN`).
- Do NOT paste API tokens into chat or commit them. If you accidentally exposed a token, rotate/revoke it immediately and generate a new one.

How to rotate an Atlassian Cloud API token
-----------------------------------------
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens and sign in.
2. Find the token you exposed and click **Delete** (or **Revoke**).
3. Click **Create API token**, give it a label (e.g., "JiraIntegration local"), and copy the new token.
4. Replace `JIRA_API_TOKEN` in your local `.env` with the new token and restart the extractor/dashboard.
5. If the token was committed anywhere, rotate other affected credentials and inform your security team.


Token manager
-------------
- The project uses `src/auth/token_manager.py` as the canonical place to obtain and refresh tokens. All API clients import and call `get_token(service_name)`.
- Use `service_name` values `jira` and `confluence`.

VS Code
-------
- Recommended: point `python.envFile` to `${workspaceFolder}/.env` in `.vscode/settings.json`. Do not put secrets directly into workspace settings.

Security checklist
------------------
1. Verify no secrets are committed.
2. Restrict local token cache file to user-only permissions (`chmod 600`).
3. Use HTTPS and validate certificates.

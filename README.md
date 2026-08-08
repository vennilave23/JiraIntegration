# JiraIntegration

Quick start
-----------
1. Copy `.env.example` to `.env` and set values.
2. Create a Python venv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run extractor once to populate local DB:

```bash
python -m src.extractor
```

4. Run Streamlit dashboard:

```bash
streamlit run src/dashboard/streamlit_app.py
```

Files of interest
- `architecture.md` — system architecture
- `instructions.md` — token instructions and workspace master file
- `src/auth/token_manager.py` — central token helper

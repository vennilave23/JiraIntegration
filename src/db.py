import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Default to a project-local SQLite DB (absolute path) so apps started
# from other working directories find the same file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
default_db = PROJECT_ROOT / 'data.db'

# Read environment override but make relative sqlite paths project-root-relative
env_db = os.getenv('DB_URL')
if env_db:
    if env_db.startswith('sqlite:///'):
        rel = env_db[len('sqlite:///'):]
        # if the path part is relative, resolve it inside the project
        if rel and not Path(rel).is_absolute():
            DB_URL = f"sqlite:///{PROJECT_ROOT / rel}"
        else:
            DB_URL = env_db
    else:
        DB_URL = env_db
else:
    DB_URL = f'sqlite:///{default_db}'

engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

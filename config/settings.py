from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"
EVIDENCE_DIR = STORAGE_DIR / "evidence"
FRAGMENTS_DIR = STORAGE_DIR / "fragments"
RECOVERED_DIR = STORAGE_DIR / "recovered"
REPORTS_DIR = STORAGE_DIR / "reports"
TEMP_DIR = STORAGE_DIR / "temp"

for folder in [DATA_DIR, STORAGE_DIR, EVIDENCE_DIR, FRAGMENTS_DIR, RECOVERED_DIR, REPORTS_DIR, TEMP_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

class Settings:
    APP_NAME = "AI Recovery Platform"
    DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'recovery.db'}")
    SECRET_KEY = os.getenv("SECRET_KEY", "local-dev-key")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "local")
    AI_MODEL = os.getenv("AI_MODEL", "local-fallback")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "200"))
    EVIDENCE_STORAGE = str(EVIDENCE_DIR)
    FRAGMENT_STORAGE = str(FRAGMENTS_DIR)
    RECOVERED_STORAGE = str(RECOVERED_DIR)
    REPORT_STORAGE = str(REPORTS_DIR)
    TEMP_STORAGE = str(TEMP_DIR)

settings = Settings()

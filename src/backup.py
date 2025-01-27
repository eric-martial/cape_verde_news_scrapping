# backup.py
import shutil
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path("data/backups")
DB_PATH = Path("scraper_database.db")


def backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"scraper_db_{datetime.now():%Y%m%d_%H%M%S}.db"
    shutil.copy(DB_PATH, backup_path)

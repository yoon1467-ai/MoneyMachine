from pathlib import Path
from datetime import datetime


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"


def write_log(message):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")

from pathlib import Path

from app.services.config_service import load_config
from app.services.history_service import init_db


def initialize_app():
    config = load_config()

    Path(config["article_save_dir"]).mkdir(parents=True, exist_ok=True)
    Path("data").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    Path("exports").mkdir(parents=True, exist_ok=True)

    init_db()

    return True

from pathlib import Path
import shutil

from app.services.history_service import clear_history


def clear_test_data():
    articles_dir = Path("articles")

    if articles_dir.exists():
        shutil.rmtree(articles_dir)

    articles_dir.mkdir(parents=True, exist_ok=True)

    clear_history()

    return True

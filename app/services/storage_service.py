from pathlib import Path
from datetime import datetime
import re

from app.services.config_service import load_config


def make_safe_filename(text):
    text = text.strip()
    text = re.sub(r"[\\/:*?\"<>|]", "", text)
    text = re.sub(r"\s+", "_", text)

    if not text:
        text = "article"

    return text


def save_content(keyword, content, suffix="content"):
    config = load_config()
    save_root = config["article_save_dir"]

    safe_keyword = make_safe_filename(keyword)

    today = datetime.now().strftime("%Y-%m-%d")
    save_dir = Path(save_root) / today
    save_dir.mkdir(parents=True, exist_ok=True)

    file_path = save_dir / f"{safe_keyword}_{suffix}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path

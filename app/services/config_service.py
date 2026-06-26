import json
from pathlib import Path


DEFAULT_CONFIG = {
    "app_name": "Money Machine Pro",
    "version": "v2.8",
    "openai_model": "gpt-5",
    "article_save_dir": "articles",
    "recommend_keyword_count": 10,
    "keyword_candidate_limit": 80,
    "article_min_length": 2500,
    "auto_exclude_years": ["2024", "2025"],
}


def load_config():
    config_path = Path("config") / "settings.json"

    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)

        return DEFAULT_CONFIG

    with open(config_path, "r", encoding="utf-8") as f:
        user_config = json.load(f)

    config = DEFAULT_CONFIG.copy()
    config.update(user_config)

    return config

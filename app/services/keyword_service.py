from pathlib import Path
import requests
import urllib.parse
from app.services.history_service import get_written_keywords as get_db_written_keywords

SEED_KEYWORDS = [
    "신용점수",
    "ISA 계좌",
    "ETF 투자",
    "연금저축",
    "IRP",
    "자동차보험",
    "실손보험",
    "전세대출",
    "주택담보대출",
    "청년도약계좌",
    "정부지원금",
    "소상공인 지원금",
    "애플페이",
    "갤럭시페이",
    "통신비 절약",
    "청년 지원금",
    "대출 갈아타기",
    "카드 포인트",
    "예금 금리",
    "적금 추천",
]


def get_written_keywords():
    written = set()

    written.update(get_db_written_keywords())

    articles_dir = Path("articles")

    if not articles_dir.exists():
        return written

    for file in articles_dir.rglob("*.md"):
        name = file.stem.replace("_", " ").strip()

        for suffix in [" blog", " shorts", " image prompts", "content"]:
            if name.endswith(suffix):
                name = name.replace(suffix, "").strip()

        if name:
            written.add(name)

    return written


def fetch_google_suggestions(keyword):
    try:
        url = "https://suggestqueries.google.com/complete/search"
        params = {
            "client": "firefox",
            "hl": "ko",
            "q": keyword,
        }

        response = requests.get(
            url,
            params=params,
            timeout=3,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        if response.status_code != 200:
            return []

        data = response.json()

        if len(data) < 2:
            return []

        return data[1]

    except Exception:
        return []


def fetch_naver_suggestions(keyword):
    try:
        encoded = urllib.parse.quote(keyword)

        url = (
            "https://ac.search.naver.com/nx/ac"
            f"?q={encoded}"
            "&con=0"
            "&frm=nv"
            "&ans=2"
            "&r_format=json"
            "&r_enc=UTF-8"
            "&st=100"
        )

        response = requests.get(
            url,
            timeout=3,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        if response.status_code != 200:
            return []

        data = response.json()
        results = []

        for group in data.get("items", []):
            for item in group:
                if isinstance(item, list) and len(item) > 0:
                    results.append(str(item[0]))

        return results

    except Exception:
        return []


def is_duplicate_keyword(keyword, written_keywords):
    keyword_clean = keyword.replace("_", " ").strip()

    for written in written_keywords:
        written_clean = written.replace("_", " ").strip()

        if keyword_clean == written_clean:
            return True

        if keyword_clean in written_clean:
            return True

        if written_clean in keyword_clean:
            return True

    return False


def collect_suggestions():
    result = []

    for seed in SEED_KEYWORDS:
        result.append(seed)
        result.extend(fetch_google_suggestions(seed))
        result.extend(fetch_naver_suggestions(seed))

    cleaned = []

    for item in result:
        text = str(item).strip()

        if not text:
            continue

        if len(text) < 2:
            continue

        if "2024" in text or "2025" in text:
            continue

        if text not in cleaned:
            cleaned.append(text)

    return cleaned[:100]


def get_filtered_keyword_candidates():
    written_keywords = get_written_keywords()
    candidates = collect_suggestions()

    filtered_candidates = []

    for keyword in candidates:
        if is_duplicate_keyword(keyword, written_keywords):
            continue

        filtered_candidates.append(keyword)

    return filtered_candidates[:80], written_keywords

from datetime import datetime

from app.ai.openai_client import ask_gpt
from app.services.config_service import load_config
from app.services.keyword_service import (
    get_filtered_keyword_candidates,
    is_duplicate_keyword,
)


def recommend_keywords():
    config = load_config()

    now = datetime.now()
    current_date = now.strftime("%Y년 %m월")
    current_year = now.year

    candidates, written_keywords = get_filtered_keyword_candidates()

    candidate_limit = config["keyword_candidate_limit"]
    recommend_count = config["recommend_keyword_count"]
    exclude_years = config["auto_exclude_years"]

    joined_candidates = "\n".join(
        f"- {item}" for item in candidates[:candidate_limit]
    )

    exclude_text = ", ".join(exclude_years)

    prompt = f"""
현재 날짜는 {current_date}입니다.

아래 후보 키워드는 구글 자동완성, 네이버 자동완성, 기본 시드 키워드를 합쳐 만든 목록입니다.

이미 작성한 글과 비슷한 키워드는 제외했습니다.

후보 키워드:
{joined_candidates}

이 후보 중에서 대한민국 블로그/애드센스용으로 좋은 키워드 {recommend_count}개만 골라주세요.

조건:
- 반드시 {current_year}년 현재 기준
- {exclude_text}처럼 지난 연도 키워드 제외
- 이미 작성한 글과 비슷한 주제 제외
- 오래된 정책, 종료된 지원금, 지난 이벤트 제외
- 클릭률이 높을 만한 제목형 키워드 우선
- 광고 단가가 비교적 높을 가능성이 있는 주제 우선
- 금융, 보험, 대출, 정부지원금, IT, 생활정보 중심
- 너무 광범위한 단어보다 롱테일 키워드 우선
- 설명은 짧게
- 반드시 아래 형식만 출력

출력 형식:
키워드|추천점수|이유

예시:
신용점수 올리는 방법|95|금융 검색 수요와 광고 가치가 높음
"""

    text = ask_gpt(prompt)

    keywords = []

    for line in text.splitlines():
        if "|" not in line:
            continue

        parts = line.split("|")

        if len(parts) < 3:
            continue

        keyword = parts[0].strip()
        score = parts[1].strip()
        reason = parts[2].strip()

        if any(year in keyword for year in exclude_years):
            continue

        if is_duplicate_keyword(keyword, written_keywords):
            continue

        keywords.append({
            "keyword": keyword,
            "score": score,
            "reason": reason,
        })

    return keywords[:recommend_count]

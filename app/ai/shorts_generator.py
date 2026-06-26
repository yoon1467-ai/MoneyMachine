from app.ai.openai_client import ask_gpt


def generate_shorts_script(keyword, article):
    prompt = f"""
아래 블로그 글을 바탕으로 유튜브 쇼츠 대본을 만들어줘.

주제:
{keyword}

블로그 글:
{article[:6000]}

조건:
- 30~45초 쇼츠
- 첫 3초 후킹 문장 강하게
- 장면 구성 6개
- 각 장면별 자막 포함
- 나레이션 포함
- 썸네일 문구 3개
- 쇼츠 제목 5개
- 해시태그 10개
- 너무 과장하지 말 것
- 한국어로 작성

출력 형식:

## 쇼츠 제목 후보

## 썸네일 문구

## 30~45초 대본

## 장면 구성

## 자막

## 해시태그
"""

    return ask_gpt(prompt)

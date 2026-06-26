from app.ai.openai_client import ask_gpt


def generate_image_prompts(keyword, article_text=""):
    prompt = f"""
아래 주제와 글 내용을 바탕으로 블로그/쇼츠용 이미지 프롬프트를 만들어줘.

주제:
{keyword}

글 내용:
{article_text[:5000]}

조건:
- 한국 블로그에 어울리는 이미지
- 과도한 텍스트 포함 금지
- 썸네일 문구는 별도로 제공
- 실제 이미지 생성 AI에 바로 넣을 수 있게 작성
- 깔끔하고 전문적인 스타일
- 금융/생활정보/IT 콘텐츠에 어울리는 스타일

출력 형식:

# 대표 이미지 프롬프트

# 본문 이미지 프롬프트 1

# 본문 이미지 프롬프트 2

# 쇼츠 썸네일 이미지 프롬프트

# 썸네일 문구 후보 5개

# 이미지 ALT 텍스트 5개
"""

    return ask_gpt(prompt)

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY가 .env 파일에 없습니다.")

client = OpenAI(api_key=api_key)


def generate_article(keyword):
    prompt = f"""
당신은 SEO 전문 블로그 작가입니다.

주제: {keyword}

조건
- 2000자 이상
- Markdown 형식
- 표 1개 포함
- FAQ 5개 포함
- 결론 포함
- 사람이 쓴 것처럼 자연스럽게 작성
"""

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content

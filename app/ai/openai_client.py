from openai import OpenAI
from dotenv import load_dotenv
import os

from app.services.config_service import load_config

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY가 .env 파일에 없습니다.")

client = OpenAI(api_key=api_key)


def ask_gpt(prompt, system_prompt=None, model=None):
    config = load_config()
    selected_model = model or config["openai_model"]

    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model=selected_model,
        messages=messages,
    )

    return response.choices[0].message.content

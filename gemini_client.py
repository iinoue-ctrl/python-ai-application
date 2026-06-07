import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash"


def configure():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY が設定されていません。.env ファイルに記載してください。"
        )
    genai.configure(api_key=api_key)


def generate(prompt: str, model_name: str = DEFAULT_MODEL, temperature: float = 0.7) -> str:
    configure()
    model = genai.GenerativeModel(
        model_name,
        generation_config={"temperature": temperature},
    )
    response = model.generate_content(prompt)
    return response.text


def stream_generate(prompt: str, model_name: str = DEFAULT_MODEL, temperature: float = 0.7):
    configure()
    model = genai.GenerativeModel(
        model_name,
        generation_config={"temperature": temperature},
    )
    for chunk in model.generate_content(prompt, stream=True):
        if chunk.text:
            yield chunk.text

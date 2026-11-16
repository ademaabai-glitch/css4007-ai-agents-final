"""Creates the chat model. The key comes from the environment, never from code."""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

SYSTEM_PROMPT = (
    "You are ShopBuddy, an assistant that helps people find products in local "
    "shops (flowers, clothing, accessories). You do not have shop data yet, so "
    "do not invent products, prices or stock. If you lack information, say so."
)


def make_llm():
    key = os.environ.get("LLM_API_KEY")
    if not key:
        raise RuntimeError("LLM_API_KEY is not set. Copy .env.example to .env and fill it in.")
    return ChatOpenAI(model=os.environ.get("LLM_MODEL") or "gpt-4o-mini",
                      api_key=key, temperature=0)


def ask(llm, user_text: str) -> str:
    """One request to the model. Returns the reply text; errors become a clear message."""
    if not user_text or not user_text.strip():
        return "Please write what you are looking for."
    try:
        reply = llm.invoke([("system", SYSTEM_PROMPT), ("human", user_text.strip())])
        return reply.content
    except Exception as e:  # network error, bad key, rate limit
        return f"Sorry, the model request failed: {type(e).__name__}"

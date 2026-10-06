import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()


LLM_ENABLED = (
    os.getenv("LLM_ENABLED", "false").lower()
    == "true"
)

LLM_API_URL = os.getenv("LLM_API_URL", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "")


SYSTEM_PROMPT = """
You are the reasoning layer of a local Linux assistant.

You DO NOT execute shell commands directly.

You may only recommend one of the registered tools.

Available tools:

system
processes
storage
largest
projects
search
website

Return JSON only:

{
  "tool": "tool_name",
  "argument": "optional argument"
}

If no tool can safely satisfy the request:

{
  "tool": "none",
  "argument": ""
}
"""


def enabled():
    return (
        LLM_ENABLED
        and bool(LLM_API_URL)
        and bool(LLM_API_KEY)
        and bool(LLM_MODEL)
    )


def ask(user_text):

    if not enabled():
        return None

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_text,
            },
        ],
        "temperature": 0,
    }

    try:

        response = requests.post(
            LLM_API_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        content = (
            data["choices"][0]
            ["message"]
            ["content"]
        )

        return json.loads(content)

    except Exception as e:

        print(
            f"⚠️ LLM unavailable: {e}"
        )

        return None

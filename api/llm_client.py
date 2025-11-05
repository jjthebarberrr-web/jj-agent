"""LLM client wrapper for OpenAI API."""

from typing import Optional
import os
from openai import AsyncOpenAI


class LLMClient:
    """Wrapper for OpenAI API client."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.model = model
        self.client = AsyncOpenAI(api_key=self.api_key)

    @property
    def chat(self):
        """Access chat completions."""
        return self.client.chat.completions

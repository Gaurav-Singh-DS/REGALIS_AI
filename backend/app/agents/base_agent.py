
import os
from abc import ABC, abstractmethod
from ..services.ai_service import ai_service


class BaseAgent(ABC):
    def __init__(self, name: str, system_prompt_path: str):
        self.name = name

        # Prompts are stored in app/prompts, alongside the app package.
        prompts_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "prompts",
        )
        prompt_full_path = os.path.join(prompts_dir, system_prompt_path)

        with open(prompt_full_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    @abstractmethod
    async def run(self, task: str, context: dict) -> dict:
        pass

    async def call_ai(self, prompt: str) -> str:
        return await ai_service.generate_text(prompt, self.system_prompt)

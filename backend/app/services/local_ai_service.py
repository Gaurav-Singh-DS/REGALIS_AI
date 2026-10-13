import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class LocalAIService:
    """
    Local AI service integration using Ollama.
    Used for local E2E testing and prompt tuning.
    """
    def __init__(self, model_name: str = "qwen2.5-coder:3b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        logger.info(f"Local AI Service initialized with model {self.model_name} at {self.base_url}")

    async def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        """
        Sends a prompt to the local Ollama instance.
        """
        try:
            # Ollama API expects a specific JSON format
            payload = {
                "model": self.model_name,
                "prompt": f"SYSTEM: {system_instruction}\n\nUSER: {prompt}",
                "stream": False
            }
            
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "No response received from local AI.")
            
        except Exception as e:
            logger.error(f"Local AI Error: {e}")
            return f"Local AI Error: {str(e)}"

# Singleton instance
local_ai_service = LocalAIService()

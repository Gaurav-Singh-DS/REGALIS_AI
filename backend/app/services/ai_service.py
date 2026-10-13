import os
from typing import Optional, Dict, Any
import logging
from .local_ai_service import local_ai_service

# In a real GCP environment, we use the official Vertex AI SDK
# For local dev, we'll provide a MockAI response to avoid API key errors during logic build
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part, SafetySetting
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    """
    Centralized AI service abstraction for REGREPORT AI.
    Handles all interactions with Gemini via Vertex AI, or Local AI via Ollama.
    """
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.ai_mode = os.getenv("AI_MODE", "mock") # Options: mock, local, prod
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

        if self.ai_mode == "prod" and VERTEX_AI_AVAILABLE:
            # Initialize Vertex AI
            vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("REGION", "us-central1"))
            self.model = GenerativeModel(self.model_name)
            logger.info(f"Vertex AI initialized with model {self.model_name}")
        elif self.ai_mode == "local":
            logger.info("AI Service running in LOCAL mode (Ollama)")
        else:
            logger.info("AI Service running in MOCK mode for local development")

    async def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        """
        Generates a response from the selected AI provider.
        """
        if self.ai_mode == "local":
            return await local_ai_service.generate_text(prompt, system_instruction)

        if self.ai_mode == "mock" or not VERTEX_AI_AVAILABLE:
            return self._get_mock_response(prompt, system_instruction)

        try:
            # We combine system instruction and prompt for the API call
            full_prompt = f"SYSTEM INSTRUCTION:\n{system_instruction}\n\nUSER REQUEST:\n{prompt}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return "Error generating response from AI."

    def _get_mock_response(self, prompt: str, system_instruction: str) -> str:
        """
        Returns structured, professional mock responses as a 'Chief Risk Architect'
        to allow frontend/orchestrator development.
        """
        prompt_lower = prompt.lower()

        if "root cause" in prompt_lower or "investigate" in prompt_lower:
            return (
                "### 🛡️ Executive Summary: Credit Risk Anomaly\n"
                "**Assessment:** High-Criticality Deviation in Credit Card Portfolio Risk Classification.\n"
                "**Finding:** A systemic shift in risk bucket distribution was identified, causing an artificial spike in High-Risk population.\n\n"
                "### 🔍 Root Cause Analysis (RCA)\n"
                "The anomaly is attributed to a logic modification in the risk scoring engine.\n"
                "- **Primary Driver:** Update to the `risk_threshold` variable in the risk classification pipeline.\n"
                "- **Technical Root Cause:** In `customer_risk.sas` (line 12), the threshold for 'High Risk' was lowered from **600** to **650**.\n"
                "- **Policy Alignment:** This change contradicts the `risk_classification_policy.md` Section 4.2.1, which mandates a minimum threshold of 600 for the current fiscal quarter.\n\n"
                "### 📉 Impact Assessment\n"
                "- **Population Shift:** ~56% increase in customers categorized as 'High Risk'.\n"
                "- **Capital Reserve Impact:** Potential over-provisioning of reserves due to inflated risk metrics.\n"
                "- **Reporting Risk:** High probability of regulatory inquiry if reported as-is.\n\n"
                "### ✅ Recommended Remediation\n"
                "1. Revert `customer_risk.sas` line 12 to threshold `600`.\n"
                "2. Trigger a full re-run of the Sept 2026 risk batch.\n"
                "3. Update the internal policy log to document the unauthorized change."
            )

        if "explain transformation" in prompt_lower or "sas" in prompt_lower:
            return (
                "### 🛠️ SAS Code Analysis: `customer_risk.sas`\n"
                "**Objective:** Evaluate the data transformation logic for risk bucket assignment.\n\n"
                "**Analysis:**\n"
                "The SAS code contains a specific rule updated in September 2026. The logic implements a conditional threshold check:\n"
                "```sas\n"
                "if credit_score >= 650 then risk_category = 'High';\n"
                "else risk_category = 'Medium';\n"
                "```\n"
                "**Finding:** This modification lowered the risk threshold from **600 to 650**. Consequently, a large volume of customers who previously qualified as 'Medium Risk' have been shifted to 'High Risk', explaining the 56% increase in the high-risk population."
            )

        return (
            "### 🤖 System Message\n"
            "This is a mock AI response generated by the **Chief Risk Architect** persona. "
            "In production mode, this will be replaced by live analysis from Gemini 1.5 Pro via Vertex AI."
        )

# Singleton instance
ai_service = AIService()

from .base_agent import BaseAgent

class CodeAgent(BaseAgent):
    def __init__(self):
        super().__init__("Code Analysis Agent", "code_explanation.txt")

    async def run(self, task: str, context: dict) -> dict:
        # In a real app, this would read the file from disk
        code_snippet = "/* SAS Logic */ IF portfolio_type = 'CreditCard' AND credit_score < 650 THEN risk_category = 'High';"
        prompt = f"Explain this code in business terms: {code_snippet}\nTask: {task}"
        response = await self.call_ai(prompt)
        return {"agent": self.name, "finding": response, "status": "completed"}

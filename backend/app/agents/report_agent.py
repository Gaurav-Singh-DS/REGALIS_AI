from .base_agent import BaseAgent

class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__("Report Analysis Agent", "report_analysis.txt")

    async def run(self, task: str, context: dict) -> dict:
        metrics = context.get("metrics", [])
        prompt = f"Analyze these metrics for anomalies: {metrics}\nTask: {task}"
        response = await self.call_ai(prompt)
        return {"agent": self.name, "finding": response, "status": "completed"}

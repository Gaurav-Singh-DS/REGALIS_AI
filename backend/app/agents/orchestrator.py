import asyncio
from .report_agent import ReportAgent
from .code_agent import CodeAgent
from .knowledge_agent import KnowledgeAgent
from ..services.ai_service import ai_service
from ..services.analytics_service import AnalyticsService

class OrchestratorAgent:
    def __init__(self):
        self.analytics = AnalyticsService()
        self.agents = {
            "report": ReportAgent(),
            "code": CodeAgent(),
            "knowledge": KnowledgeAgent()
        }

    async def investigate(self, report_id: str, metrics: list):
        # 1. DETERMINISTIC STEP: Detect Anomalies first
        # This ensures the AI is working with facts, not guesses.
        anomalies = self.analytics.detect_anomalies(metrics)
        
        if not anomalies:
            return {"status": "No significant anomalies detected", "root_cause": "N/A"}

        # 2. Identify the top anomaly to investigate
        main_anomaly = anomalies[0] # Simplification for MVP
        
        # 3. AI STEP: Initial Analysis
        report_finding = await self.agents["report"].run(
            f"The system detected a {main_anomaly['severity']} anomaly in {main_anomaly['metric_name']} "
            f"with a change of {main_anomaly['delta_pct']}%.", 
            {"metrics": metrics}
        )
        
        # 4. Parallel Investigation (Code + Knowledge)
        code_task = self.agents["code"].run(
            f"Explain why {main_anomaly['metric_name']} shifted by {main_anomaly['delta_pct']}%", {}
        )
        knowledge_task = self.agents["knowledge"].run(
            f"Find the specific regulatory rule or threshold that justifies the change in {main_anomaly['metric_name']} for NovaBank", {}
        )
        
        code_finding, knowledge_finding = await asyncio.gather(code_task, knowledge_task)
        
        # 5. Final Synthesis
        synthesis_prompt = (
            f"Identify the root cause based on this situational data:\n"
            f"Anomaly: {main_anomaly['metric_name']} ({main_anomaly['delta_pct']}%)\n"
            f"Report Analysis: {report_finding['finding']}\n"
            f"Code Analysis: {code_finding['finding']}\n"
            f"Knowledge Analysis: {knowledge_finding['finding']}"
        )
        
        final_analysis = await ai_service.generate_text(
            synthesis_prompt, 
            system_instruction="You are the Chief Risk Architect. Synthesize the findings into a structured audit-ready report."
        )
        
        return {
            "detected_anomaly": main_anomaly,
            "root_cause": final_analysis,
            "evidence": [report_finding, code_finding, knowledge_finding],
            "confidence": "85%",
            "status": "Requires Human Review"
        }

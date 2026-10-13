from .base_agent import BaseAgent
from ..services.knowledge_service import KnowledgeService

class KnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__("Regulatory Knowledge Agent", "root_cause.txt")
        self.knowledge_service = KnowledgeService()

    async def run(self, task: str, context: dict) -> dict:
        # 1. Retrieve relevant policy snippets based on the task
        context_text = await self.knowledge_service.retrieve_relevant_context(task)
        
        # 2. Feed the context into the AI
        prompt = f"CONTEXT FROM REGULATORY POLICIES:\n{context_text}\n\nTASK:\n{task}"
        response = await self.call_ai(prompt)
        
        return {
            "agent": self.name, 
            "finding": response, 
            "sources": ["risk_classification_policy.md"],
            "status": "completed"
        }

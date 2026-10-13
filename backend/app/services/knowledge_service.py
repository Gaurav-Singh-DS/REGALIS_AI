import os
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class KnowledgeService:
    """
    Knowledge Retrieval Service (RAG).
    For the MVP, we use a document-based retrieval system.
    """
    def __init__(self):
        self.docs_dir = "data/synthetic"
        # Cache for loaded documents
        self.knowledge_cache = {}

    def _load_document(self, filename: str) -> str:
        if filename in self.knowledge_cache:
            return self.knowledge_cache[filename]
        
        path = os.path.join(self.docs_dir, filename)
        try:
            with open(path, "r") as f:
                content = f.read()
                self.knowledge_cache[filename] = content
                return content
        except Exception as e:
            logger.error(f"Error loading knowledge document {filename}: {e}")
            return ""

    async def retrieve_relevant_context(self, query: str) -> str:
        """
        Retrieves relevant snippets from the knowledge base based on the query.
        In this MVP, we perform a keyword-based scan across our policy files.
        """
        # List of relevant policy files
        policy_files = ["risk_classification_policy.md"]
        all_relevant_text = []

        for file in policy_files:
            content = self._load_document(file)
            # Simple semantic split: retrieve sections that match keywords in the query
            # In a full version, we would use Vertex AI Vector Search
            sections = content.split("## ")
            for section in sections:
                # If the section contains keywords from the query, keep it
                # (e.g., "risk", "credit card", "threshold")
                if any(word in section.lower() for word in ["risk", "threshold", "credit", "classification"]):
                    all_relevant_text.append(f"Source [{file}]:\n{section}")

        if not all_relevant_text:
            return "No specific regulatory policy found matching the query."

        return "\n\n".join(all_relevant_text)

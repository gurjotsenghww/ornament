from typing import Dict, Any, List, Optional
from ornament.agents.base import BaseAgent, AgentRole
from ornament.files.file_manager import FileManager
from ornament.rag.vector_store import default_vector_store
from ornament.models.provider.base import ModelProvider

class DebugAgent(BaseAgent):
    """
    Debug Agent (Section 7, 14):
    Specializes in root-cause isolation.
    Inspects symptoms, files, routes, and console logs, querying RAG to return structured diagnosis.
    """

    def __init__(
        self,
        task: str,
        file_manager: FileManager,
        model_provider: ModelProvider,
        error_context: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
        depth: int = 1
    ):
        super().__init__(role=AgentRole.DEBUG_AGENT, task=task, parent_id=parent_id, depth=depth)
        self.file_manager = file_manager
        self.model_provider = model_provider
        self.error_context = error_context or {}

    async def execute(self) -> Dict[str, Any]:
        # 1. Retrieve targeted knowledge from RAG
        rag_context = default_vector_store.search(f"debugging {self.state.task} routes navigation", top_k=2)
        rag_text = "\n".join([f"- {doc['title']}: {doc['content']}" for doc in rag_context])

        # 2. Inspect project files relating to task
        project_files = self.file_manager.list_files()
        relevant_files = [f for f in project_files if any(k in f.lower() for k in ["navbar", "nav", "route", "header", "contact"])]

        inspected_content = {}
        for rf in relevant_files[:4]:
            try:
                inspected_content[rf] = self.file_manager.read_file(rf)
            except Exception:
                pass

        # 3. Model diagnosis prompt
        prompt = f"""
Task: Investigate bug report: "{self.state.task}"
Error Context: {self.error_context}

Available Relevant Project Files:
{list(inspected_content.keys())}

Inspected Contents:
{inspected_content}

Relevant Web Engineering Standards (RAG):
{rag_text}

Analyze the root cause with high precision.
Return a structured JSON diagnosis matching:
{{
    "root_cause": "<detailed root cause>",
    "affected_files": ["<file_path>"],
    "recommended_fix": "<smallest safe change to solve the problem>",
    "confidence": 0.95
}}
"""
        response_text = await self.model_provider.generate(
            prompt,
            system="You are an expert Autonomous Debug Agent. Follow the Minimal Change Policy. Locate the exact line and file causing the issue. Return valid JSON only."
        )

        from ornament.models.inference.engine import InferenceEngine
        diagnosis = InferenceEngine.extract_json(response_text)
        return {
            "task_id": self.id,
            "status": "diagnosed",
            "root_cause": diagnosis.get("root_cause", "Unspecified root cause"),
            "affected_files": diagnosis.get("affected_files", []),
            "recommended_fix": diagnosis.get("recommended_fix", ""),
            "confidence": diagnosis.get("confidence", 0.9)
        }

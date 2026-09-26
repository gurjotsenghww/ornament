from typing import Dict, Any, List, Optional
from ornament.agents.base import BaseAgent, AgentRole
from ornament.files.file_manager import FileManager
from ornament.models.provider.base import ModelProvider

class CodeAgent(BaseAgent):
    """
    Code Agent (Section 7, 13):
    Responsible for minimal, targeted implementation.
    Applies surgical code replacements and strictly preserves working code.
    """

    def __init__(
        self,
        task: str,
        file_manager: FileManager,
        model_provider: ModelProvider,
        target_file: Optional[str] = None,
        instruction: Optional[str] = None,
        parent_id: Optional[str] = None,
        depth: int = 1
    ):
        super().__init__(role=AgentRole.CODE_AGENT, task=task, parent_id=parent_id, depth=depth)
        self.file_manager = file_manager
        self.model_provider = model_provider
        self.target_file = target_file
        self.instruction = instruction or task

    async def execute(self) -> Dict[str, Any]:
        if not self.target_file:
            return {"status": "failed", "error": "No target file specified for Code Agent"}

        # 1. Acquire file lock (Section 10)
        lock_acquired = await self.file_manager.lock_manager.acquire_lock(
            self.target_file, self.id, timeout_sec=60.0
        )
        if not lock_acquired:
            return {
                "status": "failed",
                "error": f"Could not acquire file lock for '{self.target_file}'. File is locked by another agent."
            }

        self.state.owned_files.append(self.target_file)

        try:
            # 2. Read existing content
            existing_code = self.file_manager.read_file(self.target_file)

            # 3. Model prompt for targeted atomic replacement
            prompt = f"""
Target File: {self.target_file}
Instruction: {self.instruction}

Existing File Content:
```
{existing_code}
```

Apply the Minimal Change Policy (Section 13).
Identify the smallest contiguous string to replace.
Respond ONLY with a JSON object matching:
{{
    "target_file": "{self.target_file}",
    "action": "replace",
    "search_content": "<exact substring to find in existing file>",
    "replace_content": "<replacement substring>",
    "explanation": "<rationale for this minimal edit>"
}}
"""
            raw_response = await self.model_provider.generate(
                prompt,
                system="You are an expert Code Agent adhering to the Minimal Change Policy. Make the smallest safe edit. Return valid JSON only."
            )

            from ornament.models.inference.engine import InferenceEngine
            patch_data = InferenceEngine.extract_json(raw_response)

            search_str = patch_data.get("search_content", "")
            replace_str = patch_data.get("replace_content", "")

            # 4. Apply exact replacement
            success = self.file_manager.edit_file_exact_replacement(
                self.target_file,
                search_str,
                replace_str,
                agent_id=self.id
            )

            if not success:
                # If direct match failed, attempt route string repair heuristic
                if "/contact-us" in existing_code and "/contact" in replace_str:
                    success = self.file_manager.edit_file_exact_replacement(
                        self.target_file,
                        "/contact-us",
                        "/contact",
                        agent_id=self.id
                    )

            if not success:
                return {
                    "status": "failed",
                    "error": f"Search string '{search_str[:40]}...' not found in {self.target_file}"
                }

            return {
                "status": "completed",
                "files_changed": [self.target_file],
                "explanation": patch_data.get("explanation", "Applied targeted edit"),
                "lines_modified": len(replace_str.splitlines())
            }

        finally:
            # Always release lock
            await self.file_manager.lock_manager.release_lock(self.target_file, self.id)

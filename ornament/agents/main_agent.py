import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from ornament.config import settings
from ornament.agents.base import BaseAgent, AgentRole
from ornament.agents.manager import AgentManager
from ornament.agents.debug_agent import DebugAgent
from ornament.agents.code_agent import CodeAgent
from ornament.agents.test_agent import TestAgent
from ornament.files.file_manager import FileManager
from ornament.git_ops.checkpoint import GitCheckpointManager
from ornament.memory.project_memory import ProjectMemory, ProjectState
from ornament.memory.failure_memory import FailureMemory
from ornament.models.provider.base import ModelProvider

class MainAgent(BaseAgent):
    """
    Main Agent (Section 6):
    The Project Manager and Executive Orchestrator.
    Decomposes requirements, manages agent delegation, enforces minimal change,
    and runs the autonomous repair loop.
    """

    def __init__(
        self,
        task: str,
        workspace_path: Path,
        model_provider: ModelProvider,
        agent_manager: Optional[AgentManager] = None
    ):
        super().__init__(role=AgentRole.MAIN_AGENT, task=task, parent_id=None, depth=0)
        self.workspace_path = workspace_path
        self.model_provider = model_provider
        self.agent_manager = agent_manager or AgentManager()
        self.file_manager = FileManager(workspace_path)
        self.git_checkpoint = GitCheckpointManager(workspace_path)

        # Persistent memories (Section 18, 19)
        db_file = workspace_path.parent / ".ornament" / "project_state.db"
        self.project_memory = ProjectMemory(db_file)
        self.failure_memory = FailureMemory(db_file)

    async def execute(self) -> Dict[str, Any]:
        """
        Executes plan synthesis, delegation, and repair loop (Section 17).
        """
        self.agent_manager.register_agent(self)
        self.mark_running()

        # Step 1: Create initial Git checkpoint
        chk_id = self.git_checkpoint.create_checkpoint("Initial state before task execution", agent_id=self.id)

        # Step 2: Understand architecture and synthesize plan
        plan_prompt = f"""
Requirements: {self.state.task}
Workspace files: {self.file_manager.list_files()}

Break down this engineering task into subtasks according to Minimal Change Policy.
Return JSON with architecture overview and task sequence.
"""
        plan_raw = await self.model_provider.generate(
            plan_prompt,
            system="You are the Main Agent / Project Architect. Synthesize a clean implementation plan."
        )

        return {
            "task_id": self.id,
            "status": "planned",
            "checkpoint": chk_id,
            "plan": plan_raw
        }

    async def run_repair_loop(
        self,
        symptom: str,
        base_url: Optional[str] = None,
        test_selector: Optional[str] = None,
        expected_route: Optional[str] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Closed Autonomous Repair Loop (PRD Section 14, 17):
        DETECT -> DIAGNOSE -> PLAN FIX -> MODIFY -> BUILD -> TEST -> PASS / FAIL Loop.
        """
        attempt = 1
        last_error = symptom
        history = []

        while attempt <= max_retries:
            # 1. Snapshot state before fix attempt
            cp = self.git_checkpoint.create_checkpoint(f"Pre-repair attempt {attempt} for: {symptom}", agent_id=self.id)

            # 2. Spawning Debug Agent
            debug_agent = DebugAgent(
                task=f"Diagnose issue: {last_error}",
                file_manager=self.file_manager,
                model_provider=self.model_provider,
                error_context={"symptom": symptom, "attempt": attempt, "last_error": last_error},
                parent_id=self.id,
                depth=self.state.depth + 1
            )
            diagnosis = await self.agent_manager.run_agent(debug_agent)

            affected_files = diagnosis.get("affected_files", [])
            recommended_fix = diagnosis.get("recommended_fix", "")
            target_file = affected_files[0] if affected_files else "components/Navbar.tsx"

            # 3. Spawning Code Agent for minimal surgical modification
            code_agent = CodeAgent(
                task=f"Apply minimal fix for {symptom}",
                file_manager=self.file_manager,
                model_provider=self.model_provider,
                target_file=target_file,
                instruction=f"Apply recommended fix: {recommended_fix}",
                parent_id=self.id,
                depth=self.state.depth + 1
            )
            code_result = await self.agent_manager.run_agent(code_agent)

            # 4. Spawning Test Agent to independently verify
            test_agent = TestAgent(
                task=f"Verify fix for {symptom}",
                workspace_path=self.workspace_path,
                base_url=base_url,
                target_route="/",
                click_selector=test_selector,
                expected_route=expected_route,
                parent_id=self.id,
                depth=self.state.depth + 1
            )
            test_result = await self.agent_manager.run_agent(test_agent)

            is_pass = test_result.get("passed", False)
            record = {
                "attempt": attempt,
                "diagnosis": diagnosis.get("root_cause", ""),
                "affected_files": affected_files,
                "code_result": code_result,
                "test_result": test_result,
                "status": "PASS" if is_pass else "FAIL"
            }
            history.append(record)

            if is_pass:
                # Issue successfully resolved! Commit changes and update project memory.
                commit_hash = self.git_checkpoint.commit(
                    f"Resolved issue: {symptom} (Minimal change in {target_file})",
                    agent_id=self.id
                )
                self.failure_memory.record_attempt(
                    task=symptom,
                    attempt=attempt,
                    error=symptom,
                    diagnosis=diagnosis.get("root_cause", ""),
                    fix=recommended_fix,
                    result="pass",
                    affected_files=affected_files
                )
                self.project_memory.log_agent_action(
                    agent_id=self.id,
                    role="main_agent",
                    task=f"Fix: {symptom}",
                    status="completed",
                    output=f"Resolved in attempt {attempt}. Commit {commit_hash[:8]}"
                )

                return {
                    "status": "resolved",
                    "attempts": attempt,
                    "final_status": "PASS",
                    "commit": commit_hash,
                    "history": history
                }
            else:
                # Failed attempt: record trajectory and rollback to clean checkpoint
                self.failure_memory.record_attempt(
                    task=symptom,
                    attempt=attempt,
                    error=str(test_result.get("failures", "Test failed")),
                    diagnosis=diagnosis.get("root_cause", ""),
                    fix=recommended_fix,
                    result="fail",
                    affected_files=affected_files
                )
                self.git_checkpoint.rollback(cp)
                last_error = f"Previous fix failed: {test_result.get('failures')}"
                attempt += 1

        return {
            "status": "exhausted_retries",
            "attempts": attempt - 1,
            "final_status": "FAIL",
            "history": history
        }

from pathlib import Path
from typing import Dict, Any, List, Optional
from ornament.agents.base import BaseAgent, AgentRole
from ornament.testing.runner import MultiLevelTestHarness, TestLevel, TestResult

class TestAgent(BaseAgent):
    """
    Test Agent (Section 15, 16):
    Executes multi-level verification (Static, Build, Runtime, Browser, A11y).
    Provides evidence-based test results. Code Agent cannot declare its own work successful.
    """

    def __init__(
        self,
        task: str,
        workspace_path: Path,
        base_url: Optional[str] = None,
        target_route: str = "/",
        click_selector: Optional[str] = None,
        expected_route: Optional[str] = None,
        parent_id: Optional[str] = None,
        depth: int = 1
    ):
        super().__init__(role=AgentRole.TEST_AGENT, task=task, parent_id=parent_id, depth=depth)
        self.workspace_path = workspace_path
        self.base_url = base_url
        self.target_route = target_route
        self.click_selector = click_selector
        self.expected_route = expected_route

    async def execute(self) -> Dict[str, Any]:
        results: Dict[str, Any] = {
            "status": "completed",
            "passed": True,
            "levels_run": [],
            "failures": []
        }

        # Level 1: Static checks
        lvl1 = await MultiLevelTestHarness.run_level1_static(self.workspace_path)
        results["levels_run"].append(lvl1.model_dump())
        if not lvl1.passed:
            results["passed"] = False
            results["failures"].append({"level": "level_1_static", "errors": lvl1.errors})

        # Level 2: Build verification
        lvl2 = await MultiLevelTestHarness.run_level2_build(self.workspace_path)
        results["levels_run"].append(lvl2.model_dump())
        if not lvl2.passed:
            results["passed"] = False
            results["failures"].append({"level": "level_2_build", "errors": lvl2.errors})

        # Level 4: Browser functional test (if dev server / base_url is available)
        if self.base_url:
            lvl4 = await MultiLevelTestHarness.run_level4_browser_functional(
                base_url=self.base_url,
                target_route=self.target_route,
                click_selector=self.click_selector,
                expected_route=self.expected_route
            )
            results["levels_run"].append(lvl4.model_dump())
            if not lvl4.passed:
                results["passed"] = False
                results["failures"].append({"level": "level_4_browser", "errors": lvl4.errors})

        # Level 7: Accessibility audit
        lvl7 = await MultiLevelTestHarness.run_level7_accessibility(self.workspace_path)
        results["levels_run"].append(lvl7.model_dump())
        if not lvl7.passed:
            results["passed"] = False
            results["failures"].append({"level": "level_7_accessibility", "errors": lvl7.errors})

        return results

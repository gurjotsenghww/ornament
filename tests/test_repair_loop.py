import pytest
import shutil
import asyncio
from pathlib import Path

from ornament.generator.portfolio_generator import PortfolioGenerator
from ornament.sandbox.dev_server import DevPreviewServer
from ornament.testing.runner import MultiLevelTestHarness
from ornament.agents.main_agent import MainAgent
from ornament.agents.manager import AgentManager
from ornament.models.provider.factory import get_model_provider

@pytest.fixture
def demo_workspace(tmp_path):
    ws = tmp_path / "portfolio_demo"
    ws.mkdir()
    yield ws
    shutil.rmtree(ws, ignore_errors=True)

@pytest.mark.asyncio
async def test_end_to_end_autonomous_repair_loop(demo_workspace):
    """
    Demonstration per Section 58, 59:
    1. Generate portfolio with intentional route bug (/contact-us)
    2. Multi-level test fails with 404
    3. Main Agent -> Debug Agent -> Code Agent -> Test Agent -> PASS
    4. Minimal Change Policy verified
    """
    # 1. Scaffolding with controlled route bug
    PortfolioGenerator.generate(demo_workspace, intentional_bug=True)
    navbar_initial = (demo_workspace / "components" / "Navbar.tsx").read_text(encoding="utf-8")
    assert 'href="/contact-us"' in navbar_initial

    # 2. Launch DevPreviewServer for Playwright
    server = DevPreviewServer(demo_workspace, port=3457)
    server.start()

    try:
        # 3. Independent test verification fails on route bug
        pre_test = await MultiLevelTestHarness.run_level4_browser_functional(
            base_url=server.url,
            target_route="/",
            click_selector="#nav-contact-button",
            expected_route="/contact"
        )
        assert pre_test.passed is False
        assert any("404" in err or "mismatch" in err.lower() for err in pre_test.errors)

        # 4. Trigger Main Agent closed repair loop
        model_prov = get_model_provider("deterministic")
        main_agent = MainAgent(
            task="Contact button gives 404 because href is /contact-us instead of /contact",
            workspace_path=demo_workspace,
            model_provider=model_prov
        )

        repair_result = await main_agent.run_repair_loop(
            symptom="Contact button points to /contact-us which produces 404",
            base_url=server.url,
            test_selector="#nav-contact-button",
            expected_route="/contact"
        )

        # 5. Verify Repair Success
        assert repair_result["final_status"] == "PASS"
        assert repair_result["status"] == "resolved"
        assert repair_result["attempts"] == 1
        assert "commit" in repair_result

        # 6. Verify Minimal Change Policy: Only Navbar.tsx modified, rest of files untouched!
        navbar_repaired = (demo_workspace / "components" / "Navbar.tsx").read_text(encoding="utf-8")
        assert 'href="/contact"' in navbar_repaired
        assert 'href="/contact-us"' not in navbar_repaired

        # 7. Post-repair independent Playwright browser test
        post_test = await MultiLevelTestHarness.run_level4_browser_functional(
            base_url=server.url,
            target_route="/",
            click_selector="#nav-contact-button",
            expected_route="/contact"
        )
        assert post_test.passed is True
        print("\n[SUCCESS] Playwright Browser Test confirmed /contact navigation successfully!")

    finally:
        server.stop()

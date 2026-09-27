import pytest
import shutil
from pathlib import Path
from ornament.generator import PortfolioGenerator, EcommerceGenerator, SaasGenerator
from ornament.generator.custom_site_generator import CustomSiteGenerator
from ornament.testing.runner import MultiLevelTestHarness

@pytest.fixture
def site_workspaces(tmp_path):
    ws_port = tmp_path / "ws_portfolio"
    ws_ecom = tmp_path / "ws_ecom"
    ws_saas = tmp_path / "ws_saas"
    ws_custom = tmp_path / "ws_custom"
    ws_port.mkdir()
    ws_ecom.mkdir()
    ws_saas.mkdir()
    ws_custom.mkdir()
    yield ws_port, ws_ecom, ws_saas, ws_custom
    shutil.rmtree(tmp_path, ignore_errors=True)

@pytest.mark.asyncio
async def test_portfolio_generator_validation(site_workspaces):
    ws_port, _, _, _ = site_workspaces
    res = PortfolioGenerator.generate(ws_port)
    assert res["status"] == "generated"
    assert len(res["files_created"]) >= 10

    lvl1 = await MultiLevelTestHarness.run_level1_static(ws_port)
    assert lvl1.passed is True
    lvl2 = await MultiLevelTestHarness.run_level2_build(ws_port)
    assert lvl2.passed is True

@pytest.mark.asyncio
async def test_ecommerce_generator_validation(site_workspaces):
    _, ws_ecom, _, _ = site_workspaces
    res = EcommerceGenerator.generate(ws_ecom)
    assert res["status"] == "generated"
    assert res["files_count"] >= 8

    lvl1 = await MultiLevelTestHarness.run_level1_static(ws_ecom)
    assert lvl1.passed is True
    lvl2 = await MultiLevelTestHarness.run_level2_build(ws_ecom)
    assert lvl2.passed is True

@pytest.mark.asyncio
async def test_saas_generator_validation(site_workspaces):
    _, _, ws_saas, _ = site_workspaces
    res = SaasGenerator.generate(ws_saas)
    assert res["status"] == "generated"
    assert res["files_count"] >= 8

    lvl1 = await MultiLevelTestHarness.run_level1_static(ws_saas)
    assert lvl1.passed is True
    lvl2 = await MultiLevelTestHarness.run_level2_build(ws_saas)
    assert lvl2.passed is True

@pytest.mark.asyncio
async def test_custom_site_generator_validation(site_workspaces):
    _, _, _, ws_custom = site_workspaces
    res = CustomSiteGenerator.generate(
        workspace_path=ws_custom,
        prompt="Autonomous AI Edge Platform with dark bento grid and fleet metrics",
        site_type="saas",
        style="dark_futuristic",
        palette_key="cyan",
        sections=["hero", "features", "stats", "pricing", "contact"]
    )
    assert res["status"] == "generated"
    assert res["files_count"] >= 4
    assert (ws_custom / "public" / "preview.html").exists()

    lvl1 = await MultiLevelTestHarness.run_level1_static(ws_custom)
    assert lvl1.passed is True
    lvl2 = await MultiLevelTestHarness.run_level2_build(ws_custom)
    assert lvl2.passed is True


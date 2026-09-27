import pytest
import shutil
from pathlib import Path
from ornament.generator import PortfolioGenerator, EcommerceGenerator, SaasGenerator
from ornament.testing.runner import MultiLevelTestHarness

@pytest.fixture
def site_workspaces(tmp_path):
    ws_port = tmp_path / "ws_portfolio"
    ws_ecom = tmp_path / "ws_ecom"
    ws_saas = tmp_path / "ws_saas"
    ws_port.mkdir()
    ws_ecom.mkdir()
    ws_saas.mkdir()
    yield ws_port, ws_ecom, ws_saas
    shutil.rmtree(tmp_path, ignore_errors=True)

@pytest.mark.asyncio
async def test_portfolio_generator_validation(site_workspaces):
    ws_port, _, _ = site_workspaces
    res = PortfolioGenerator.generate(ws_port)
    assert res["status"] == "generated"
    assert len(res["files_created"]) >= 10

    lvl1 = await MultiLevelTestHarness.run_level1_static(ws_port)
    assert lvl1.passed is True
    lvl2 = await MultiLevelTestHarness.run_level2_build(ws_port)
    assert lvl2.passed is True

@pytest.mark.asyncio
async def test_ecommerce_generator_validation(site_workspaces):
    _, ws_ecom, _ = site_workspaces
    res = EcommerceGenerator.generate(ws_ecom)
    assert res["status"] == "generated"
    assert res["files_count"] >= 8

    lvl1 = await MultiLevelTestHarness.run_level1_static(ws_ecom)
    assert lvl1.passed is True
    lvl2 = await MultiLevelTestHarness.run_level2_build(ws_ecom)
    assert lvl2.passed is True

@pytest.mark.asyncio
async def test_saas_generator_validation(site_workspaces):
    _, _, ws_saas = site_workspaces
    res = SaasGenerator.generate(ws_saas)
    assert res["status"] == "generated"
    assert res["files_count"] >= 8

    lvl1 = await MultiLevelTestHarness.run_level1_static(ws_saas)
    assert lvl1.passed is True
    lvl2 = await MultiLevelTestHarness.run_level2_build(ws_saas)
    assert lvl2.passed is True

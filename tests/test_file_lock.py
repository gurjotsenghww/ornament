import pytest
import shutil
from pathlib import Path
from ornament.files.file_manager import FileManager
from ornament.files.lock_manager import FileLockManager

@pytest.fixture
def temp_workspace(tmp_path):
    ws = tmp_path / "test_ws"
    ws.mkdir()
    yield ws
    shutil.rmtree(ws, ignore_errors=True)

@pytest.mark.asyncio
async def test_file_lock_manager():
    lock_mgr = FileLockManager()
    file_path = "components/Navbar.tsx"

    # Agent A acquires lock
    acquired = await lock_mgr.acquire_lock(file_path, agent_id="agent_a", timeout_sec=10.0)
    assert acquired is True
    assert lock_mgr.get_owner(file_path) == "agent_a"

    # Agent B fails to acquire lock
    b_acquired = await lock_mgr.acquire_lock(file_path, agent_id="agent_b", timeout_sec=10.0)
    assert b_acquired is False

    # Main Agent overrides lock (Section 10)
    override = await lock_mgr.force_override(file_path, requester_id="main_agent")
    assert override is True
    assert lock_mgr.get_owner(file_path) is None

    # Agent B can now acquire lock
    b_acquired_after = await lock_mgr.acquire_lock(file_path, agent_id="agent_b", timeout_sec=10.0)
    assert b_acquired_after is True
    await lock_mgr.release_lock(file_path, agent_id="agent_b")

def test_file_manager_duplicate_prevention(temp_workspace):
    fm = FileManager(temp_workspace)
    fm.create_file("components/Hero.tsx", "export default function Hero() {}", overwrite=True)

    # Attempting to create duplicate "HeroFinal.tsx" should raise ValueError under Minimal Change Policy
    with pytest.raises(ValueError) as excinfo:
        fm.create_file("components/HeroFinal.tsx", "export default function HeroFinal() {}")
    assert "Minimal Change Policy Violation" in str(excinfo.value)

def test_file_manager_surgical_edit(temp_workspace):
    fm = FileManager(temp_workspace)
    code = '<nav><a href="/contact-us">Contact</a></nav>'
    fm.create_file("components/Navbar.tsx", code, overwrite=True)

    # Minimal targeted replacement
    success = fm.edit_file_exact_replacement(
        "components/Navbar.tsx",
        target_content='href="/contact-us"',
        replacement_content='href="/contact"',
        agent_id="code_agent"
    )
    assert success is True
    updated = fm.read_file("components/Navbar.tsx")
    assert 'href="/contact"' in updated
    assert 'href="/contact-us"' not in updated

import pytest
import shutil
from pathlib import Path
from ornament.git_ops.checkpoint import GitCheckpointManager

@pytest.fixture
def temp_repo(tmp_path):
    repo_dir = tmp_path / "repo_ws"
    repo_dir.mkdir()
    yield repo_dir
    shutil.rmtree(repo_dir, ignore_errors=True)

def test_git_checkpoint_and_rollback(temp_repo):
    git_mgr = GitCheckpointManager(temp_repo)
    initial_commit = git_mgr.create_checkpoint("Initial state", agent_id="main_agent")
    assert initial_commit is not None

    # Modify file
    test_file = temp_repo / "Hero.tsx"
    test_file.write_text("export default function BrokenHero() {}", encoding="utf-8")
    diff = git_mgr.get_diff()
    assert "BrokenHero" in diff

    # Rollback to clean state
    rolled_back = git_mgr.rollback()
    assert rolled_back is True
    assert not test_file.exists()

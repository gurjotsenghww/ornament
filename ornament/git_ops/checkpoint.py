from pathlib import Path
from typing import Optional, List, Dict
import git

class GitCheckpointManager:
    """
    Manages Git checkpoints, diff inspection, and atomic rollbacks for generated projects (Section 31, 55).
    """

    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.repo = self._ensure_repo()

    def _ensure_repo(self) -> git.Repo:
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        git_dir = self.workspace_path / ".git"
        if not git_dir.exists():
            repo = git.Repo.init(self.workspace_path)
            # Create initial commit if empty
            initial_file = self.workspace_path / ".gitkeep"
            if not initial_file.exists():
                initial_file.touch()
            repo.index.add([".gitkeep"])
            repo.index.commit("Initial project repository bootstrap [Ornàment]")
            return repo
        return git.Repo(self.workspace_path)

    def create_checkpoint(self, description: str, agent_id: str = "main_agent") -> str:
        """Creates a snapshot before executing modifications."""
        try:
            self.repo.git.add(A=True)
            if self.repo.is_dirty(untracked_files=True):
                commit = self.repo.index.commit(f"CHECKPOINT [{agent_id}]: {description}")
                return commit.hexsha
            # Clean working directory, return head
            return self.repo.head.commit.hexsha
        except Exception as e:
            return f"checkpoint_err_{e}"

    def commit(self, message: str, agent_id: str = "code_agent") -> str:
        """Commits verified changes after test suite passes."""
        self.repo.git.add(A=True)
        if self.repo.is_dirty(untracked_files=True):
            commit = self.repo.index.commit(f"[{agent_id}] {message}")
            return commit.hexsha
        return self.repo.head.commit.hexsha

    def rollback(self, target_commit: Optional[str] = None) -> bool:
        """Restores repository to last known-good state if changes fail tests."""
        try:
            if target_commit:
                self.repo.git.reset("--hard", target_commit)
            else:
                self.repo.git.reset("--hard", "HEAD")
            self.repo.git.clean("-fd")
            return True
        except Exception:
            return False

    def get_diff(self) -> str:
        """Returns unified diff of uncommitted and untracked changes."""
        try:
            diff_staged = self.repo.git.diff("--staged")
            diff_unstaged = self.repo.git.diff()
            untracked = self.repo.untracked_files
            parts = []
            if diff_staged:
                parts.append(f"--- Staged ---\n{diff_staged}")
            if diff_unstaged:
                parts.append(f"--- Unstaged ---\n{diff_unstaged}")
            if untracked:
                untracked_blocks = []
                for u in untracked:
                    try:
                        u_path = self.workspace_path / u
                        content = u_path.read_text(encoding="utf-8", errors="ignore")
                        untracked_blocks.append(f"--- Untracked: {u} ---\n+++ {u}\n{content}")
                    except Exception:
                        untracked_blocks.append(f"--- Untracked: {u} ---")
                parts.append("\n".join(untracked_blocks))
            return "\n".join(parts) if parts else "No changes detected."
        except Exception as e:
            return f"Diff error: {e}"

    def get_history(self, limit: int = 10) -> List[Dict[str, str]]:
        commits = []
        try:
            for c in list(self.repo.iter_commits("HEAD", max_count=limit)):
                commits.append({
                    "hexsha": c.hexsha[:8],
                    "message": c.message.strip(),
                    "author": str(c.author),
                    "committed_date": str(c.committed_datetime)
                })
        except Exception:
            pass
        return commits

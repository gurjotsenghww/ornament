import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from ornament.files.lock_manager import FileLockManager
from ornament.files.dependency_graph import DependencyGraph

class FileManager:
    """
    Dedicated sandboxed File Manager for Ornàment (Section 12, 13, 42).
    Maintains file registry, duplicate prevention, and surgical edits.
    """

    def __init__(self, workspace_root: Path, lock_manager: Optional[FileLockManager] = None):
        self.workspace_root = workspace_root.resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        self.lock_manager = lock_manager or FileLockManager()
        self.dependency_graph = DependencyGraph(self.workspace_root)
        self.change_history: List[Dict[str, str]] = []

    def _resolve_and_verify(self, rel_path: str) -> Path:
        """Enforces sandbox boundary: prohibits path traversal outside workspace."""
        clean_rel = rel_path.lstrip("/\\")
        target = (self.workspace_root / clean_rel).resolve()
        try:
            target.relative_to(self.workspace_root)
        except ValueError:
            raise PermissionError(f"Access Denied: Path '{rel_path}' is outside designated workspace sandbox.")
        return target

    def _check_duplicate_intent(self, rel_path: str) -> Optional[str]:
        """
        Prevents redundant copy-paste clutter (HeroFinal.tsx, HeroNew.tsx).
        """
        filename = Path(rel_path).name
        # Match names like HeroNew, HeroFinal, Hero2, Hero_v2
        stem = Path(rel_path).stem
        ext = Path(rel_path).suffix
        pattern = r"^(.*?)(?:[Nn]ew|[Ff]inal|[Cc]opy|[Vv]ersion\d+|\d+|_v\d+)$"
        match = re.match(pattern, stem)
        if match:
            base_stem = match.group(1)
            candidate = Path(rel_path).parent / f"{base_stem}{ext}"
            if (self.workspace_root / candidate).exists():
                return candidate.as_posix()
        return None

    def create_directory(self, rel_dir: str) -> Path:
        target = self._resolve_and_verify(rel_dir)
        target.mkdir(parents=True, exist_ok=True)
        return target

    def create_file(self, rel_path: str, content: str, agent_id: str = "main_agent", overwrite: bool = False) -> Path:
        target = self._resolve_and_verify(rel_path)

        # Check duplicate naming anomaly
        existing_counterpart = self._check_duplicate_intent(rel_path)
        if existing_counterpart and not overwrite:
            raise ValueError(
                f"Minimal Change Policy Violation: File '{rel_path}' appears to be a redundant duplicate of existing file '{existing_counterpart}'. Modify the existing file instead of creating duplicate variations."
            )

        if target.exists() and not overwrite:
            raise FileExistsError(f"File '{rel_path}' already exists. Use targeted edit or explicit overwrite.")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        self.change_history.append({
            "agent_id": agent_id,
            "action": "create" if not target.exists() else "overwrite",
            "file": rel_path
        })
        self.dependency_graph.scan_project()
        return target

    def read_file(self, rel_path: str) -> str:
        target = self._resolve_and_verify(rel_path)
        if not target.exists():
            raise FileNotFoundError(f"File '{rel_path}' does not exist.")
        return target.read_text(encoding="utf-8")

    def edit_file_exact_replacement(
        self,
        rel_path: str,
        target_content: str,
        replacement_content: str,
        agent_id: str = "code_agent"
    ) -> bool:
        """
        Minimal Change Policy surgical edit (Section 13):
        Replaces specific targeted substring without re-synthesizing the whole file.
        """
        # Lock verification
        owner = self.lock_manager.get_owner(rel_path)
        if owner and owner != agent_id and agent_id != "main_agent":
            raise PermissionError(f"File '{rel_path}' is locked by active agent '{owner}'. Cannot modify.")

        target = self._resolve_and_verify(rel_path)
        if not target.exists():
            raise FileNotFoundError(f"Cannot edit non-existent file '{rel_path}'.")

        current = target.read_text(encoding="utf-8")
        if target_content not in current:
            # Normalize line endings and check again
            curr_norm = current.replace("\r\n", "\n")
            targ_norm = target_content.replace("\r\n", "\n")
            if targ_norm not in curr_norm:
                return False
            updated = curr_norm.replace(targ_norm, replacement_content.replace("\r\n", "\n"), 1)
        else:
            updated = current.replace(target_content, replacement_content, 1)

        target.write_text(updated, encoding="utf-8")
        self.change_history.append({
            "agent_id": agent_id,
            "action": "minimal_edit",
            "file": rel_path
        })
        self.dependency_graph.scan_project()
        return True

    def delete_file(self, rel_path: str, agent_id: str = "main_agent") -> bool:
        target = self._resolve_and_verify(rel_path)
        if target.exists() and target.is_file():
            target.unlink()
            self.change_history.append({
                "agent_id": agent_id,
                "action": "delete",
                "file": rel_path
            })
            self.dependency_graph.scan_project()
            return True
        return False

    def list_files(self, exclude_build: bool = True) -> List[str]:
        results = []
        for p in self.workspace_root.rglob("*"):
            if p.is_file():
                if exclude_build and any(x in p.parts for x in ["node_modules", ".next", ".git", ".turbo"]):
                    continue
                results.append(p.relative_to(self.workspace_root).as_posix())
        return sorted(results)

    def search_code(self, query: str) -> List[Dict[str, Any]]:
        """Searches for pattern/text across all source code in the project."""
        matches = []
        for rel_file in self.list_files(exclude_build=True):
            try:
                content = self.read_file(rel_file)
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if query in line:
                        matches.append({
                            "file": rel_file,
                            "line_number": i + 1,
                            "line_content": line.strip()
                        })
            except Exception:
                pass
        return matches

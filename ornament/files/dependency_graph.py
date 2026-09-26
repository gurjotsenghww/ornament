import re
from pathlib import Path
from typing import Dict, Set, List

class DependencyGraph:
    """
    Maintains component and import dependency graphs (Section 12).
    Enables impact analysis: if File A changes, what dependent components need verification?
    """

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.dependencies: Dict[str, Set[str]] = {}  # file -> {files it imports}
        self.dependents: Dict[str, Set[str]] = {}    # file -> {files that import it}

    def scan_project(self):
        self.dependencies.clear()
        self.dependents.clear()

        extensions = [".ts", ".tsx", ".js", ".jsx", ".css"]
        for ext in extensions:
            for file_path in self.workspace_root.rglob(f"*{ext}"):
                if "node_modules" in file_path.parts or ".next" in file_path.parts:
                    continue
                rel_path = file_path.relative_to(self.workspace_root).as_posix()
                self._parse_file_imports(rel_path, file_path)

    def _parse_file_imports(self, rel_path: str, file_path: Path):
        if rel_path not in self.dependencies:
            self.dependencies[rel_path] = set()

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return

        # Matches: import ... from "path" or require("path")
        matches = re.findall(r'(?:import|from|require\()\s*[\'"]([^\'"]+)[\'"]', content)
        for import_str in matches:
            if import_str.startswith(".") or import_str.startswith("@/"):
                resolved = self._resolve_import(rel_path, import_str)
                if resolved:
                    self.dependencies[rel_path].add(resolved)
                    if resolved not in self.dependents:
                        self.dependents[resolved] = set()
                    self.dependents[resolved].add(rel_path)

    def _resolve_import(self, source_rel: str, import_str: str) -> str:
        source_dir = (self.workspace_root / source_rel).parent

        if import_str.startswith("@/"):
            target_base = self.workspace_root / import_str[2:]
        else:
            target_base = (source_dir / import_str).resolve()

        # Try extensions
        candidates = [
            target_base,
            target_base.with_suffix(".tsx"),
            target_base.with_suffix(".ts"),
            target_base.with_suffix(".jsx"),
            target_base.with_suffix(".js"),
            target_base / "index.tsx",
            target_base / "index.ts"
        ]

        for cand in candidates:
            if cand.exists() and cand.is_file():
                try:
                    return cand.relative_to(self.workspace_root).as_posix()
                except ValueError:
                    pass
        return ""

    def get_affected_files(self, changed_file: str) -> List[str]:
        """Returns all files that directly or transitively depend on changed_file."""
        changed_rel = changed_file.replace("\\", "/")
        visited = set()
        queue = [changed_rel]

        while queue:
            curr = queue.pop(0)
            if curr in self.dependents:
                for dep in self.dependents[curr]:
                    if dep not in visited:
                        visited.add(dep)
                        queue.append(dep)
        return sorted(list(visited))

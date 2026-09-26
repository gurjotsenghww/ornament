import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class ProjectState(BaseModel):
    name: str
    framework: str = "Next.js 14 App Router"
    language: str = "TypeScript"
    styling: str = "Tailwind CSS"
    theme: str = "dark"
    routes: List[str] = ["/"]
    components: List[str] = []
    design_system: Dict[str, Any] = {}
    known_issues: List[str] = []

class ProjectMemory:
    """
    Persistent memory for project architecture, routes, components, and history (Section 19).
    Prevents costly re-discovery loops across agent iterations.
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS project_state (
                    id TEXT PRIMARY KEY,
                    state_json TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT,
                    role TEXT,
                    task TEXT,
                    status TEXT,
                    output TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_state(self, project_id: str, state: ProjectState):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO project_state (id, state_json) VALUES (?, ?)",
                (project_id, state.model_dump_json())
            )

    def load_state(self, project_id: str) -> Optional[ProjectState]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT state_json FROM project_state WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            if row:
                return ProjectState.model_validate_json(row[0])
        return None

    def log_agent_action(self, agent_id: str, role: str, task: str, status: str, output: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO agent_history (agent_id, role, task, status, output) VALUES (?, ?, ?, ?, ?)",
                (agent_id, role, task, status, output)
            )

    def get_agent_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM agent_history ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]

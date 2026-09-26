import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class FailureTrajectory(BaseModel):
    task: str
    attempt: int
    error: str
    diagnosis: str
    fix: str
    result: str  # "pass" or "fail"
    affected_files: List[str] = Field(default_factory=list)
    timestamp: Optional[str] = None

class FailureMemory:
    """
    FailureMemory records debugging trajectories (Section 18).
    Curates failure -> diagnosis -> fix sequences for subsequent LoRA fine-tuning.
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS failure_trajectories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    attempt INTEGER,
                    error TEXT,
                    diagnosis TEXT,
                    fix TEXT,
                    result TEXT,
                    affected_files TEXT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def record_attempt(
        self,
        task: str,
        attempt: int,
        error: str,
        diagnosis: str,
        fix: str,
        result: str,
        affected_files: Optional[List[str]] = None
    ):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO failure_trajectories 
                (task, attempt, error, diagnosis, fix, result, affected_files)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (task, attempt, error, diagnosis, fix, result, json.dumps(affected_files or []))
            )

    def export_training_trajectories(self, output_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM failure_trajectories ORDER BY id ASC")
            rows = cursor.fetchall()

        trajectories = []
        for r in rows:
            trajectories.append({
                "task": r["task"],
                "attempt": r["attempt"],
                "error": r["error"],
                "diagnosis": r["diagnosis"],
                "fix": r["fix"],
                "result": r["result"],
                "affected_files": json.loads(r["affected_files"]) if r["affected_files"] else []
            })

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(trajectories, f, indent=2)

        return trajectories

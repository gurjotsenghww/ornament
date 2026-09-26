import uuid
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class AgentStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentRole(str, Enum):
    MAIN_AGENT = "main_agent"
    CODE_AGENT = "code_agent"
    DEBUG_AGENT = "debug_agent"
    TEST_AGENT = "test_agent"
    DESIGN_AGENT = "design_agent"
    SEO_AGENT = "seo_agent"

class AgentState(BaseModel):
    id: str = Field(default_factory=lambda: f"agent_{uuid.uuid4().hex[:8]}")
    role: AgentRole
    task: str
    parent_id: Optional[str] = None
    status: AgentStatus = AgentStatus.QUEUED
    depth: int = 0
    owned_files: List[str] = Field(default_factory=list)
    output: Optional[Dict[str, Any]] = None
    error_state: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    finished_at: Optional[float] = None

class BaseAgent(ABC):
    """
    Base class for all agents in the Ornàment hierarchy (Section 8, 9).
    """

    def __init__(
        self,
        role: AgentRole,
        task: str,
        parent_id: Optional[str] = None,
        depth: int = 0,
        agent_id: Optional[str] = None
    ):
        self.state = AgentState(
            id=agent_id or f"{role.value}_{uuid.uuid4().hex[:6]}",
            role=role,
            task=task,
            parent_id=parent_id,
            depth=depth,
            status=AgentStatus.QUEUED
        )

    @property
    def id(self) -> str:
        return self.state.id

    @property
    def role(self) -> AgentRole:
        return self.state.role

    @property
    def status(self) -> AgentStatus:
        return self.state.status

    def mark_running(self):
        self.state.status = AgentStatus.RUNNING

    def mark_completed(self, output: Dict[str, Any]):
        self.state.status = AgentStatus.COMPLETED
        self.state.output = output
        self.state.finished_at = time.time()

    def mark_failed(self, error: str):
        self.state.status = AgentStatus.FAILED
        self.state.error_state = error
        self.state.finished_at = time.time()

    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """Execute agent task and return structured output."""
        pass

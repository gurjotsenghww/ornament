# Ornàment Agent System Specification

## Agent Hierarchy & Roles
Ornàment implements a structured, nested hierarchy governed by the `AgentManager`.

```text
Main Agent (Architect & Planner)
  ├── Debug Agent (Root-cause diagnostician)
  ├── Code Agent (Minimal change surgical applicator)
  └── Test Agent (Multi-level verification & Playwright automation)
```

## Agent Lifecycles & States
Every agent transitions through strict states:
```text
queued ──> running ──┬──> completed
                     ├──> failed
                     └──> cancelled
```

### Agent State Schema
```python
class AgentState(BaseModel):
    id: str               # Unique agent ID
    role: AgentRole       # main_agent | code_agent | debug_agent | test_agent
    task: str             # Actionable objective
    parent_id: Optional[str] # Parent orchestrator ID
    status: AgentStatus   # Current state
    depth: int            # Recursion depth (max 3)
    owned_files: List[str]# Files locked for modification
    output: Optional[Dict]# Structured result
    error_state: Optional[str]
```

## File Ownership & Locks
- Agents must never write to the same file concurrently.
- `FileLockManager` grants temporary atomic leases.
- The `MainAgent` can force-override locks if an agent becomes unresponsive.

## Safety & Concurrency Limits
- **Max Depth**: 3 levels.
- **Max Concurrent Subagents**: 2 (resource-gated by `HardwareManager`).
- **Throttling Triggers**: Spawning blocked if free RAM < 2048 MB, free VRAM < 1024 MB, or CPU > 95%.
- **Prohibited Commands**: Destructive operations (`rm -rf /`, `format`, `del /f /s /q c:\`, etc.) are blocked.

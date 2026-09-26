import asyncio
from typing import Dict, List, Optional
from ornament.config import settings
from ornament.hardware.monitor import HardwareManager
from ornament.agents.base import BaseAgent, AgentStatus

class AgentManager:
    """
    AgentManager governs the dynamic sub-agent lifecycle and enforces hardware concurrency limits (Section 7, 9, 50, 52).
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.active_agents: Dict[str, BaseAgent] = {}
        self.execution_log: List[Dict[str, str]] = []

    def register_agent(self, agent: BaseAgent) -> bool:
        if agent.state.depth > settings.max_agent_depth:
            agent.mark_failed(f"Max agent depth exceeded ({agent.state.depth} > {settings.max_agent_depth})")
            return False

        self.agents[agent.id] = agent
        self.execution_log.append({
            "event": "agent_registered",
            "agent_id": agent.id,
            "role": agent.role.value,
            "task": agent.state.task
        })
        return True

    async def run_agent(self, agent: BaseAgent) -> Dict:
        if not self.register_agent(agent):
            return {"status": "failed", "error": agent.state.error_state}

        # Check hardware capacity & concurrency
        can_spawn, reason = HardwareManager.can_spawn_agent(len(self.active_agents))
        if not can_spawn:
            # Wait or throttle
            retries = 0
            while not can_spawn and retries < 10:
                await asyncio.sleep(1.0)
                can_spawn, reason = HardwareManager.can_spawn_agent(len(self.active_agents))
                retries += 1

            if not can_spawn:
                agent.mark_failed(f"Agent launch throttled: {reason}")
                return {"status": "failed", "error": reason}

        # Mark running
        self.active_agents[agent.id] = agent
        agent.mark_running()
        self.execution_log.append({
            "event": "agent_started",
            "agent_id": agent.id,
            "role": agent.role.value
        })

        try:
            result = await agent.execute()
            agent.mark_completed(result)
            self.execution_log.append({
                "event": "agent_completed",
                "agent_id": agent.id,
                "role": agent.role.value
            })
            return result
        except Exception as e:
            agent.mark_failed(str(e))
            self.execution_log.append({
                "event": "agent_failed",
                "agent_id": agent.id,
                "role": agent.role.value,
                "error": str(e)
            })
            return {"status": "failed", "error": str(e)}
        finally:
            if agent.id in self.active_agents:
                del self.active_agents[agent.id]

    def get_agent_tree(self) -> List[Dict]:
        """Returns visual hierarchy of all registered agents (Section 44)."""
        tree = []
        for agent in self.agents.values():
            tree.append({
                "id": agent.id,
                "role": agent.role.value,
                "parent_id": agent.state.parent_id,
                "status": agent.status.value,
                "task": agent.state.task,
                "depth": agent.state.depth,
                "owned_files": agent.state.owned_files,
                "error": agent.state.error_state
            })
        return tree

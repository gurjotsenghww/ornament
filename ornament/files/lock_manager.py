import asyncio
import time
from typing import Dict, Optional

class FileLockManager:
    """
    FileLockManager enforces strict file ownership and prevents concurrent conflicting edits (Section 10).
    Allows Main Agent to override locks when necessary.
    """

    def __init__(self):
        # file_path -> (owner_agent_id, lock_acquired_time, timeout_seconds)
        self._locks: Dict[str, tuple[str, float, float]] = {}
        self._async_locks: Dict[str, asyncio.Lock] = {}

    def _get_async_lock(self, file_path: str) -> asyncio.Lock:
        normalized = file_path.replace("\\", "/").lower()
        if normalized not in self._async_locks:
            self._async_locks[normalized] = asyncio.Lock()
        return self._async_locks[normalized]

    async def acquire_lock(self, file_path: str, agent_id: str, timeout_sec: float = 30.0) -> bool:
        normalized = file_path.replace("\\", "/").lower()
        async_lock = self._get_async_lock(normalized)

        async with async_lock:
            current_time = time.time()
            if normalized in self._locks:
                owner, acquired_at, lease = self._locks[normalized]
                # Check for lease expiration
                if current_time - acquired_at < lease:
                    if owner == agent_id:
                        # Re-entrant lock by same agent
                        self._locks[normalized] = (agent_id, current_time, lease)
                        return True
                    return False

            # Lock acquired
            self._locks[normalized] = (agent_id, current_time, timeout_sec)
            return True

    async def release_lock(self, file_path: str, agent_id: str) -> bool:
        normalized = file_path.replace("\\", "/").lower()
        async_lock = self._get_async_lock(normalized)

        async with async_lock:
            if normalized in self._locks:
                owner, _, _ = self._locks[normalized]
                if owner == agent_id or agent_id == "main_agent":
                    del self._locks[normalized]
                    return True
                return False
            return True

    async def force_override(self, file_path: str, requester_id: str = "main_agent") -> bool:
        """Main Agent override (Section 10)"""
        normalized = file_path.replace("\\", "/").lower()
        async_lock = self._get_async_lock(normalized)
        async with async_lock:
            if normalized in self._locks:
                del self._locks[normalized]
            return True

    def get_owner(self, file_path: str) -> Optional[str]:
        normalized = file_path.replace("\\", "/").lower()
        if normalized in self._locks:
            owner, acquired_at, lease = self._locks[normalized]
            if time.time() - acquired_at < lease:
                return owner
            del self._locks[normalized]
        return None

    def get_all_locks(self) -> Dict[str, str]:
        current_time = time.time()
        active = {}
        for path, (owner, acquired_at, lease) in list(self._locks.items()):
            if current_time - acquired_at < lease:
                active[path] = owner
            else:
                del self._locks[path]
        return active

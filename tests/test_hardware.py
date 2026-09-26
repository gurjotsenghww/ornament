import pytest
from ornament.hardware.monitor import HardwareManager

def test_hardware_telemetry():
    telemetry = HardwareManager.get_system_telemetry()
    assert telemetry.cpu_percent >= 0.0
    assert telemetry.cpu_count > 0
    assert telemetry.ram_total_mb > 1000
    assert telemetry.ram_available_mb > 0
    print(f"\n[Hardware] CPU: {telemetry.cpu_percent}%, RAM Free: {telemetry.ram_available_mb}MB, GPU: {telemetry.gpu_name}")

def test_agent_spawning_throttle():
    # Test concurrency threshold
    can_spawn, reason = HardwareManager.can_spawn_agent(current_active_agents=99)
    assert not can_spawn
    assert "Maximum concurrent agents" in reason

    can_spawn_ok, _ = HardwareManager.can_spawn_agent(current_active_agents=0)
    assert isinstance(can_spawn_ok, bool)

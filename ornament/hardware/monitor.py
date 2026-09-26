import subprocess
import shutil
from typing import Dict, Any, Tuple
import psutil
from pydantic import BaseModel
from ornament.config import settings

class SystemTelemetry(BaseModel):
    cpu_percent: float
    cpu_count: int
    ram_total_mb: float
    ram_available_mb: float
    ram_used_percent: float
    gpu_available: bool
    gpu_name: str = "None"
    vram_total_mb: float = 0.0
    vram_free_mb: float = 0.0
    vram_used_mb: float = 0.0
    gpu_util_percent: float = 0.0
    gpu_temp_c: float = 0.0

class HardwareManager:
    """
    HardwareManager monitors real-time CPU, RAM, and GPU telemetry.
    Dynamically throttles model inference and sub-agent concurrency according to Section 2, 50.
    """

    @classmethod
    def get_system_telemetry(cls) -> SystemTelemetry:
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_count = psutil.cpu_count(logical=True) or 4
        ram = psutil.virtual_memory()

        telemetry = SystemTelemetry(
            cpu_percent=cpu_percent,
            cpu_count=cpu_count,
            ram_total_mb=round(ram.total / (1024 * 1024), 1),
            ram_available_mb=round(ram.available / (1024 * 1024), 1),
            ram_used_percent=ram.percent,
            gpu_available=False
        )

        # NVIDIA GPU telemetry via nvidia-smi
        if shutil.which("nvidia-smi"):
            try:
                cmd = [
                    "nvidia-smi",
                    "--query-gpu=name,memory.total,memory.free,memory.used,utilization.gpu,temperature.gpu",
                    "--format=csv,noheader,nounits"
                ]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                if res.returncode == 0 and res.stdout.strip():
                    parts = [p.strip() for p in res.stdout.strip().split(",")]
                    if len(parts) >= 6:
                        telemetry.gpu_available = True
                        telemetry.gpu_name = parts[0]
                        telemetry.vram_total_mb = float(parts[1])
                        telemetry.vram_free_mb = float(parts[2])
                        telemetry.vram_used_mb = float(parts[3])
                        telemetry.gpu_util_percent = float(parts[4])
                        telemetry.gpu_temp_c = float(parts[5])
            except Exception:
                pass

        return telemetry

    @classmethod
    def can_spawn_agent(cls, current_active_agents: int) -> Tuple[bool, str]:
        """
        Determines whether the system has sufficient resources to spawn another agent.
        """
        if current_active_agents >= settings.max_concurrent_agents:
            return False, f"Maximum concurrent agents limit reached ({settings.max_concurrent_agents})"

        telemetry = cls.get_system_telemetry()
        if telemetry.ram_available_mb < settings.min_free_ram_mb:
            return False, f"Insufficient free RAM ({telemetry.ram_available_mb:.0f} MB < {settings.min_free_ram_mb} MB threshold)"

        if telemetry.gpu_available and telemetry.vram_free_mb < settings.min_free_vram_mb:
            return False, f"Insufficient free VRAM ({telemetry.vram_free_mb:.0f} MB < {settings.min_free_vram_mb} MB threshold)"

        if telemetry.cpu_percent > 95.0:
            return False, f"CPU utilization too high ({telemetry.cpu_percent:.1f}%)"

        return True, "Resources adequate for spawning agent"

    @classmethod
    def get_model_recommendations(cls) -> Dict[str, Any]:
        """
        Determines optimal model quantization and context length based on physical hardware.
        """
        telemetry = cls.get_system_telemetry()
        if telemetry.gpu_available:
            if telemetry.vram_total_mb <= 6144:
                return {
                    "quantization": "4-bit (INT4 / Q4_K_M / AWQ)",
                    "max_context_tokens": 4096,
                    "batch_size": 1,
                    "offload_cpu": True,
                    "recommendation": "RTX 3050 6GB: Strict 4-bit quantization with shared model server."
                }
            elif telemetry.vram_total_mb <= 12288:
                return {
                    "quantization": "8-bit (INT8)",
                    "max_context_tokens": 8192,
                    "batch_size": 2,
                    "offload_cpu": False,
                    "recommendation": "Mid-tier GPU: 8-bit quantization supported."
                }
        return {
            "quantization": "CPU Q4 / Ollama quantized",
            "max_context_tokens": 4096,
            "batch_size": 1,
            "offload_cpu": True,
            "recommendation": "CPU / Shared model mode active."
        }

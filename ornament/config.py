from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # General
    env: str = Field(default="development", alias="ORNAMENT_ENV")
    log_level: str = Field(default="INFO", alias="ORNAMENT_LOG_LEVEL")
    base_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent)

    # Model Configuration
    model_provider: str = Field(default="openai_compatible", alias="ORNAMENT_MODEL_PROVIDER")
    model_name: str = Field(default="Qwen/Qwen2.5-Coder-7B-Instruct", alias="ORNAMENT_MODEL_NAME")
    model_api_base: str = Field(default="http://localhost:11434/v1", alias="ORNAMENT_MODEL_API_BASE")
    model_api_key: str = Field(default="local-key-not-required", alias="ORNAMENT_MODEL_API_KEY")
    context_window: int = Field(default=8192, alias="ORNAMENT_CONTEXT_WINDOW")

    # Hardware & Safety Limits (Section 2, 9, 41)
    max_concurrent_agents: int = Field(default=2, alias="ORNAMENT_MAX_CONCURRENT_AGENTS")
    max_agent_depth: int = Field(default=3, alias="ORNAMENT_MAX_AGENT_DEPTH")
    max_task_retries: int = Field(default=3, alias="ORNAMENT_MAX_TASK_RETRIES")
    max_execution_time_sec: int = Field(default=600, alias="ORNAMENT_MAX_EXECUTION_TIME_SEC")
    default_command_timeout_sec: int = Field(default=120, alias="ORNAMENT_DEFAULT_COMMAND_TIMEOUT_SEC")
    min_free_ram_mb: int = Field(default=2048, alias="ORNAMENT_MIN_FREE_RAM_MB")
    min_free_vram_mb: int = Field(default=1024, alias="ORNAMENT_MIN_FREE_VRAM_MB")

    # Prohibited / Dangerous Commands (Section 41)
    prohibited_commands: List[str] = [
        "rm -rf /",
        "rmdir /s /q c:\\",
        "format",
        "del /f /s /q c:\\",
        "drop database",
        "mkfs",
        "shutdown"
    ]

    # Workspace & Storage (Section 11, 19, 42)
    workspace_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "workspace")
    database_url: str = Field(default="sqlite:///./.ornament/ornament.db", alias="ORNAMENT_DATABASE_URL")
    port: int = Field(default=5050, alias="ORNAMENT_PORT")

settings = Settings()

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ModelConfig(BaseModel):
    model_name: str = Field(default="Qwen/Qwen2.5-Coder-7B-Instruct")
    api_base: str = Field(default="http://localhost:11434/v1")
    api_key: Optional[str] = Field(default="not-needed")
    temperature: float = Field(default=0.2)
    max_tokens: int = Field(default=4096)
    context_window: int = Field(default=8192)
    stream: bool = Field(default=False)
    timeout_sec: float = Field(default=60.0)

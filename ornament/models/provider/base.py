from abc import ABC, abstractmethod
from typing import Optional, Type, AsyncIterator, Tuple, Dict, Any
from pydantic import BaseModel
from ornament.models.configuration.model_config import ModelConfig
from ornament.models.tokenizer.token_estimator import TokenEstimator

class ModelProvider(ABC):
    """
    Abstract ModelProvider interface (Section 4).
    All agents interact exclusively with this layer.
    """

    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config or ModelConfig()

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Generate plain text or code response."""
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
        system: Optional[str] = None
    ) -> BaseModel:
        """Generate guaranteed structured output conforming to a Pydantic schema."""
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream token responses."""
        pass

    def estimate_tokens(self, text: str) -> int:
        """Estimates token usage for context budgeting."""
        return TokenEstimator.estimate_tokens(text)

    @abstractmethod
    async def health_check(self) -> Tuple[bool, str]:
        """Check if model backend is alive and responding."""
        pass

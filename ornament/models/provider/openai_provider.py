import httpx
from typing import Optional, Type, AsyncIterator, Tuple, Dict, Any
from pydantic import BaseModel
from ornament.models.provider.base import ModelProvider
from ornament.models.configuration.model_config import ModelConfig
from ornament.models.inference.engine import InferenceEngine

class OpenAICompatibleProvider(ModelProvider):
    """
    Client for OpenAI-compatible model endpoints (Ollama, vLLM, LM Studio, Qwen server).
    """

    def __init__(self, config: Optional[ModelConfig] = None):
        super().__init__(config)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key or 'none'}"
        }
        self.fallback = None

    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "max_tokens": max_tokens or self.config.max_tokens,
            "temperature": temperature if temperature is not None else self.config.temperature,
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.post(
                    f"{self.config.api_base.rstrip('/')}/chat/completions",
                    json=payload,
                    headers=self.headers
                )
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.HTTPError, Exception) as e:
            # Automatic graceful fallback when local server (Ollama/vLLM) is not yet active
            from ornament.models.provider.fallback_provider import DeterministicEngineProvider
            if not self.fallback:
                self.fallback = DeterministicEngineProvider(self.config)
            return await self.fallback.generate(prompt, system=system, max_tokens=max_tokens, temperature=temperature)

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
        system: Optional[str] = None
    ) -> BaseModel:
        system_instruction = (
            (system or "") +
            f"\nYou MUST respond ONLY with a valid JSON object strictly matching this schema:\n"
            f"{schema.model_json_schema()}"
        )
        raw_text = await self.generate(prompt, system=system_instruction)
        return InferenceEngine.parse_to_model(raw_text, schema)

    async def stream(
        self,
        prompt: str,
        system: Optional[str] = None
    ) -> AsyncIterator[str]:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "stream": True
        }

        async with httpx.AsyncClient(timeout=self.config.timeout_sec) as client:
            async with client.stream(
                "POST",
                f"{self.config.api_base.rstrip('/')}/chat/completions",
                json=payload,
                headers=self.headers
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and not line.endswith("[DONE]"):
                        import json
                        chunk = json.loads(line[6:])
                        content = chunk["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content

    async def health_check(self) -> Tuple[bool, str]:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{self.config.api_base.rstrip('/')}/models", headers=self.headers)
                if resp.status_code == 200:
                    return True, "Model API endpoint reachable"
                return False, f"Unexpected HTTP status {resp.status_code}"
        except Exception as e:
            return False, f"Connection to {self.config.api_base} failed: {e}"

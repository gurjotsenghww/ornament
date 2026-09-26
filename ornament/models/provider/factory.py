from ornament.config import settings
from ornament.models.configuration.model_config import ModelConfig
from ornament.models.provider.base import ModelProvider
from ornament.models.provider.openai_provider import OpenAICompatibleProvider
from ornament.models.provider.fallback_provider import DeterministicEngineProvider

def get_model_provider(force_provider: str = None) -> ModelProvider:
    provider_type = force_provider or settings.model_provider

    config = ModelConfig(
        model_name=settings.model_name,
        api_base=settings.model_api_base,
        api_key=settings.model_api_key,
        context_window=settings.context_window
    )

    if provider_type in ["openai_compatible", "ollama", "qwen_local"]:
        return OpenAICompatibleProvider(config)
    elif provider_type in ["mock", "fallback", "deterministic"]:
        return DeterministicEngineProvider(config)
    else:
        # Default safe fallback
        return DeterministicEngineProvider(config)

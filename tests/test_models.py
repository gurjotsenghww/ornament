import pytest
from pydantic import BaseModel
from ornament.models.tokenizer.token_estimator import TokenEstimator
from ornament.models.qwen.formatter import QwenPromptFormatter
from ornament.models.provider.factory import get_model_provider

class SamplePlan(BaseModel):
    project_name: str
    routes: list[str]

@pytest.mark.asyncio
async def test_token_estimator():
    text = "const hero = () => { return <div className='p-4'>Hello World</div> };"
    tokens = TokenEstimator.estimate_tokens(text)
    assert tokens > 5
    assert tokens < 50

@pytest.mark.asyncio
async def test_qwen_formatter():
    messages = [
        {"role": "user", "content": "How do I fix a broken route in Next.js?"}
    ]
    formatted = QwenPromptFormatter.format_chat(messages, system_prompt="You are an AI engineer.")
    assert "<|im_start|>system" in formatted
    assert "<|im_start|>user" in formatted
    assert "<|im_start|>assistant" in formatted

@pytest.mark.asyncio
async def test_deterministic_model_provider():
    provider = get_model_provider("deterministic")
    healthy, msg = await provider.health_check()
    assert healthy

    res = await provider.generate("Investigate broken contact button route in navbar")
    assert "route" in res.lower()

    structured = await provider.generate_structured("Create portfolio plan", SamplePlan)
    assert isinstance(structured, SamplePlan)
    assert len(structured.routes) > 0

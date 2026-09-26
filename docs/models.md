# Ornàment Model Modularity & Serving Strategy

## Model Abstraction Architecture
All agents interact exclusively with the `ModelProvider` abstraction layer:

```text
ornament/models/
  ├── configuration/      # ModelConfig schemas (temperature, context window, API base)
  ├── tokenizer/          # TokenEstimator (BPE budgeting)
  ├── inference/          # InferenceEngine (JSON parsing, Markdown fence extraction)
  ├── qwen/               # ChatML template formatting (<|im_start|>...<|im_end|>)
  └── provider/           # OpenAICompatibleProvider, DeterministicEngineProvider
```

## Provider Interface
Every model provider implements:
- `generate(prompt, system, max_tokens, temperature)`: Plain text generation.
- `generate_structured(prompt, schema, system)`: Guaranteed schema adherence.
- `stream(prompt, system)`: Async token streaming.
- `estimate_tokens(text)`: Context length calculation.
- `health_check()`: Verifies endpoint connectivity.

## Hardware Optimization for RTX 3050 6GB Laptop GPU
1. **Quantization**: 4-bit (`Q4_K_M` or `AWQ`). Fits an 8B model inside ~4.5 GB of VRAM.
2. **Context Window**: 4096-8192 tokens max to prevent out-of-memory (OOM) exceptions.
3. **Shared Server**: Agents share a single local model server (Ollama or vLLM) instead of loading weights per agent process.
4. **Resilient Fallback**: If the local endpoint is unreachable, the system automatically falls back to `DeterministicEngineProvider` to preserve workflow continuity without crashing.

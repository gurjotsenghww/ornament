# Ornàment Setup & Installation Guide

## 1. Prerequisites
- **Operating System**: Windows 10/11 64-bit, Linux, or macOS.
- **Python**: Python 3.10.x (Recommended: Python 3.10.11 for ML & Windows PyTorch compatibility).
- **Node.js**: Node.js v18+ or v20+ with npm / pnpm.
- **Git**: Installed and available in PATH.
- **GPU (Optional but recommended)**: NVIDIA GPU with CUDA drivers (e.g., RTX 3050 Laptop GPU 6GB VRAM, RTX 40-series).

## 2. Environment Setup

### Create and Activate Virtual Environment
```powershell
# Using Python 3.10
python -m venv .venv

# Activate venv on Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### Install Python Dependencies
```powershell
pip install -r requirements.txt
pip install -e .
```

### Install Playwright Browser Binaries
Playwright headless Chromium is required for Level 4 browser functional testing:
```powershell
playwright install chromium
```

## 3. Environment Variables
Copy `.env.example` to `.env` and configure as appropriate:
```powershell
Copy-Item .env.example .env
```

Key variables:
- `ORNAMENT_MODEL_PROVIDER`: `openai_compatible` (for Ollama / vLLM / local Qwen server) or `deterministic` (for offline tests & benchmarks).
- `ORNAMENT_MODEL_NAME`: `Qwen/Qwen2.5-Coder-7B-Instruct` or `Qwen3-8B`.
- `ORNAMENT_MODEL_API_BASE`: `http://localhost:11434/v1`.
- `ORNAMENT_MAX_CONCURRENT_AGENTS`: `2` (tailored for 6GB VRAM machines).
- `ORNAMENT_PORT`: `5050`.

## 4. Model Setup (Qwen Ecosystem)
To run local Qwen with Ollama:
```bash
# Pull 4-bit quantized Qwen coder
ollama pull qwen2.5-coder:7b
```
Ensure Ollama is running at `http://localhost:11434`.

# Ornàment Troubleshooting Guide

## 1. Out of Memory (OOM) on 6GB VRAM
- **Symptom**: CUDA out of memory during inference.
- **Remedy**:
  - Run `ornament telemetry` to inspect active GPU processes.
  - Set `ORNAMENT_MODEL_PROVIDER=openai_compatible` using a 4-bit quantized GGUF/Ollama model (`qwen2.5-coder:7b` requires ~4.5 GB VRAM).
  - Reduce `ORNAMENT_CONTEXT_WINDOW` to 4096 in `.env`.
  - Close background GPU apps (Discord hardware acceleration, heavy browser tabs).

## 2. Playwright Browser Automation Errors
- **Symptom**: `Executable doesn't exist at C:\Users\...\AppData\Local\ms-playwright\...`
- **Remedy**:
  - Run `playwright install chromium` inside the active virtual environment.

## 3. Windows Terminal Unicode Characters
- **Symptom**: `UnicodeEncodeError: 'charmap' codec can't encode character ...`
- **Remedy**:
  - Ornàment CLI uses clean ASCII tags (`[OK]`, `[*]`, `[FAIL]`) to guarantee zero encoding errors on any Windows codepage.
  - You can also run `$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8` in PowerShell.

## 4. Port Conflict on Preview Server
- **Symptom**: `OSError: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 3456)`
- **Remedy**:
  - The preview server sets `allow_reuse_address = True`.
  - Alternatively, pass custom ports via the CLI or UI.

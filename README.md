# Ornàment: Autonomous AI Website Engineer

**Ornàment** is a local-first, autonomous AI software-engineering system specifically engineered for modern websites. Rather than blindly regenerating entire files, Ornàment executes the end-to-end engineering discipline:
$$\text{Understand} \to \text{Plan} \to \text{Delegate} \to \text{Implement} \to \text{Test} \to \text{Diagnose} \to \text{Fix} \to \text{Retest} \to \text{Maintain}$$

Tailored specifically to operate efficiently within consumer hardware constraints (e.g. NVIDIA RTX 3050 Laptop GPU 6GB VRAM, 16GB RAM, AMD Ryzen HS-series CPU), Ornàment enforces the **Minimal Change Policy**, dynamic subagent throttling, and automated verification through **Playwright**.

---

## Key Features

1. **Hardware-Aware Concurrency (`HardwareManager`)**:
   - Continuously telemetry-monitors CPU, RAM, and GPU/VRAM.
   - Throttles agent concurrency dynamically to prevent memory thrashing.
2. **Model Abstraction Layer (`ModelProvider`)**:
   - Centralized model server interface supporting Qwen models (Qwen2.5-Coder, Qwen3) via local Ollama, vLLM, LM Studio, or local API.
   - Resilient fallback engine for offline testing and fast verification.
3. **Specialized Agent Hierarchy**:
   - **Main Agent**: Architect, planner, and closed-loop repair orchestrator.
   - **Debug Agent**: Root-cause diagnostician inspecting symptoms, routes, and console logs.
   - **Code Agent**: Surgical patch applicator preserving working code.
   - **Test Agent**: Multi-level validator (Static, Build, Runtime, Playwright Functional, Responsiveness, Accessibility).
4. **File Ownership & Lock Safety (`FileLockManager`)**:
   - Granular path-based file locking prevents race conditions and overwrites.
5. **Git Checkpoints & Atomic Rollback**:
   - Snapshots every change; automatically rolls back unverified or failing modifications.
6. **Project & Failure Memory**:
   - SQLite-backed state storing component registries, routes, test logs, and failure-to-fix trajectories ready for LoRA fine-tuning.
7. **Local Knowledge Retrieval (RAG)**:
   - Zero-cloud TF-IDF / BM25 index of web engineering standards (Next.js App Router, Tailwind, WCAG A11y).
8. **Interactive Web Dashboard & CLI**:
   - Real-time agent tree, live preview iframe, minimal diff viewer, and test results.

---

## Quick Start

### 1. Install & Activate Environment
```powershell
# Using Python 3.10
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies and editable package
pip install -r requirements.txt
pip install -e .
playwright install chromium
```

### 2. Verify Hardware & System Telemetry
```powershell
ornament telemetry
```

### 3. Run Subsystem Test Suite
```powershell
pytest -v tests
```

### 4. Run the Autonomous Engineering Demonstration (Section 59)
```powershell
# 1. Generate Next.js Developer Portfolio with intentional route bug (/contact-us)
ornament generate --name demo-portfolio --bug

# 2. Run multi-level Playwright test harness (Level 4 fails with HTTP 404)
ornament test --name demo-portfolio

# 3. Launch Main Agent Autonomous Repair Loop (Debug Agent -> Code Agent -> Test Agent -> PASS)
ornament repair --name demo-portfolio

# 4. Confirm all test levels now pass with verified Playwright browser click
ornament test --name demo-portfolio
```

### 5. Launch the Web UI & API Server
```powershell
ornament serve --port 5050
```
Open [http://localhost:5050](http://localhost:5050) in your browser.

---

## Model Version Control Repository
Model training scripts, dataset manifests, and LoRA configs are stored in the isolated `ai-website-engineer-model/` repository:
- `train_lora.py`: Fine-tunes model on trajectory datasets.
- `evaluate_benchmark.py`: Evaluates against fixed benchmark test suites.
- `rollback_model.py`: Switches model versions.

---

## Documentation
- [Setup & Installation](docs/setup.md)
- [Architecture & Design](docs/architecture.md)
- [Agent Hierarchy](docs/agents.md)
- [Model System](docs/models.md)
- [Training & Datasets](docs/training_and_datasets.md)
- [Troubleshooting](docs/troubleshooting.md)

# Ornàment: Autonomous AI Website Engineer

**Ornàment** is a local-first, autonomous AI software-engineering system specifically engineered for modern websites. Rather than blindly regenerating entire files, Ornàment executes the end-to-end engineering discipline:
$$\text{Understand} \to \text{Plan} \to \text{Delegate} \to \text{Implement} \to \text{Test} \to \text{Diagnose} \to \text{Fix} \to \text{Retest} \to \text{Maintain}$$

Tailored specifically to operate efficiently within consumer hardware constraints (e.g. NVIDIA RTX 3050 Laptop GPU 6GB VRAM, 16GB RAM, AMD Ryzen HS-series CPU) and scalable to cloud accelerators (**Google Colab Tesla T4**, **NVIDIA A100/DGX**), Ornàment enforces the **Minimal Change Policy**, dynamic subagent throttling, and automated verification through **Playwright**.

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

## Local Development

### 1. Install & Activate Environment
```powershell
# Using Python 3.10
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install core dependencies and editable package
pip install -r requirements.txt
pip install -r requirements-train.txt
pip install -e .
playwright install chromium
```

### 2. Verify Hardware & System Telemetry
```powershell
# Check GPU VRAM and compute capability
python scripts/check_gpu.py

# Check Ornàment system telemetry
ornament telemetry
```

### 3. Run Subsystem Test Suite
```powershell
pytest -v tests
```

### 4. Run Model Training (Local RTX 3050 6GB)
```powershell
python ai-website-engineer-model/scripts/train_lora.py --config ai-website-engineer-model/configs/training_config.yaml
```

---

## Google Colab Training

Ornàment supports cloud training on **Google Colab** with NVIDIA Tesla T4 (~14.56 GB usable VRAM) and persistent storage on Google Drive.

A dedicated notebook is provided:
- `colab/train.ipynb` (also mirrored at `colab_training.ipynb`)

### Quick Colab Execution Steps:
1. Open [Google Colab](https://colab.research.google.com).
2. Upload `colab/train.ipynb` or open your private GitHub notebook.
3. Select **Runtime → Change runtime type → T4 GPU**.
4. Run **Step 1** to verify the T4 GPU (~14.56 GB VRAM).
5. Run **Step 2** to clone your private GitHub repository (using Colab Secrets).
6. Run **Step 3** to install project dependencies (`pip install -r requirements.txt -r requirements-train.txt`).
7. Run **Step 4** to mount Google Drive (`/content/drive/MyDrive/Ornàment`).
8. Run **Step 5–7** to sync datasets to `/content/` NVMe and run the GPU matrix computation test.
9. Run **Step 8** to execute the **50-Step Sanity Test**.
10. Run **Step 9** to launch **Full Production Training** (checkpoints save directly to Google Drive).

---

## GitHub Workflow (Local ↔ GitHub ↔ Colab)

```
Google Antigravity (Local PC)
         ↓  (1. Modify code / test)
     git commit
         ↓  (2. Push changes)
   GitHub Private Repo
         ↓  (3. Pull changes)
    Google Colab (Tesla T4)
         ↓  (4. Run training)
    Google Drive Persistent Storage
```

### 1. Linking Your Private GitHub Repository
Run locally in Antigravity:
```bash
# Add your private GitHub repository remote
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git

# Push current codebase
git branch -M master
git push -u origin master
```

### 2. Updating Code & Syncing to Cloud
```bash
# 1. Edit code locally in Antigravity
# 2. Stage and commit
git add .
git commit -m "feat: enhance training pipeline"

# 3. Push to GitHub
git push origin master

# 4. In Colab, pull latest updates:
!cd /content/Ornàment && git pull
```

---

## Dataset & Checkpoint Storage Architecture

Ornàment strictly enforces the **Separation of Code and Data**:

| Location | Contents | Stored In |
| :--- | :--- | :--- |
| **GitHub** | Source code, configs, CLI, tests, documentation | Git Version Control |
| **Local Cache** | Base model weights (`Qwen2.5-Coder-3B`), HuggingFace cache | `D:\Ornàment\.cache\` |
| **Persistent Cloud** | Datasets, LoRA checkpoints, trained adapters | Google Drive (`/content/drive/MyDrive/Ornàment/`) |
| **Colab Scratch** | Fast training workspace, active batch buffer | `/content/ornament_workspace/` |

> [!IMPORTANT]
> Large binary model files (`*.safetensors`, `*.pt`, `*.bin`, `*.gguf`) and datasets (`*.jsonl`) are **strictly excluded** from GitHub via `.gitignore`. Checkpoints are versioned in Google Drive and referenced via metadata manifests.

---

## Resume Training

If your Google Colab session disconnects or reaches the idle timeout, your training progress is **never lost**. Checkpoints are automatically saved every 20 steps to Google Drive:

### Resuming on Colab:
In `colab/train.ipynb`, run the **RESUME TRAINING** cell or execute:
```bash
python ai-website-engineer-model/scripts/train_lora.py \
    --config ai-website-engineer-model/configs/training_config.yaml \
    --resume latest
```
The trainer automatically detects the latest checkpoint (e.g. `checkpoint-40`, `checkpoint-60`) in `/content/drive/MyDrive/Ornàment/checkpoints/v0.1.0/` and continues without restarting!

### Resuming Locally:
```powershell
python ai-website-engineer-model/scripts/train_lora.py --resume latest
```

---

## GPU Requirements & Hardware Profiles

| Hardware Profile | Usable VRAM | Recommended Precision | Batch Size | Accumulation | Context Length |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Local RTX 3050 Laptop** | ~5.3 GB | 4-bit NF4 QLoRA | 1 | 16 | 1280 |
| **Local RTX 4050 Laptop** | ~5.5 GB | 4-bit NF4 QLoRA | 1 | 16 | 1280 |
| **Google Colab Tesla T4** | ~14.56 GB | 4-bit NF4 or FP16 LoRA | 2 | 8 | 2048 |
| **NVIDIA A100 (40GB/80GB)**| 40–80 GB | BF16 / Full LoRA | 4–8 | 4 | 4096+ |

---

## End-to-End Walkthrough: 10-Step Operational Guide

1. **Develop in Antigravity**: Write and test code locally on Windows/Linux.
2. **Commit changes**: Run `git commit -am "your message"` (data and caches are auto-ignored).
3. **Push to GitHub**: Run `git push origin master`.
4. **Open Colab**: Open your shared notebook: [Google Colab Notebook](https://colab.research.google.com/drive/1DXYXlnGqz-PR120-4KqZFL1jUJWWbOdm).
5. **Connect the T4**: In Colab, click **Connect** → Verify **T4 GPU** runtime.
6. **Pull latest project**: Run Step 2 cell to clone or pull your private repository.
7. **Mount Google Drive**: Run Step 4 cell (`drive.mount('/content/drive')`).
8. **Run the Sanity Test**: Run Step 8 cell to execute 50 steps and verify checkpoints.
9. **Start Full Training**: Run Step 9 cell (2 epochs, auto-saving to Google Drive).
10. **Resume after Disconnect**: If disconnected, simply re-run Step 4 (mount Drive) and the Resume cell.

---

## Documentation
- [Setup & Installation](docs/setup.md)
- [Architecture & Design](docs/architecture.md)
- [Agent Hierarchy](docs/agents.md)
- [Model System](docs/models.md)
- [Training & Datasets](docs/training_and_datasets.md)
- [Troubleshooting](docs/troubleshooting.md)

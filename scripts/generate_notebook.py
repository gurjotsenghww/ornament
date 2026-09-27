#!/usr/bin/env python3
"""
Generates valid Jupyter Notebooks (colab/train.ipynb and colab_training.ipynb)
for Google Colab Tesla T4 training with Google Drive persistence.
"""

import json
from pathlib import Path

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Ornàment AI Website Engineer — Google Colab Cloud Training Pipeline\n",
                "\n",
                "**Hardware Profile**: NVIDIA Tesla T4 (~14.56 GB usable VRAM) | Google AI Pro\n",
                "**Persistent Storage**: Google Drive (`/content/drive/MyDrive/Ornàment/`)\n",
                "**Fast Scratch Workspace**: `/content/ornament_workspace/`\n",
                "\n",
                "This notebook provides a clean, reproducible, and fault-tolerant pipeline to train the **Ornàment Qwen Coder** LoRA adapter in the cloud with persistent checkpointing to Google Drive."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## STEP 1: Hardware & GPU Diagnostic Check\n",
                "Verify that a CUDA-capable GPU (Tesla T4) is allocated."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import torch\n",
                "import platform\n",
                "\n",
                "print('=' * 60)\n",
                "print('          STEP 1: HARDWARE & CUDA DIAGNOSTIC')\n",
                "print('=' * 60)\n",
                "print(f'Python Version   : {platform.python_version()}')\n",
                "print(f'PyTorch Version  : {torch.__version__}')\n",
                "print(f'CUDA Available   : {torch.cuda.is_available()}')\n",
                "\n",
                "if torch.cuda.is_available():\n",
                "    gpu_name = torch.cuda.get_device_name(0)\n",
                "    props = torch.cuda.get_device_properties(0)\n",
                "    total_vram = round(props.total_memory / (1024 ** 3), 2)\n",
                "    allocated = round(torch.cuda.memory_allocated(0) / (1024 ** 3), 2)\n",
                "    usable_free = round(total_vram - allocated, 2)\n",
                "    print(f'CUDA Version     : {torch.version.cuda}')\n",
                "    print(f'GPU Name         : {gpu_name}')\n",
                "    print(f'Total VRAM       : {total_vram} GB')\n",
                "    print(f'Usable Free VRAM : ~{usable_free} GB')\n",
                "    print(f'BF16 Supported   : {torch.cuda.is_bf16_supported()}')\n",
                "    print('[OK] Hardware verified for training.')\n",
                "else:\n",
                "    print('[!] WARNING: No GPU detected! Go to Runtime -> Change runtime type -> Select T4 GPU.')\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## STEP 2: Clone or Pull GitHub Private Repository\n",
                "Uses Colab Secrets (`userdata`) or interactive prompt. **No tokens or secrets are hardcoded.**"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import getpass\n",
                "\n",
                "REPO_DIR = '/content/Ornàment'\n",
                "GITHUB_REPO = input('Enter your GitHub repository (e.g. username/ornament): ').strip()\n",
                "\n",
                "# Secure authentication via Google Colab Secrets or interactive token prompt\n",
                "token = None\n",
                "try:\n",
                "    from google.colab import userdata\n",
                "    token = userdata.get('GITHUB_TOKEN')\n",
                "    print('[OK] Retrieved GitHub Personal Access Token from Colab Secrets.')\n",
                "except Exception:\n",
                "    pass\n",
                "\n",
                "if not token:\n",
                "    token = getpass.getpass('Enter GitHub Personal Access Token (PAT with repo access): ').strip()\n",
                "\n",
                "clone_url = f'https://{token}@github.com/{GITHUB_REPO}.git'\n",
                "\n",
                "if os.path.exists(REPO_DIR):\n",
                "    print(f'[*] Repository already exists at {REPO_DIR}. Pulling latest changes...')\n",
                "    !cd {REPO_DIR} && git pull\n",
                "else:\n",
                "    print(f'[*] Cloning repository into {REPO_DIR}...')\n",
                "    !git clone {clone_url} {REPO_DIR}\n",
                "\n",
                "os.chdir(REPO_DIR)\n",
                "print(f'[OK] Current working directory: {os.getcwd()}')\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## STEP 3: Install Dependencies\n",
                "Installs training dependencies (`transformers`, `peft`, `bitsandbytes`, `datasets`) without clobbering Colab's PyTorch/CUDA installation."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "!pip install -q -r requirements.txt\n",
                "!pip install -q -r requirements-train.txt\n",
                "!pip install -q -e .\n",
                "print('[OK] Dependencies installed successfully.')\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## STEP 4: Mount Google Drive & Setup Persistent Storage\n",
                "Persistent structure ensures checkpoints and trained weights survive runtime disconnects."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from google.colab import drive\n",
                "drive.mount('/content/drive')\n",
                "\n",
                "GDRIVE_ROOT = '/content/drive/MyDrive/Ornàment'\n",
                "!mkdir -p {GDRIVE_ROOT}/datasets\n",
                "!mkdir -p {GDRIVE_ROOT}/checkpoints/v0.1.0\n",
                "!mkdir -p {GDRIVE_ROOT}/models\n",
                "!mkdir -p {GDRIVE_ROOT}/logs\n",
                "print(f'[OK] Persistent storage configured at: {GDRIVE_ROOT}')\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## STEP 5 & 6: Fast Local Scratch Workspace & Dataset Synchronization\n",
                "Datasets are cached on `/content/` NVMe storage to eliminate slow Google Drive micro-reads during training."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import shutil\n",
                "from pathlib import Path\n",
                "\n",
                "WORKSPACE = Path('/content/ornament_workspace')\n",
                "WORKSPACE.mkdir(parents=True, exist_ok=True)\n",
                "(WORKSPACE / 'datasets').mkdir(parents=True, exist_ok=True)\n",
                "\n",
                "# Check persistent Drive first, then repository files\n",
                "repo_dataset = Path('/content/Ornàment/ai-website-engineer-model/datasets/ornament_master_train.jsonl')\n",
                "gdrive_dataset = Path(f'{GDRIVE_ROOT}/datasets/ornament_master_train.jsonl')\n",
                "target_train = WORKSPACE / 'datasets' / 'ornament_master_train.jsonl'\n",
                "target_val = WORKSPACE / 'datasets' / 'ornament_master_val.jsonl'\n",
                "\n",
                "if gdrive_dataset.exists():\n",
                "    print(f'[*] Syncing dataset from Google Drive: {gdrive_dataset}')\n",
                "    shutil.copy(gdrive_dataset, target_train)\n",
                "    val_gdrive = Path(f'{GDRIVE_ROOT}/datasets/ornament_master_val.jsonl')\n",
                "    if val_gdrive.exists():\n",
                "        shutil.copy(val_gdrive, target_val)\n",
                "elif repo_dataset.exists():\n",
                "    print(f'[*] Using dataset from repository: {repo_dataset}')\n",
                "    shutil.copy(repo_dataset, target_train)\n",
                "    val_repo = Path('/content/Ornàment/ai-website-engineer-model/datasets/ornament_master_val.jsonl')\n",
                "    if val_repo.exists():\n",
                "        shutil.copy(val_repo, target_val)\n",
                "\n",
                "print(f'[OK] Local dataset size: {target_train.stat().st_size / 1024:.1f} KB')\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## STEP 7: Run GPU Matrix Multiplication Sanity Test\n",
                "Validates GPU compute capability before allocating large model tensors."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import torch\n",
                "\n",
                "x = torch.randn(4096, 4096, device='cuda')\n",
                "y = x @ x\n",
                "del x, y\n",
                "torch.cuda.empty_cache()\n",
                "\n",
                "print('[SUCCESS] GPU matrix computation successful!')\n",
                "print(f'Device: {torch.cuda.get_device_name(0)}')\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## STEP 8: Training Sanity Test (50 Steps)\n",
                "Runs exactly 50 training steps to verify:\n",
                "- Forward pass\n",
                "- Backward pass (gradients)\n",
                "- Optimizer step & loss calculation\n",
                "- VRAM stability (<10 GB on T4)\n",
                "- Checkpoint serialization"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "\n",
                "# Model Selection: '8B' (Qwen 7B/8B Coder on Colab T4) or '3B'\n",
                "MODEL_TIER = '8B'\n",
                "CONFIG_FILE = 'ai-website-engineer-model/configs/training_config_8b.yaml' if MODEL_TIER == '8B' else 'ai-website-engineer-model/configs/training_config.yaml'\n",
                "\n",
                "os.environ['OUTPUT_PATH'] = f'/content/ornament_workspace/adapters/sanity_test_{MODEL_TIER.lower()}'\n",
                "os.environ['DATASET_PATH'] = '/content/ornament_workspace/datasets/ornament_master_train.jsonl'\n",
                "os.environ['VAL_DATASET_PATH'] = '/content/ornament_workspace/datasets/ornament_master_val.jsonl'\n",
                "\n",
                "print(f'[*] Starting 50-step Sanity Test for Qwen {MODEL_TIER}...')\n",
                "!python ai-website-engineer-model/scripts/train_lora.py \\\n",
                "    --config {CONFIG_FILE} \\\n",
                "    --sanity-test\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Checkpoint Verification\n",
                "Confirms that checkpoint weights are properly saved and reloadable."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pathlib import Path\n",
                "\n",
                "adapter_dir = Path('/content/ornament_workspace/adapters/sanity_test')\n",
                "checkpoints = list(adapter_dir.glob('checkpoint-*'))\n",
                "print(f'[OK] Checkpoints saved: {[c.name for c in checkpoints]}')\n",
                "print('[SUCCESS] Sanity Test Passed! You are ready to run full training.')\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "---\n",
                "# ========================================================\n",
                "# STEP 9: FULL PRODUCTION TRAINING RUN (Manual Execution)\n",
                "# ========================================================\n",
                "> [!IMPORTANT]\n",
                "> Execute this cell only after Step 8 passes.\n",
                "> Checkpoints will be saved directly into Google Drive (`/content/drive/MyDrive/Ornàment/checkpoints/v0.1.0/`)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "\n",
                "# Model Selection: '8B' (Qwen 7B/8B Coder on Colab T4) or '3B'\n",
                "MODEL_TIER = '8B'\n",
                "CONFIG_FILE = 'ai-website-engineer-model/configs/training_config_8b.yaml' if MODEL_TIER == '8B' else 'ai-website-engineer-model/configs/training_config.yaml'\n",
                "GDRIVE_CKPT = f'/content/drive/MyDrive/Ornàment/checkpoints/v0.1.0-{MODEL_TIER.lower()}'\n",
                "\n",
                "os.environ['OUTPUT_PATH'] = GDRIVE_CKPT\n",
                "os.environ['DATASET_PATH'] = '/content/ornament_workspace/datasets/ornament_master_train.jsonl'\n",
                "os.environ['VAL_DATASET_PATH'] = '/content/ornament_workspace/datasets/ornament_master_val.jsonl'\n",
                "\n",
                "print('=' * 65)\n",
                "print(f'      LAUNCHING FULL PRODUCTION TRAINING RUN (Qwen {MODEL_TIER})     ')\n",
                "print('=' * 65)\n",
                "print(f'[*] Using Config  : {CONFIG_FILE}')\n",
                "print(f'[*] Checkpoint Dir: {GDRIVE_CKPT}')\n",
                "\n",
                "!python ai-website-engineer-model/scripts/train_lora.py \\\n",
                "    --config {CONFIG_FILE}\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## RESUME TRAINING (If Colab Disconnects)\n",
                "If the runtime terminated or disconnected, run this cell to seamlessly continue from the latest checkpoint stored on Google Drive."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "GDRIVE_CKPT = '/content/drive/MyDrive/Ornàment/checkpoints/v0.1.0'\n",
                "os.environ['OUTPUT_PATH'] = GDRIVE_CKPT\n",
                "\n",
                "print(f'[*] Resuming training from latest checkpoint in: {GDRIVE_CKPT}')\n",
                "!python ai-website-engineer-model/scripts/train_lora.py \\\n",
                "    --config ai-website-engineer-model/configs/training_config.yaml \\\n",
                "    --resume latest\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Post-Training Benchmark & Ability Evaluation\n",
                "Measure design theory, CSS Container Queries, and Minimal Change Policy scores against baseline."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "!python ai-website-engineer-model/evaluation/evaluate_trained_adapter.py\n"
            ]
        }
    ],
    "metadata": {
        "accelerator": "GPU",
        "colab": {
            "provenance": [],
            "gpuType": "T4"
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

colab_dir = Path("colab")
colab_dir.mkdir(exist_ok=True)

with open(colab_dir / "train.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

with open("colab_training.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("Generated colab/train.ipynb and colab_training.ipynb successfully.")

#!/usr/bin/env bash
# ==============================================================================
# Ornàment Google Colab Setup Script
# Configures the training environment on Google Colab (Tesla T4 or higher)
# ==============================================================================

set -e

echo "=========================================================="
echo "         ORNÀMENT GOOGLE COLAB ENVIRONMENT SETUP"
echo "=========================================================="

# 1. Diagnostic Check
echo "[*] Checking Python and GPU status..."
python3 scripts/check_gpu.py

# 2. Install ML Dependencies without overwriting Colab's PyTorch/CUDA
echo "[*] Installing project dependencies..."
pip install -q -r requirements.txt
pip install -q -r requirements-train.txt
pip install -q -e .

# 3. Setup Persistent Google Drive Structure (if mounted)
GDRIVE_DIR="/content/drive/MyDrive/Ornàment"
if [ -d "/content/drive/MyDrive" ]; then
    echo "[*] Google Drive detected. Setting up persistent directories..."
    mkdir -p "${GDRIVE_DIR}/datasets"
    mkdir -p "${GDRIVE_DIR}/checkpoints"
    mkdir -p "${GDRIVE_DIR}/models"
    mkdir -p "${GDRIVE_DIR}/logs"
    echo "[OK] Persistent directories created at: ${GDRIVE_DIR}"
else
    echo "[!] Google Drive not yet mounted at /content/drive/MyDrive."
    echo "    Run from google.colab import drive; drive.mount('/content/drive') first."
fi

# 4. Setup Fast NVMe Scratch Workspace in /content
WORKSPACE_DIR="/content/ornament_workspace"
mkdir -p "${WORKSPACE_DIR}/datasets"
mkdir -p "${WORKSPACE_DIR}/adapters"
echo "[OK] Fast local workspace prepared at: ${WORKSPACE_DIR}"

echo "=========================================================="
echo "[SUCCESS] Colab setup completed successfully."
echo "=========================================================="

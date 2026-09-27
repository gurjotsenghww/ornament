#!/usr/bin/env bash
# ==============================================================================
# Ornàment Resumption Script
# Resumes training from the latest saved checkpoint after runtime disconnection
# ==============================================================================

set -e

CONFIG_FILE="${1:-ai-website-engineer-model/configs/training_config.yaml}"

# If Google Drive is mounted on Colab, check persistent storage
if [ -d "/content/drive/MyDrive/Ornàment" ]; then
    echo "[*] Google Drive detected. Checking persistent checkpoint directory..."
    export OUTPUT_PATH="/content/drive/MyDrive/Ornàment/checkpoints/v0.1.0"
fi

echo "=========================================================="
echo "          RESUMING ORNÀMENT MODEL TRAINING"
echo "=========================================================="
echo "[*] Configuration : ${CONFIG_FILE}"
echo "[*] Resuming from : latest checkpoint"

python3 ai-website-engineer-model/scripts/train_lora.py --config "${CONFIG_FILE}" --resume latest "$@"

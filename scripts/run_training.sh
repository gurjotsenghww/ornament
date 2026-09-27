#!/usr/bin/env bash
# ==============================================================================
# Ornàment Multi-Device Training Runner
# Runs training on Local Machine, Google Colab (Tesla T4), or Cloud Clusters
# ==============================================================================

set -e

CONFIG_FILE="${1:-ai-website-engineer-model/configs/training_config.yaml}"

# If Google Drive is mounted on Colab, save checkpoints directly to persistent storage
if [ -d "/content/drive/MyDrive/Ornàment" ]; then
    echo "[*] Google Drive detected. Redirecting adapter outputs to persistent Drive storage..."
    export OUTPUT_PATH="/content/drive/MyDrive/Ornàment/checkpoints/v0.1.0"
fi

echo "=========================================================="
echo "          STARTING ORNÀMENT MODEL TRAINING"
echo "=========================================================="
echo "[*] Config file : ${CONFIG_FILE}"

python3 ai-website-engineer-model/scripts/train_lora.py --config "${CONFIG_FILE}" "$@"

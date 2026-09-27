import os
from pathlib import Path
from typing import Optional
from huggingface_hub import hf_hub_download
from ornament.config import settings

QWEN_MODELS = {
    "qwen2.5-coder-7b-q4": {
        "repo_id": "Qwen/Qwen2.5-Coder-7B-Instruct-GGUF",
        "filename": "qwen2.5-coder-7b-instruct-q4_k_m.gguf",
        "size_gb": 4.68,
        "recommended_for": "Inference on RTX 3050 6GB GPU (Strict 4-bit quantization, fits ~4.7GB VRAM)"
    },
    "qwen2.5-coder-3b-q4": {
        "repo_id": "Qwen/Qwen2.5-Coder-3B-Instruct-GGUF",
        "filename": "qwen2.5-coder-3b-instruct-q4_k_m.gguf",
        "size_gb": 1.93,
        "recommended_for": "Balanced Local Inference & Lightweight Training on 6GB VRAM"
    },
    "qwen2.5-coder-1.5b-q4": {
        "repo_id": "Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF",
        "filename": "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf",
        "size_gb": 1.12,
        "recommended_for": "Fast Local LoRA Fine-Tuning directly on 6GB VRAM GPU"
    }
}

class ModelDownloader:
    """
    Downloads and manages compatible official Qwen GGUF model weights (Section 3, 49).
    Stores weights in ai-website-engineer-model/weights/ without cluttering git history.
    """

    @classmethod
    def get_weights_dir(cls) -> Path:
        d = settings.base_dir / "ai-website-engineer-model" / "weights"
        d.mkdir(parents=True, exist_ok=True)
        return d

    @classmethod
    def download_model(cls, model_key: str = "qwen2.5-coder-7b-q4") -> Path:
        if model_key not in QWEN_MODELS:
            raise ValueError(f"Unknown model key '{model_key}'. Available: {list(QWEN_MODELS.keys())}")

        info = QWEN_MODELS[model_key]
        dest_dir = cls.get_weights_dir()
        target_path = dest_dir / info["filename"]

        if target_path.exists():
            print(f"[OK] Model weight file already exists: {target_path} ({target_path.stat().st_size / (1024**3):.2f} GB)")
            return target_path

        print(f"[*] Downloading {info['filename']} ({info['size_gb']} GB) from Hugging Face...")
        print(f"    Repository: {info['repo_id']}")
        print(f"    Recommended: {info['recommended_for']}")

        downloaded_file = hf_hub_download(
            repo_id=info["repo_id"],
            filename=info["filename"],
            local_dir=str(dest_dir),
            local_dir_use_symlinks=False
        )
        return Path(downloaded_file)

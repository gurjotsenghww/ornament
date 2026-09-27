"""
Unified Configuration Manager for Ornàment Training.
Loads configuration from YAML/JSON with automatic overrides from environment variables:
- MODEL_NAME
- DATASET_PATH
- CHECKPOINT_PATH
- OUTPUT_PATH
- BATCH_SIZE
- GRADIENT_ACCUMULATION_STEPS
- LEARNING_RATE
- NUM_EPOCHS
- MAX_STEPS
- CONTEXT_LENGTH
- PRECISION
- DEVICE
"""

import os
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class TrainingConfig:
    # Model settings
    model_name: str = "Qwen/Qwen2.5-Coder-3B-Instruct"
    precision: str = "4bit"  # 4bit, 8bit, fp16, bf16
    device: str = "auto"     # auto, cuda, cpu
    context_length: int = 1280

    # LoRA settings
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: List[str] = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"
    ])
    bias: str = "none"
    task_type: str = "CAUSAL_LM"

    # Training hyperparameters
    batch_size: int = 1
    gradient_accumulation_steps: int = 16
    learning_rate: float = 0.0002
    num_epochs: int = 2
    max_steps: int = -1  # -1 for full training, >0 for sanity testing
    warmup_ratio: float = 0.03
    max_grad_norm: float = 0.3
    optim: str = "paged_adamw_8bit"
    logging_steps: int = 10
    save_strategy: str = "steps"
    save_steps: int = 20
    eval_strategy: str = "no"
    gradient_checkpointing: bool = True

    # Storage paths
    dataset_path: str = "ai-website-engineer-model/datasets/ornament_master_train.jsonl"
    val_dataset_path: str = "ai-website-engineer-model/datasets/ornament_master_val.jsonl"
    checkpoint_path: str = ""
    output_path: str = "ai-website-engineer-model/adapters/v0.1.0"

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "TrainingConfig":
        """Loads configuration from file and applies environment variable overrides."""
        instance = cls()
        data: Dict[str, Any] = {}

        if config_path:
            p = Path(config_path)
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    if p.suffix in [".yaml", ".yml"]:
                        if yaml is None:
                            raise ImportError("PyYAML is required to parse .yaml config files.")
                        data = yaml.safe_load(f) or {}
                    else:
                        data = json.load(f)

        # Parse nested YAML or flat JSON structure
        if "model" in data:
            m = data.get("model", {})
            instance.model_name = m.get("model_name", instance.model_name)
            instance.precision = m.get("precision", instance.precision)
            instance.device = m.get("device", instance.device)
            instance.context_length = m.get("context_length", instance.context_length)

        if "lora" in data:
            l = data.get("lora", {})
            instance.lora_r = l.get("r", instance.lora_r)
            instance.lora_alpha = l.get("alpha", instance.lora_alpha)
            instance.lora_dropout = l.get("dropout", instance.lora_dropout)
            instance.target_modules = l.get("target_modules", instance.target_modules)

        if "training" in data:
            t = data.get("training", {})
            instance.batch_size = t.get("batch_size", instance.batch_size)
            instance.gradient_accumulation_steps = t.get("gradient_accumulation_steps", instance.gradient_accumulation_steps)
            instance.learning_rate = float(t.get("learning_rate", instance.learning_rate))
            instance.num_epochs = int(t.get("num_epochs", instance.num_epochs))
            instance.max_steps = int(t.get("max_steps", instance.max_steps))
            instance.warmup_ratio = float(t.get("warmup_ratio", instance.warmup_ratio))
            instance.max_grad_norm = float(t.get("max_grad_norm", instance.max_grad_norm))
            instance.optim = t.get("optim", instance.optim)
            instance.logging_steps = int(t.get("logging_steps", instance.logging_steps))
            instance.save_strategy = t.get("save_strategy", instance.save_strategy)
            instance.save_steps = int(t.get("save_steps", instance.save_steps))
            instance.eval_strategy = t.get("eval_strategy", instance.eval_strategy)
            instance.gradient_checkpointing = bool(t.get("gradient_checkpointing", instance.gradient_checkpointing))

        if "paths" in data:
            p_data = data.get("paths", {})
            instance.dataset_path = p_data.get("dataset_path", instance.dataset_path)
            instance.val_dataset_path = p_data.get("val_dataset_path", instance.val_dataset_path)
            instance.checkpoint_path = p_data.get("checkpoint_path", instance.checkpoint_path)
            instance.output_path = p_data.get("output_path", instance.output_path)

        # Legacy flat structure support
        if "base_model" in data:
            instance.model_name = data["base_model"]
        if "training_hyperparameters" in data:
            th = data["training_hyperparameters"]
            instance.batch_size = th.get("per_device_train_batch_size", instance.batch_size)
            instance.gradient_accumulation_steps = th.get("gradient_accumulation_steps", instance.gradient_accumulation_steps)
            instance.learning_rate = float(th.get("learning_rate", instance.learning_rate))
            instance.num_epochs = int(th.get("num_epochs", instance.num_epochs))
            instance.max_steps = int(th.get("max_steps", instance.max_steps))
            instance.context_length = int(th.get("max_seq_length", instance.context_length))

        # --- ENVIRONMENT VARIABLE OVERRIDES (PHASE 3 SPECIFICATION) ---
        if os.getenv("MODEL_NAME"):
            instance.model_name = os.environ["MODEL_NAME"]
        if os.getenv("DATASET_PATH"):
            instance.dataset_path = os.environ["DATASET_PATH"]
        if os.getenv("CHECKPOINT_PATH"):
            instance.checkpoint_path = os.environ["CHECKPOINT_PATH"]
        if os.getenv("OUTPUT_PATH"):
            instance.output_path = os.environ["OUTPUT_PATH"]
        if os.getenv("BATCH_SIZE"):
            instance.batch_size = int(os.environ["BATCH_SIZE"])
        if os.getenv("GRADIENT_ACCUMULATION_STEPS"):
            instance.gradient_accumulation_steps = int(os.environ["GRADIENT_ACCUMULATION_STEPS"])
        if os.getenv("LEARNING_RATE"):
            instance.learning_rate = float(os.environ["LEARNING_RATE"])
        if os.getenv("NUM_EPOCHS"):
            instance.num_epochs = int(os.environ["NUM_EPOCHS"])
        if os.getenv("MAX_STEPS"):
            instance.max_steps = int(os.environ["MAX_STEPS"])
        if os.getenv("CONTEXT_LENGTH"):
            instance.context_length = int(os.environ["CONTEXT_LENGTH"])
        if os.getenv("PRECISION"):
            instance.precision = os.environ["PRECISION"]
        if os.getenv("DEVICE"):
            instance.device = os.environ["DEVICE"]

        return instance

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "precision": self.precision,
            "device": self.device,
            "context_length": self.context_length,
            "lora_r": self.lora_r,
            "lora_alpha": self.lora_alpha,
            "lora_dropout": self.lora_dropout,
            "target_modules": self.target_modules,
            "batch_size": self.batch_size,
            "gradient_accumulation_steps": self.gradient_accumulation_steps,
            "learning_rate": self.learning_rate,
            "num_epochs": self.num_epochs,
            "max_steps": self.max_steps,
            "optim": self.optim,
            "save_steps": self.save_steps,
            "dataset_path": self.dataset_path,
            "val_dataset_path": self.val_dataset_path,
            "checkpoint_path": self.checkpoint_path,
            "output_path": self.output_path,
        }

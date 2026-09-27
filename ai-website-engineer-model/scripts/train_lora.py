#!/usr/bin/env python3
"""
Ornàment Unified Multi-Device Training Script.
Supports:
- Local Consumer GPUs: NVIDIA RTX 3050, RTX 4050 (6GB VRAM)
- Cloud GPUs: Google Colab Tesla T4 (~15GB VRAM), V100
- High-End / Cluster: NVIDIA A100 (40GB/80GB), H100, DGX

Features:
- Auto-hardware detection & PyTorch/CUDA telemetry
- Dynamic precision: 4-bit NF4 QLoRA, 8-bit, FP16, BF16
- Gradient accumulation & checkpointing
- Resumable training from checkpoints (survives Colab disconnections)
- Sanity testing mode (--max-steps / --sanity-test)
- Robust CUDA OOM recovery guidance
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add parent directory for config loader import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from configs.config_loader import TrainingConfig

# Cache path defaults (only if not already set by environment)
project_root = Path(__file__).resolve().parent.parent.parent
cache_root = project_root / ".cache"
if "HF_HOME" not in os.environ and cache_root.exists():
    os.environ["HF_HOME"] = str(cache_root / "huggingface")
if "HF_HUB_CACHE" not in os.environ and cache_root.exists():
    os.environ["HF_HUB_CACHE"] = str(cache_root / "huggingface" / "hub")
if "TORCH_HOME" not in os.environ and cache_root.exists():
    os.environ["TORCH_HOME"] = str(cache_root / "torch")
if "PIP_CACHE_DIR" not in os.environ and cache_root.exists():
    os.environ["PIP_CACHE_DIR"] = str(cache_root / "pip")
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"


def train(
    config_path: Optional[Path] = None,
    train_dataset_path: Optional[Path] = None,
    val_dataset_path: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    dry_run: bool = False,
    resume_checkpoint: Optional[str] = None,
    max_steps: Optional[int] = None,
    batch_size: Optional[int] = None,
    gradient_accumulation_steps: Optional[int] = None,
    learning_rate: Optional[float] = None,
    epochs: Optional[int] = None,
    precision: Optional[str] = None,
):
    print("=" * 65)
    print("      ORNÀMENT AI WEBSITE ENGINEER — UNIFIED TRAINING PIPELINE")
    print("=" * 65 + "\n")

    # 1. Load Configuration
    cfg_file = str(config_path) if config_path else None
    config = TrainingConfig.load(cfg_file)

    # CLI Overrides
    if train_dataset_path:
        config.dataset_path = str(train_dataset_path)
    if val_dataset_path:
        config.val_dataset_path = str(val_dataset_path)
    if output_dir:
        config.output_path = str(output_dir)
    if resume_checkpoint:
        config.checkpoint_path = resume_checkpoint
    if max_steps is not None and max_steps > 0:
        config.max_steps = max_steps
    if batch_size is not None and batch_size > 0:
        config.batch_size = batch_size
    if gradient_accumulation_steps is not None and gradient_accumulation_steps > 0:
        config.gradient_accumulation_steps = gradient_accumulation_steps
    if learning_rate is not None and learning_rate > 0:
        config.learning_rate = learning_rate
    if epochs is not None and epochs > 0:
        config.num_epochs = epochs
    if precision:
        config.precision = precision.lower()

    out_path = Path(config.output_path)
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"[*] Base Model       : {config.model_name}")
    print(f"[*] Train Dataset    : {config.dataset_path}")
    print(f"[*] Val Dataset      : {config.val_dataset_path}")
    print(f"[*] Output Directory : {config.output_path}")
    print(f"[*] Precision        : {config.precision.upper()}")
    print(f"[*] Batch Size       : {config.batch_size} (accumulation: {config.gradient_accumulation_steps})")
    print(f"[*] Learning Rate    : {config.learning_rate}")
    print(f"[*] Epochs / Steps   : {config.num_epochs} epochs | max_steps={config.max_steps}")
    print(f"[*] Context Length   : {config.context_length}\n")

    # Dry run / mock check
    if dry_run or os.getenv("ORNAMENT_TRAIN_MOCK") == "1":
        print("[*] Dry run mode enabled. Validating dataset schema...")
        count = 0
        ds_file = Path(config.dataset_path)
        if not ds_file.exists():
            ds_file = project_root / config.dataset_path
        with open(ds_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    assert "messages" in item, "Missing 'messages' in ChatML item"
                    count += 1
        print(f"[OK] Dataset validated: {count} samples with valid ChatML schema.")
        mock_meta = {
            "status": "ready_for_training",
            "samples": count,
            "base_model": config.model_name,
            "precision": config.precision,
            "lora_r": config.lora_r,
            "lora_alpha": config.lora_alpha,
            "target_modules": config.target_modules
        }
        with open(out_path / "training_spec.json", "w", encoding="utf-8") as f:
            json.dump(mock_meta, f, indent=2)
        print(f"[SUCCESS] Training spec written to {out_path / 'training_spec.json'}")
        return True

    # 2. Framework & GPU Telemetry
    try:
        import torch
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
            TrainingArguments,
            Trainer,
            DataCollatorForSeq2Seq
        )
        from peft import (
            LoraConfig,
            get_peft_model,
            prepare_model_for_kbit_training
        )
        from datasets import Dataset
    except ImportError as e:
        print(f"[!] Required training framework missing: {e}")
        print("[*] Install dependencies with: pip install -r requirements-train.txt")
        return False

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 65)
    print("                 HARDWARE & CUDA TELEMETRY")
    print("=" * 65)
    print(f"[*] PyTorch Version  : {torch.__version__}")
    print(f"[*] CUDA Available   : {torch.cuda.is_available()}")
    print(f"[*] CUDA Version     : {torch.version.cuda or 'N/A'}")
    print(f"[*] Selected Device  : {device}")

    if not torch.cuda.is_available():
        print("\n[!] WARNING: CUDA is not available. GPU is required for efficient training.")
        return False

    gpu_name = torch.cuda.get_device_name(0)
    props = torch.cuda.get_device_properties(0)
    total_vram_gb = round(props.total_memory / (1024 ** 3), 2)
    print(f"[*] Detected GPU     : {gpu_name}")
    print(f"[*] Total VRAM       : {total_vram_gb} GB")
    print(f"[*] BF16 Supported   : {torch.cuda.is_bf16_supported()}")
    print(f"[*] FP16 Supported   : True\n")

    # 3. Model & Quantization Configuration
    bnb_config = None
    torch_dtype = torch.float16

    if config.precision == "4bit":
        print("[*] Configuring 4-bit NormalFloat (NF4) double quantization...")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16
        )
    elif config.precision == "8bit":
        print("[*] Configuring 8-bit quantization...")
        bnb_config = BitsAndBytesConfig(load_in_8bit=True)
    elif config.precision == "bf16":
        torch_dtype = torch.bfloat16
    elif config.precision == "fp16":
        torch_dtype = torch.float16

    # Load Tokenizer
    print(f"[*] Loading tokenizer for {config.model_name}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(config.model_name, local_files_only=True, trust_remote_code=True)
    except Exception:
        tokenizer = AutoTokenizer.from_pretrained(config.model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load Base Model
    print(f"[*] Loading base model weights ({config.precision.upper()})...")
    load_kwargs: Dict[str, Any] = {
        "device_map": "auto",
        "trust_remote_code": True,
    }
    if bnb_config is not None:
        load_kwargs["quantization_config"] = bnb_config
    else:
        load_kwargs["torch_dtype"] = torch_dtype

    try:
        model = AutoModelForCausalLM.from_pretrained(
            config.model_name,
            local_files_only=True,
            **load_kwargs
        )
    except Exception:
        model = AutoModelForCausalLM.from_pretrained(
            config.model_name,
            **load_kwargs
        )

    if config.precision in ["4bit", "8bit"]:
        model = prepare_model_for_kbit_training(model)
    if config.gradient_checkpointing:
        model.gradient_checkpointing_enable()

    # 4. Attach LoRA Adapter
    print(f"[*] Initializing LoRA adapter (r={config.lora_r}, alpha={config.lora_alpha})...")
    peft_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        target_modules=config.target_modules,
        lora_dropout=config.lora_dropout,
        bias=config.bias,
        task_type=config.task_type
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 5. Load and Tokenize Datasets
    print(f"\n[*] Processing ChatML dataset into tokenized sequences...")
    def load_jsonl(p: Path) -> List[Dict[str, Any]]:
        entries = []
        target = p if p.exists() else (project_root / p)
        if not target.exists():
            raise FileNotFoundError(f"Dataset file not found at: {target}")
        with open(target, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries

    raw_train = load_jsonl(Path(config.dataset_path))
    raw_val = load_jsonl(Path(config.val_dataset_path))
    print(f"[*] Ingested {len(raw_train)} training samples and {len(raw_val)} validation samples.")

    max_seq_len = config.context_length

    def preprocess_function(examples):
        input_ids_list = []
        labels_list = []
        for msgs in examples["messages"]:
            text = tokenizer.apply_chat_template(
                msgs,
                tokenize=False,
                add_generation_prompt=False
            )
            tokens = tokenizer(
                text,
                truncation=True,
                max_length=max_seq_len,
                padding=False,
                return_tensors=None
            )
            input_ids = tokens["input_ids"]
            labels = list(input_ids)
            input_ids_list.append(input_ids)
            labels_list.append(labels)
        return {"input_ids": input_ids_list, "labels": labels_list}

    train_ds = Dataset.from_list(raw_train)
    val_ds = Dataset.from_list(raw_val)

    train_tokenized = train_ds.map(preprocess_function, batched=True, remove_columns=train_ds.column_names)
    val_tokenized = val_ds.map(preprocess_function, batched=True, remove_columns=val_ds.column_names)

    # 6. Training Arguments & Resumption Logic
    training_kwargs: Dict[str, Any] = {
        "output_dir": str(out_path),
        "per_device_train_batch_size": config.batch_size,
        "gradient_accumulation_steps": config.gradient_accumulation_steps,
        "learning_rate": config.learning_rate,
        "warmup_steps": 10,
        "max_grad_norm": config.max_grad_norm,
        "num_train_epochs": config.num_epochs,
        "optim": config.optim,
        "fp16": (config.precision != "bf16"),
        "bf16": (config.precision == "bf16" and torch.cuda.is_bf16_supported()),
        "logging_steps": config.logging_steps,
        "eval_strategy": config.eval_strategy,
        "save_strategy": config.save_strategy,
        "save_steps": config.save_steps,
        "save_total_limit": 3,
        "report_to": "none",
        "dataloader_num_workers": 0,
    }

    if config.max_steps > 0:
        training_kwargs["max_steps"] = config.max_steps
        print(f"[*] Active Mode: SANITY TEST / FIXED STEPS ({config.max_steps} steps)")
    else:
        print(f"[*] Active Mode: FULL TRAINING ({config.num_epochs} epochs)")

    training_args = TrainingArguments(**training_kwargs)

    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        padding=True,
        return_tensors="pt"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        data_collator=data_collator
    )

    # Determine Resumption Target
    resume_from = None
    if config.checkpoint_path:
        cp = config.checkpoint_path.strip()
        if cp.lower() in ["latest", "true", "1"]:
            ckpts = list(out_path.glob("checkpoint-*"))
            if ckpts:
                ckpts.sort(key=lambda x: int(x.name.split("-")[1]))
                resume_from = str(ckpts[-1])
                print(f"[*] Found latest checkpoint to resume: {resume_from}")
            else:
                print(f"[*] No checkpoint found in {out_path}. Starting fresh training.")
        else:
            resume_from = cp
            print(f"[*] Resuming explicitly from: {resume_from}")

    # 7. Execute Training Loop with CUDA OOM Safeguard
    print("\n" + "=" * 65)
    print("                  LAUNCHING TRAINING LOOP")
    print("=" * 65)
    start_time = time.time()

    try:
        trainer.train(resume_from_checkpoint=resume_from)
    except torch.cuda.OutOfMemoryError as oom:
        print("\n" + "!" * 65)
        print("          CUDA OUT OF MEMORY (OOM) ERROR CAUGHT")
        print("!" * 65)
        print(f"[!] Details: {oom}\n")
        print("[*] Actionable remediation recommendations:")
        print("    1. Set BATCH_SIZE=1 (e.g., export BATCH_SIZE=1)")
        print("    2. Set CONTEXT_LENGTH=1024 or 1280 (export CONTEXT_LENGTH=1280)")
        print("    3. Increase GRADIENT_ACCUMULATION_STEPS (export GRADIENT_ACCUMULATION_STEPS=16)")
        print("    4. If using 16-bit, switch to 4-bit (export PRECISION=4bit)")
        print("    5. Any completed checkpoints remain safely saved in the output directory.")
        print("!" * 65 + "\n")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return False

    duration = time.time() - start_time
    print(f"\n[OK] Training completed in {round(duration / 60, 2)} minutes.")

    # 8. Save Final Model & Metadata
    print(f"[*] Saving final trained adapter weights to: {out_path}")
    model.save_pretrained(str(out_path))
    tokenizer.save_pretrained(str(out_path))

    latest_meta = {
        "status": "completed",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "base_model": config.model_name,
        "adapter_path": str(out_path),
        "duration_minutes": round(duration / 60, 2),
        "precision": config.precision,
        "batch_size": config.batch_size,
        "gradient_accumulation_steps": config.gradient_accumulation_steps,
        "max_steps": config.max_steps,
        "num_epochs": config.num_epochs,
    }
    with open(out_path / "latest_checkpoint.json", "w", encoding="utf-8") as f:
        json.dump(latest_meta, f, indent=2)

    print("[SUCCESS] Ornàment LoRA adapter and metadata saved successfully.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ornàment Multi-Device LoRA Training Pipeline")
    parser.add_argument("--config", default="ai-website-engineer-model/configs/training_config.yaml",
                        help="Path to YAML or JSON configuration file")
    parser.add_argument("--train-dataset", default=None, help="Path to training JSONL dataset")
    parser.add_argument("--val-dataset", default=None, help="Path to validation JSONL dataset")
    parser.add_argument("--output", default=None, help="Output directory for trained adapter")
    parser.add_argument("--resume", "--resume-from-checkpoint", dest="resume", default=None,
                        help="Set to 'latest' or specific checkpoint path to resume training")
    parser.add_argument("--max-steps", type=int, default=None, help="Run for specific number of steps")
    parser.add_argument("--sanity-test", action="store_true", default=False,
                        help="Run a 50-step sanity test before launching full training")
    parser.add_argument("--batch-size", type=int, default=None, help="Per-device batch size")
    parser.add_argument("--grad-accum", type=int, default=None, help="Gradient accumulation steps")
    parser.add_argument("--lr", type=float, default=None, help="Learning rate")
    parser.add_argument("--epochs", type=int, default=None, help="Number of training epochs")
    parser.add_argument("--precision", default=None, choices=["4bit", "8bit", "fp16", "bf16"],
                        help="Model precision")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Validate dataset schema only")

    args = parser.parse_args()

    steps = 50 if args.sanity_test else args.max_steps

    train(
        config_path=Path(args.config) if args.config else None,
        train_dataset_path=Path(args.train_dataset) if args.train_dataset else None,
        val_dataset_path=Path(args.val_dataset) if args.val_dataset else None,
        output_dir=Path(args.output) if args.output else None,
        dry_run=args.dry_run,
        resume_checkpoint=args.resume,
        max_steps=steps,
        batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        epochs=args.epochs,
        precision=args.precision
    )

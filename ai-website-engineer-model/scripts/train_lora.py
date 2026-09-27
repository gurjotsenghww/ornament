#!/usr/bin/env python3
"""
Ornàment 4-Bit QLoRA Fine-Tuning Script.
Optimized for NVIDIA GeForce RTX 3050 Laptop GPU (6GB VRAM, ~5.3GB available).

Loads:
- Base: Qwen/Qwen2.5-Coder-3B-Instruct in 4-bit NF4
- Dataset: ChatML formatted ornament_master_train.jsonl and val.jsonl
- Adapter: LoRA r=16, alpha=32 on all projection layers
- VRAM optimization: gradient checkpointing + paged_adamw_8bit (<4GB VRAM usage)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

def train(
    config_path: Path,
    train_dataset_path: Path,
    val_dataset_path: Path,
    output_dir: Path,
    dry_run: bool = False
):
    print("=========================================================")
    print("      ORNÀMENT AI WEBSITE ENGINEER — MODEL TRAINING")
    print("=========================================================\n")
    print(f"[*] Configuration : {config_path}")
    print(f"[*] Train Dataset : {train_dataset_path}")
    print(f"[*] Val Dataset   : {val_dataset_path}")
    print(f"[*] Output Adapter: {output_dir}\n")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    base_model_name = config.get("base_model", "Qwen/Qwen2.5-Coder-3B-Instruct")
    lora_r = config.get("lora_r", 16)
    lora_alpha = config.get("lora_alpha", 32)
    lora_dropout = config.get("lora_dropout", 0.05)
    target_modules = config.get("target_modules", ["q_proj", "k_proj", "v_proj", "o_proj"])
    hyperparams = config.get("training_hyperparameters", {})

    output_dir.mkdir(parents=True, exist_ok=True)

    if dry_run or os.getenv("ORNAMENT_TRAIN_MOCK") == "1":
        print("[*] Dry run / test mode specified. Validating dataset schema...")
        count = 0
        with open(train_dataset_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    assert "messages" in item, "Missing 'messages' key in dataset item"
                    count += 1
        print(f"[OK] Dataset validated: {count} samples with valid ChatML schema.")
        mock_meta = {
            "status": "ready_for_training",
            "samples": count,
            "base_model": base_model_name,
            "lora_r": lora_r,
            "lora_alpha": lora_alpha,
            "target_modules": target_modules
        }
        with open(output_dir / "training_spec.json", "w", encoding="utf-8") as f:
            json.dump(mock_meta, f, indent=2)
        print(f"[SUCCESS] Training spec written to {output_dir / 'training_spec.json'}")
        return True

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
        print("[*] Install dependencies with:")
        print("    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124")
        print("    pip install transformers peft accelerate bitsandbytes datasets")
        return False

    # Check CUDA device
    if not torch.cuda.is_available():
        print("[!] CUDA is not available. GPU is required for 4-bit QLoRA training.")
        return False

    gpu_name = torch.cuda.get_device_name(0)
    vram_mb = torch.cuda.get_device_properties(0).total_memory / (1024 * 1024)
    print(f"[*] Detected GPU: {gpu_name} ({round(vram_mb, 1)} MB VRAM)")

    # 1. 4-bit Quantization Config (NF4)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16
    )

    print(f"[*] Loading base model tokenizer: {base_model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"[*] Loading base model in 4-bit precision onto GPU...")
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )

    model = prepare_model_for_kbit_training(model)
    model.gradient_checkpointing_enable()

    # 2. Attach LoRA Adapter
    print(f"[*] Initializing LoRA adapter (r={lora_r}, alpha={lora_alpha})...")
    peft_config = LoraConfig(
        r=lora_r,
        lora_alpha=lora_alpha,
        target_modules=target_modules,
        lora_dropout=lora_dropout,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 3. Load Datasets
    print(f"[*] Processing dataset entries into tokenized sequences...")
    def load_jsonl(path: Path) -> List[Dict[str, Any]]:
        entries = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries

    raw_train = load_jsonl(train_dataset_path)
    raw_val = load_jsonl(val_dataset_path)

    def preprocess_function(examples):
        input_ids_list = []
        labels_list = []
        max_seq_length = hyperparams.get("max_seq_length", 2048)

        for msgs in examples["messages"]:
            text = tokenizer.apply_chat_template(
                msgs,
                tokenize=False,
                add_generation_prompt=False
            )
            tokens = tokenizer(
                text,
                truncation=True,
                max_length=max_seq_length,
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

    # 4. Training Arguments
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        per_device_train_batch_size=hyperparams.get("per_device_train_batch_size", 1),
        gradient_accumulation_steps=hyperparams.get("gradient_accumulation_steps", 16),
        learning_rate=hyperparams.get("learning_rate", 2e-4),
        warmup_ratio=hyperparams.get("warmup_ratio", 0.03),
        max_grad_norm=hyperparams.get("max_grad_norm", 0.3),
        num_train_epochs=hyperparams.get("num_train_epochs", 3),
        optim="paged_adamw_8bit",
        fp16=True,
        logging_steps=hyperparams.get("logging_steps", 10),
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        report_to="none"
    )

    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        padding=True,
        return_tensors="pt"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        eval_dataset=val_tokenized,
        data_collator=data_collator
    )

    print("\n[*] Starting training loop on NVIDIA RTX 3050...")
    start_time = time.time()
    trainer.train()
    duration = time.time() - start_time
    print(f"\n[OK] Training completed in {round(duration / 60, 2)} minutes.")

    # 5. Save Final Adapter
    print(f"[*] Saving trained LoRA adapter to: {output_dir}")
    model.save_pretrained(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    print("[SUCCESS] Ornàment LoRA adapter saved successfully.")

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Ornàment Qwen Coder Model")
    parser.add_argument("--config", default="ai-website-engineer-model/configs/lora_config_3b.json")
    parser.add_argument("--train-dataset", default="ai-website-engineer-model/datasets/ornament_master_train.jsonl")
    parser.add_argument("--val-dataset", default="ai-website-engineer-model/datasets/ornament_master_val.jsonl")
    parser.add_argument("--output", default="ai-website-engineer-model/adapters/v0.1.0")
    parser.add_argument("--dry-run", action="store_true", default=False)
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent.parent
    train(
        base / args.config,
        base / args.train_dataset,
        base / args.val_dataset,
        base / args.output,
        dry_run=args.dry_run
    )

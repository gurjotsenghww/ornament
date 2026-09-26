# AI Website Engineer Model Repository (`ai-website-engineer-model`)

This repository is dedicated **strictly** to model version control, dataset manifests, LoRA adapter configurations, training pipelines, and evaluation benchmarks for the **Ornàment** system.

> [!IMPORTANT]
> As specified in the master PRD (Sections 32 & 56), **never** mix website projects with model checkpoints or push massive binary weights directly into ordinary Git history. Model weights are version-controlled via manifests, Git LFS, or model artifact repositories.

## Directory Structure

```text
ai-website-engineer-model/
├── adapters/          # Fine-tuned LoRA adapter weights / export locations
├── configs/           # SFT & DPO training hyperparameters, LoRA configs
├── datasets/          # Dataset manifests (portfolio-v0.1, etc.) and provenance logs
├── docs/              # Training methodology, data governance, safety guidelines
├── evaluation/        # Fixed benchmark test suites & evaluation logs
├── manifests/         # Model release manifests (e.g. model-v0.1.0.json)
└── scripts/           # Dataset synthesis, preprocessing, training, and eval scripts
```

## Release Manifest Schema

Every model release must be recorded in `manifests/` with:
- Model Name & Version (`model-v0.1.0`)
- Base Model (`Qwen/Qwen2.5-Coder-7B-Instruct` or `Qwen3-8B`)
- Training Dataset Version (`portfolio-v0.1.0`)
- Training Method (`LoRA`, rank=16, alpha=32, target_modules)
- Commit SHA
- Hardware specifications (e.g., RTX 3050 Laptop GPU 6GB, offloaded or cloud-trained)
- Benchmark Scores (Code Pass Rate, Route Match, Level 1-4 validation)
- Rollback Target

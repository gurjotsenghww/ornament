# Model Training, Dataset Versioning & LoRA Architecture

## 1. Separate Model Repository (`ai-website-engineer-model`)
As specified in PRD Section 32, model checkpoints and website projects are strictly separated.

```text
ai-website-engineer-model/
├── adapters/          # Exported LoRA weights
├── configs/           # Training hyperparameters (lora_config.json)
├── datasets/          # Trajectory datasets (portfolio-v0.1.0.json)
├── manifests/         # Model release manifests (model-v0.1.0.json)
└── scripts/           # Training, evaluation, and rollback utilities
```

## 2. Dataset Trajectory Format (Section 35)
Data is saved not merely as `prompt -> code`, but as full engineering trajectories:
```json
{
  "task": "Fix broken contact navigation link in Navbar",
  "requirements": "Navbar button must navigate to active /contact route",
  "project_context": "Next.js 14 App Router, Tailwind CSS",
  "plan": "1. Debug Agent scans routes. 2. Identify /contact-us typo. 3. Code Agent modifies href.",
  "files_changed": ["components/Navbar.tsx"],
  "code_changes": [
    {
      "file": "components/Navbar.tsx",
      "action": "modify",
      "diff": "- <Link href=\"/contact-us\">Contact</Link>\n+ <Link href=\"/contact\">Contact</Link>"
    }
  ],
  "tests": ["level4_browser_contact_click"],
  "failures": [{"attempt": 1, "error": "HTTP 404 Not Found at /contact-us"}],
  "fixes": [{"attempt": 2, "fix_applied": "Updated href attribute to /contact", "result": "pass"}],
  "final_status": "passed"
}
```

## 3. Training & Evaluation Commands
```powershell
# Run LoRA training pipeline
python ai-website-engineer-model/scripts/train_lora.py --config configs/lora_config.json --dataset datasets/portfolio-v0.1.0.json --output adapters/v0.1.0

# Run evaluation benchmark
python ai-website-engineer-model/scripts/evaluate_benchmark.py --manifest manifests/model-v0.1.0.json

# Rollback model version
python ai-website-engineer-model/scripts/rollback_model.py --version 0.1.0
```

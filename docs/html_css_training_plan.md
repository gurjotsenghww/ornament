# Ornàment: Model Selection, Hardware Reality, and HTML+CSS Training Architecture

**Target Hardware**: AMD Ryzen 5 7235HS (4C/8T) | NVIDIA RTX 3050 Laptop GPU (6 GB VRAM) | 16 GB System RAM  
**Project**: Ornàment AI Website Engineer  

---

## 1. Model Selection Clarification: Qwen2.5 vs. "Qwen3"

- **Current State of the Art**: Alibaba's official open-source coding model family is **Qwen2.5-Coder** (specifically `Qwen2.5-Coder-7B-Instruct`).
- **"Qwen3" Status**: As of today, Alibaba has not released a "Qwen3" generation. When the specification refers to "Qwen3-8B initially", the industry-standard drop-in equivalent is **`Qwen2.5-Coder-7B-Instruct`** (or 8B-parameter open coder alternatives like Llama-3-8B).
- **Format for Ornàment**: 
  - **Inference**: Official 4-bit GGUF quantization (`qwen2.5-coder-7b-instruct-q4_k_m.gguf` = 4.68 GB).
  - **Weights Location**: `ai-website-engineer-model/weights/`.

---

## 2. Hardware Reality: 6 GB VRAM vs. 7B/8B Training

It is critical to distinguish between **Model Inference (Running the Model)** and **Model Training (Backpropagation & Gradients)**.

### A. Inference (Running Ornàment Locally) — **WORKS ON 6GB VRAM**
- `qwen2.5-coder-7b-instruct-q4_k_m.gguf` occupies **4.68 GB VRAM**.
- Leaves **~1.1 GB VRAM** for the KV-cache and context window.
- The RTX 3050 6GB GPU executes fast local inference at 25–40 tokens/sec.

### B. Training (LoRA Fine-Tuning / Backprop) — **THE VRAM BOTTLENECK**
When training an LLM with PyTorch and Backpropagation, memory is required for:
1. Model weights (even in 4-bit QLoRA = ~4.5 GB)
2. **Gradients** ($\nabla W$) for trainable LoRA matrices
3. **Optimizer States**: AdamW maintains 2 floating-point states (momentum + variance) per parameter. Even 8-bit AdamW requires additional memory.
4. **Activation Checkpoints**: Forward activations stored for the backward pass across sequence lengths (e.g., 2048 to 4096 tokens).

> **Conclusion**: Even with 4-bit QLoRA and sequence truncation, training a 7B or 8B model requires **9 GB to 11 GB of VRAM**. Attempting to backpropagate a 7B model directly on an RTX 3050 6GB GPU triggers an immediate **CUDA Out of Memory (OOM)** crash.

### C. The 3 Viable Paths for Training
1. **Local Training on Laptop GPU (Recommended for 100% Local Development)**:
   - Train **`Qwen2.5-Coder-1.5B`** (1.12 GB) or **`Qwen2.5-Coder-3B`** (1.93 GB) with 4-bit QLoRA.
   - Fits comfortably in **3.2 GB – 4.5 GB VRAM** on your RTX 3050!
   - Ideal for rapid iteration, custom HTML/Tailwind styling adapters, and testing the LoRA pipeline.
2. **CPU-Offloaded Optimizer Training**:
   - Keep model weights on GPU, but offload AdamW optimizer states into your 16GB system RAM using Hugging Face Accelerate / `paged_adamw_8bit`.
3. **Free Cloud GPU for 7B/8B Training**:
   - Run `train_lora.py` on a free **Google Colab T4 (16 GB VRAM)** or RunPod/Modal instance.
   - The resulting LoRA adapter (`adapter_model.safetensors`) is tiny (**~30 MB**).
   - Download the adapter back to your laptop to merge and run inference on your RTX 3050!

---

## 3. Why We Train HTML and CSS Together (Never HTML Alone)

Training HTML in isolation without CSS produces:
- Naked, unstyled document tags (`<div>`, `<p>`, `<h1>`) with zero visual structure.
- In modern web engineering, **HTML and utility CSS (Tailwind) are inextricably linked**:
  - Grid & Flex layouts (`grid grid-cols-1 md:grid-cols-3 gap-6`)
  - Dark mode surfaces (`bg-[#09090b] text-zinc-100 border border-zinc-800`)
  - Responsive breakpoints (`hidden md:flex`, `text-sm sm:text-base`)
  - Glassmorphism & Micro-animations (`backdrop-blur-md bg-zinc-950/80 hover:border-zinc-700`)
  - Semantic ARIA attributes paired with visible focus states (`focus:ring-2 focus:ring-indigo-500`)
- **Decision**: All Ornàment training datasets pair semantic HTML5 with modern Tailwind CSS and interactive React/Next.js component structure.

---

## 4. Sourcing the World's Best Website Designs

To achieve visual aesthetics comparable to top design agencies and products (e.g., Linear, Vercel, Stripe), Ornàment curates training data from:

### 1. Premier Open-Source Component Systems
- **Shadcn UI & Radix Primitives**: The modern gold standard for SaaS, clean typography, dropdowns, dialogs, and accessible forms.
- **Tailwind UI Open Patterns & HyperUI**: High-conversion landing page layouts, pricing grids, testimonials, and e-commerce catalogs.
- **Cruip Open Templates**: Award-winning dark-mode SaaS, AI startups, developer landing pages, and bento grids.
- **DaisyUI & Flowbite**: Production-grade data tables, stat cards, and interactive widgets.
- **HTML5 UP (Creative Commons)**: Responsive, clean HTML5/CSS3 templates for portfolios and creative agency showcases.

### 2. Multi-Turn Autonomous Engineering Trajectories
An AI Website Engineer cannot just emit static HTML. It must learn **agentic software engineering**:
- **Trajectory Type 1**: User Prompt $\to$ Architecture Plan $\to$ Clean HTML5/Tailwind Component.
- **Trajectory Type 2**: Bug Diagnosis $\to$ Minimal 1-File Patch $\to$ Passing Playwright Verification.
- **Trajectory Type 3**: Accessibility Refactor $\to$ Adding ARIA landmarks, `alt` attributes, semantic heading levels without breaking CSS styling.

Our script `ai-website-engineer-model/scripts/generate_dataset.py` generates 100+ multi-turn trajectories with code, diffs, and test assertions.

---

## 5. Execution Commands Quick Reference

```bash
# 1. Download official Qwen Coder model (7B 4-bit GGUF for inference, or 1.5B/3B for local training)
python -m ornament.cli.main download-model --model qwen2.5-coder-7b-q4
python -m ornament.cli.main download-model --model qwen2.5-coder-1.5b-q4

# 2. Curate high-design HTML+CSS dataset
python ai-website-engineer-model/scripts/curate_dataset.py

# 3. Generate multi-turn synthetic engineering trajectories
python ai-website-engineer-model/scripts/generate_dataset.py --count 100

# 4. Launch Ornàment Web Studio & Live Preview
python -m ornament.cli.main serve --port 5050
```

#!/usr/bin/env python3
"""
Hardware & GPU Diagnostic Utility for Ornàment AI.
Auto-detects PyTorch, CUDA, compute capabilities, and memory limits across:
- Local Consumer GPUs (RTX 3050, RTX 4050, etc.)
- Google Colab (Tesla T4, V100, A100)
- Enterprise Clusters (A100, H100, DGX)
"""

import sys
import platform

def check_gpu():
    print("=" * 60)
    print("       ORNÀMENT HARDWARE & GPU DIAGNOSTIC TELEMETRY")
    print("=" * 60)
    print(f"[*] Python Version       : {platform.python_version()} ({platform.system()} {platform.machine()})")

    try:
        import torch
    except ImportError:
        print("[!] ERROR: PyTorch is not installed in this environment.")
        sys.exit(1)

    print(f"[*] PyTorch Version      : {torch.__version__}")
    print(f"[*] CUDA Available       : {torch.cuda.is_available()}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Selected Device      : {device}")

    if not torch.cuda.is_available():
        print("\n[!] WARNING: No CUDA GPU detected. Training will run on CPU (NOT RECOMMENDED).")
        return False

    cuda_version = torch.version.cuda or "N/A"
    cudnn_version = torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else "N/A"
    device_count = torch.cuda.device_count()

    print(f"[*] CUDA Version         : {cuda_version}")
    print(f"[*] cuDNN Version        : {cudnn_version}")
    print(f"[*] GPU Device Count     : {device_count}")

    for idx in range(device_count):
        props = torch.cuda.get_device_properties(idx)
        total_vram_gb = round(props.total_memory / (1024 ** 3), 2)
        allocated_gb = round(torch.cuda.memory_allocated(idx) / (1024 ** 3), 2)
        reserved_gb = round(torch.cuda.memory_reserved(idx) / (1024 ** 3), 2)
        free_vram_gb = round(total_vram_gb - allocated_gb, 2)
        compute_cap = f"{props.major}.{props.minor}"

        print(f"\n--- GPU [{idx}]: {props.name} ---")
        print(f"    Compute Capability   : {compute_cap}")
        print(f"    Total VRAM           : {total_vram_gb} GB")
        print(f"    Allocated VRAM       : {allocated_gb} GB")
        print(f"    Reserved VRAM        : {reserved_gb} GB")
        print(f"    Usable Free VRAM     : ~{free_vram_gb} GB")
        print(f"    BF16 Supported       : {torch.cuda.is_bf16_supported()}")
        print(f"    FP16 Supported       : True")

        # Hardware profiling recommendation
        if total_vram_gb < 8.0:
            tier = "Consumer Entry (e.g. RTX 3050/4050 6GB)"
            rec = "4-bit QLoRA (NF4), batch_size=1, gradient_accumulation=16, max_seq_length=1280"
        elif total_vram_gb < 20.0:
            tier = "Cloud Standard (e.g. Tesla T4 16GB)"
            rec = "4-bit QLoRA or 8-bit LoRA, batch_size=2, gradient_accumulation=8, max_seq_length=2048"
        else:
            tier = "Enterprise / Cloud High-End (e.g. A100 40GB/80GB)"
            rec = "Full 16-bit LoRA / BF16, batch_size=4-8, gradient_accumulation=4, max_seq_length=4096+"

        print(f"    Hardware Tier Profile: {tier}")
        print(f"    Recommended Strategy : {rec}")

    # Small sanity check computation
    try:
        x = torch.randn(4096, 4096, device="cuda")
        y = x @ x
        del x, y
        torch.cuda.empty_cache()
        print("\n[SUCCESS] GPU matrix multiplication test passed.")
        return True
    except Exception as e:
        print(f"\n[!] GPU Compute Self-Test Failed: {e}")
        return False

if __name__ == "__main__":
    success = check_gpu()
    sys.exit(0 if success else 1)

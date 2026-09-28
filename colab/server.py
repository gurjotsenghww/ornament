"""
Ornàment Cloud Dual-Model Server (Google Colab T4 Edition)
=========================================================
Flagship Models:
1. Qwen 2.5 Coder 7B Instruct (Flagship 7B/8B Coding Engine)
2. Qwen2-VL 2B Instruct (Deep Visual & UI Mockup Analysis)

Exposed automatically via Cloudflare HTTPS Tunnel.
"""
import os
import sys
import gc
import re
import json
import base64
import io
import time
import subprocess
import threading
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

app = FastAPI(title="Ornàment Cloud Engine (7B Coder + Vision)", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model holders
CODER_MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
VL_MODEL_NAME = "Qwen/Qwen2-VL-2B-Instruct"

coder_tokenizer = None
coder_model = None
vl_processor = None
vl_model = None

def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

def load_models():
    global coder_tokenizer, coder_model, vl_processor, vl_model
    print("=" * 60)
    print("LOADING ORNÀMENT CLOUD DUAL-MODEL ENGINE (7B CODER + VISION)")
    print("=" * 60)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    # 1. Load Qwen 2.5 Coder 7B
    print(f"[1/2] Loading {CODER_MODEL_NAME} in 4-bit NF4...")
    coder_tokenizer = AutoTokenizer.from_pretrained(CODER_MODEL_NAME)
    coder_model = AutoModelForCausalLM.from_pretrained(
        CODER_MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto"
    )
    vram_coder = torch.cuda.memory_allocated(0) / (1024 ** 3)
    print(f"  [OK] Coder 7B loaded! VRAM used: {vram_coder:.2f} GB")

    # 2. Load Qwen2-VL 2B
    print(f"[2/2] Loading {VL_MODEL_NAME} in 4-bit NF4...")
    vl_processor = AutoProcessor.from_pretrained(VL_MODEL_NAME)
    vl_model = Qwen2VLForConditionalGeneration.from_pretrained(
        VL_MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto"
    )
    vram_total = torch.cuda.memory_allocated(0) / (1024 ** 3)
    print(f"  [OK] Qwen2-VL loaded! Total VRAM used: {vram_total:.2f} GB")
    print(f"  [OK] Free VRAM headroom: {14.56 - vram_total:.2f} GB")
    print("=" * 60)

# Request schemas
class GenerateSiteRequest(BaseModel):
    prompt: str
    existing_files: Optional[Dict[str, str]] = None
    fast_mode: Optional[bool] = False
    max_tokens: Optional[int] = 1600
    temperature: Optional[float] = 0.3

class AnalyzeImageRequest(BaseModel):
    image_base64: str
    prompt: Optional[str] = "Analyze this web UI / application screenshot thoroughly. Extract the visual hierarchy, 60-30-10 color palette, typography styles, layout grid structure, and interactive components."

class VisionToSiteRequest(BaseModel):
    image_base64: str
    prompt: Optional[str] = "Build a complete, responsive, modern website that faithfully replicates and enhances this design."
    existing_files: Optional[Dict[str, str]] = None

@app.get("/health")
def health():
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"
    allocated = round(torch.cuda.memory_allocated(0) / (1024 ** 3), 2) if torch.cuda.is_available() else 0
    total = round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 2) if torch.cuda.is_available() else 0
    return {
        "status": "healthy",
        "engine": "Ornàment Cloud Engine",
        "gpu": gpu_name,
        "vram_used_gb": allocated,
        "vram_total_gb": total,
        "coder_model": CODER_MODEL_NAME,
        "vision_model": VL_MODEL_NAME,
        "dual_model_ready": coder_model is not None and vl_model is not None
    }

def extract_code_blocks(text: str) -> Dict[str, str]:
    files = {}
    
    # 1. Look for explicit filenames in fences: ```html index.html or ```css style.css
    pattern = r'```(?:([a-zA-Z0-9_-]+)(?:\s+([a-zA-Z0-9_\-\.]+))?)?\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    html_found = None
    css_found = None
    js_found = None
    
    for lang, fname, code in matches:
        lang = lang.lower().strip()
        fname = fname.strip() if fname else ""
        code = code.strip()
        if not code:
            continue
            
        if fname:
            files[fname] = code
            if fname.endswith(".html"): html_found = code
            elif fname.endswith(".css"): css_found = code
            elif fname.endswith(".js"): js_found = code
        elif lang in ("html", "htm") and not html_found:
            html_found = code
            files["index.html"] = code
        elif lang in ("css", "style") and not css_found:
            css_found = code
            files["style.css"] = code
        elif lang in ("javascript", "js") and not js_found:
            js_found = code
            files["app.js"] = code

    # Fallback search if no fences matched
    if "index.html" not in files:
        html_m = re.search(r'(<!DOCTYPE\s+html[\s\S]*?</html>)', text, re.IGNORECASE)
        if html_m:
            files["index.html"] = html_m.group(1).strip()

    return files

@app.post("/api/generate-site")
def generate_site(req: GenerateSiteRequest):
    global coder_model, coder_tokenizer
    if coder_model is None:
        raise HTTPException(status_code=503, detail="Coder model not loaded.")

    system_prompt = (
        "You are Ornàment 2.5 Coder (Neural 7B), an elite autonomous staff software engineer. "
        "When asked to create or update a website, write clean, modern, responsive code with bespoke styling, "
        "fluid layouts, accessible elements, and dynamic interactions. "
        "First, output 5 to 6 concise technical execution steps tailored specifically to this request under:\n"
        "### Execution Steps:\n"
        "1. <Specific step 1 tailored to the requested components & data>\n"
        "2. <Specific step 2 tailored to HTML semantic structure>\n"
        "3. <Specific step 3 tailored to CSS layout & color tokens>\n"
        "4. <Specific step 4 tailored to JavaScript logic & events>\n"
        "5. <Specific step 5 tailored to responsive breakpoints & accessibility>\n\n"
        "Then provide your solution across clear markdown code blocks with filenames, e.g.:\n"
        "```html index.html\n<!DOCTYPE html>...\n```\n"
        "```css style.css\n/* CSS styling */\n```\n"
        "```javascript app.js\n// JavaScript logic\n```"
    )

    user_content = req.prompt
    if req.existing_files and len(req.existing_files) > 0:
        context_str = "CURRENT PROJECT FILES (apply changes directly to this code):\n"
        for name, content in req.existing_files.items():
            context_str += f"=== {name} ===\n{content[:2000]}\n\n"
        user_content = f"{context_str}\nUSER REQUEST: {req.prompt}\nUpdate or regenerate the files to satisfy the request."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]

    prompt_text = coder_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = coder_tokenizer([prompt_text], return_tensors="pt").to("cuda")

    max_new_tokens = 900 if req.fast_mode else req.max_tokens
    temp = 0.1 if req.fast_mode else req.temperature

    start_time = time.time()
    with torch.no_grad():
        generated_ids = coder_model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temp,
            do_sample=(temp > 0.0),
            top_p=0.9 if temp > 0.0 else None,
            pad_token_id=coder_tokenizer.eos_token_id
        )

    output_ids = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    raw_response = coder_tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
    elapsed = round(time.time() - start_time, 2)

    extracted_files = extract_code_blocks(raw_response)

    # Extract dynamic execution steps from raw response
    steps = []
    plan_m = re.search(r"###\s*(?:Execution\s*Steps|Plan|Engineering\s*Steps|Steps)[\s\S]*?(?=```|$)", raw_response, re.IGNORECASE)
    if plan_m:
        for line in plan_m.group(0).split("\n"):
            line = line.strip()
            m = re.match(r"^\d+[\.\)]\s*(?:\*\*(.*?)\*\*:?\s*)?(.*)$", line)
            if m:
                t = (m.group(1) or "").strip()
                s = (m.group(2) or "").strip()
                step_str = f"{t}: {s}".strip(" :") if t and s else (t or s)
                step_str = re.sub(r"[*`#_]+", "", step_str).strip()
                if step_str and not step_str.lower().startswith("execution step"):
                    steps.append(step_str)
    
    if len(steps) < 3:
        steps = [
            f"Synthesizing bespoke architecture for {req.prompt[:32]}",
            "Scaffolding semantic HTML5 layout & accessible landmarks",
            "Composing responsive CSS styling & color harmony system",
            "Wiring client-side JavaScript interactions & state management",
            "Validating responsive breakpoints across viewports",
            "Bundling production-ready output files"
        ]
    
    # If css/js were embedded in html, extract them if needed or provide standard bundle
    if "index.html" in extracted_files and "style.css" not in extracted_files:
        style_match = re.search(r'<style>([\s\S]*?)</style>', extracted_files["index.html"], re.IGNORECASE)
        if style_match:
            extracted_files["style.css"] = style_match.group(1).strip()
            
    if "index.html" in extracted_files and "app.js" not in extracted_files:
        script_match = re.search(r'<script>([\s\S]*?)</script>', extracted_files["index.html"], re.IGNORECASE)
        if script_match:
            extracted_files["app.js"] = script_match.group(1).strip()

    file_list = []
    for fname, content in extracted_files.items():
        ext = fname.split(".")[-1].lower() if "." in fname else "txt"
        file_list.append({
            "name": fname,
            "type": ext,
            "content": content,
            "size": len(content)
        })

    return {
        "success": True,
        "elapsed_seconds": elapsed,
        "model": CODER_MODEL_NAME,
        "files": file_list,
        "steps": steps,
        "raw_text": raw_response
    }

def decode_base64_image(b64_str: str) -> Image.Image:
    if "," in b64_str:
        b64_str = b64_str.split(",", 1)[1]
    img_bytes = base64.b64decode(b64_str)
    return Image.open(io.BytesIO(img_bytes)).convert("RGB")

@app.post("/api/analyze-image")
def analyze_image(req: AnalyzeImageRequest):
    global vl_model, vl_processor
    if vl_model is None:
        raise HTTPException(status_code=503, detail="Vision model not loaded.")

    image = decode_base64_image(req.image_base64)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": req.prompt}
            ]
        }
    ]

    text_prompt = vl_processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = vl_processor(
        text=[text_prompt],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt"
    ).to("cuda")

    start_time = time.time()
    with torch.no_grad():
        generated_ids = vl_model.generate(**inputs, max_new_tokens=800, temperature=0.2)
        
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    analysis = vl_processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )[0]
    elapsed = round(time.time() - start_time, 2)

    return {
        "success": True,
        "elapsed_seconds": elapsed,
        "analysis": analysis,
        "model": VL_MODEL_NAME
    }

@app.post("/api/vision-to-site")
def vision_to_site(req: VisionToSiteRequest):
    # Step 1: Analyze image using Qwen2-VL
    analyze_req = AnalyzeImageRequest(
        image_base64=req.image_base64,
        prompt="Analyze this visual design in high detail: describe all sections, layout components, color scheme (hex codes), typography, buttons, cards, forms, and visual hierarchy."
    )
    analysis_res = analyze_image(analyze_req)
    analysis_text = analysis_res["analysis"]

    # Step 2: Synthesize full website bundle using Qwen 2.5 Coder 7B
    synth_prompt = (
        f"Based on the following visual analysis of an uploaded mockup/screenshot, create a complete, "
        f"stunning, fully-responsive website bundle (index.html, style.css, app.js):\n\n"
        f"VISUAL ANALYSIS & SPECIFICATIONS:\n{analysis_text}\n\n"
        f"USER GOAL: {req.prompt}\n\n"
        f"Deliver production-quality HTML, bespoke CSS styling, and dynamic JavaScript."
    )

    gen_req = GenerateSiteRequest(
        prompt=synth_prompt,
        existing_files=req.existing_files,
        fast_mode=False,
        max_tokens=2200
    )
    site_res = generate_site(gen_req)

    return {
        "success": True,
        "analysis": analysis_text,
        "files": site_res["files"],
        "elapsed_seconds": round(analysis_res["elapsed_seconds"] + site_res["elapsed_seconds"], 2)
    }

def start_tunnel():
    print("[*] Starting Cloudflare tunnel...")
    if not os.path.exists("/tmp/cloudflared"):
        subprocess.run(["curl", "-sL", "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", "-o", "/tmp/cloudflared"], check=True)
        subprocess.run(["chmod", "+x", "/tmp/cloudflared"], check=True)

    proc = subprocess.Popen(["/tmp/cloudflared", "tunnel", "--url", "http://127.0.0.1:8000"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    
    tunnel_url = None
    start = time.time()
    while time.time() - start < 20:
        line = proc.stderr.readline()
        if not line:
            time.sleep(0.2)
            continue
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            tunnel_url = match.group(0)
            break

    if tunnel_url:
        print("\n" + "=" * 65)
        print("ORNÀMENT CLOUD DUAL-MODEL ENGINE READY!")
        print(f"PUBLIC CLOUD TUNNEL URL: {tunnel_url}")
        print("=" * 65 + "\n")
        with open("/tmp/ornament_tunnel_url.txt", "w") as f:
            f.write(tunnel_url)
    else:
        print("[!] Cloudflare tunnel did not provide URL in time.")

if __name__ == "__main__":
    import uvicorn
    # 1. Load models into GPU
    load_models()
    
    # 2. Start Cloudflare tunnel in background thread
    tunnel_thread = threading.Thread(target=start_tunnel, daemon=True)
    tunnel_thread.start()

    # 3. Start FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)

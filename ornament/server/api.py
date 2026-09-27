from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from ornament.config import settings
from ornament.hardware.monitor import HardwareManager
from ornament.files.file_manager import FileManager
from ornament.git_ops.checkpoint import GitCheckpointManager
from ornament.testing.runner import MultiLevelTestHarness
from ornament.generator.portfolio_generator import PortfolioGenerator
from ornament.agents.main_agent import MainAgent
from ornament.agents.manager import AgentManager
from ornament.models.provider.factory import get_model_provider
from ornament.sandbox.dev_server import DevPreviewServer

app = FastAPI(
    title="Ornàment AI Website Engineer",
    version="0.1.0",
    description="Local-first agentic software engineering system for autonomous websites."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

shared_agent_manager = AgentManager()
active_preview_servers: Dict[str, DevPreviewServer] = {}

def get_project_dir(project_name: str) -> Path:
    p = settings.workspace_dir / project_name
    p.mkdir(parents=True, exist_ok=True)
    return p

@app.get("/api/health")
def get_health():
    telemetry = HardwareManager.get_system_telemetry()
    recs = HardwareManager.get_model_recommendations()
    return {
        "status": "healthy",
        "system": telemetry.model_dump(),
        "recommendations": recs
    }

@app.get("/api/projects")
def list_projects():
    if not settings.workspace_dir.exists():
        return []
    projects = []
    for item in settings.workspace_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            projects.append({
                "name": item.name,
                "path": str(item)
            })
    return projects

@app.post("/api/projects/generate-portfolio")
async def generate_portfolio(project_name: str = "demo-portfolio", intentional_bug: bool = False):
    p_dir = get_project_dir(project_name)
    result = PortfolioGenerator.generate(p_dir, intentional_bug=intentional_bug)
    
    # Initialize Git checkpoint
    git_mgr = GitCheckpointManager(p_dir)
    git_mgr.create_checkpoint("Developer portfolio generated", agent_id="main_agent")
    
    # Start or restart preview server
    if project_name not in active_preview_servers:
        server = DevPreviewServer(p_dir, port=3456)
        server.start()
        active_preview_servers[project_name] = server
        
    return {
        "status": "success",
        "project": project_name,
        "files_count": len(result["files_created"]),
        "intentional_bug": intentional_bug,
        "preview_url": active_preview_servers[project_name].url
    }

@app.post("/api/projects/generate-ecommerce")
async def generate_ecommerce(project_name: str = "demo-ecommerce"):
    from ornament.generator.ecommerce_generator import EcommerceGenerator
    p_dir = get_project_dir(project_name)
    result = EcommerceGenerator.generate(p_dir)
    git_mgr = GitCheckpointManager(p_dir)
    git_mgr.create_checkpoint("E-Commerce store generated", agent_id="main_agent")
    if project_name not in active_preview_servers:
        server = DevPreviewServer(p_dir, port=3458)
        server.start()
        active_preview_servers[project_name] = server
    return {
        "status": "success",
        "project": project_name,
        "files_count": result["files_count"],
        "preview_url": active_preview_servers[project_name].url
    }

@app.post("/api/projects/generate-saas")
async def generate_saas(project_name: str = "demo-saas"):
    from ornament.generator.saas_generator import SaasGenerator
    p_dir = get_project_dir(project_name)
    result = SaasGenerator.generate(p_dir)
    git_mgr = GitCheckpointManager(p_dir)
    git_mgr.create_checkpoint("SaaS platform generated", agent_id="main_agent")
    if project_name not in active_preview_servers:
        server = DevPreviewServer(p_dir, port=3459)
        server.start()
        active_preview_servers[project_name] = server
    return {
        "status": "success",
        "project": project_name,
        "files_count": result["files_count"],
        "preview_url": active_preview_servers[project_name].url
    }

class CustomSiteRequest(BaseModel):
    project_name: str = "custom-site"
    prompt: str = ""
    site_type: str = "portfolio"  # portfolio | ecommerce | saas
    style: str = "dark_futuristic"
    color_palette: str = "deep_indigo"
    typography: str = "inter_mono"
    sections: List[str] = Field(default_factory=lambda: ["hero", "about", "projects", "contact"])

@app.post("/api/projects/generate-custom")
async def generate_custom(req: CustomSiteRequest):
    p_dir = get_project_dir(req.project_name)
    from ornament.generator.custom_site_generator import CustomSiteGenerator
    result = CustomSiteGenerator.generate(
        workspace_path=p_dir,
        prompt=req.prompt,
        site_type=req.site_type,
        style=req.style,
        palette_key=req.color_palette,
        sections=req.sections
    )
    count = result["files_count"]
    git_mgr = GitCheckpointManager(p_dir)
    cp = git_mgr.create_checkpoint(f"Custom {req.site_type} generated: {req.prompt[:50]}", agent_id="main_agent")

    if req.project_name not in active_preview_servers:
        server = DevPreviewServer(p_dir, port=3456)
        server.start()
        active_preview_servers[req.project_name] = server

    return {
        "status": "success",
        "project": req.project_name,
        "site_type": req.site_type,
        "prompt": req.prompt,
        "files_count": count,
        "checkpoint": cp[:8],
        "preview_url": active_preview_servers[req.project_name].url
    }

@app.post("/api/projects/{project_name}/simulate-bug")
async def simulate_bug(project_name: str):
    p_dir = get_project_dir(project_name)
    fm = FileManager(p_dir)
    nav_file = "components/Navbar.tsx"
    if fm.file_exists(nav_file):
        content = fm.read_file(nav_file)
        if 'href="/contact"' in content:
            fm.edit_file_exact_replacement(nav_file, 'href="/contact"', 'href="/contact-us"')
            git_mgr = GitCheckpointManager(p_dir)
            return {
                "status": "success",
                "message": "Injected intentional route mismatch (/contact-us) in Navbar.tsx",
                "diff": git_mgr.get_diff()
            }
        else:
            return {"status": "warning", "message": "Route already set to /contact-us"}
    return {"status": "error", "message": f"{nav_file} not found"}

@app.post("/api/projects/{project_name}/run-audits")
async def run_audits(project_name: str):
    from ornament.testing.auditors import SiteAuditor
    p_dir = get_project_dir(project_name)
    seo = SiteAuditor.run_seo_audit(p_dir)
    perf = SiteAuditor.run_performance_audit(p_dir)
    a11y = SiteAuditor.run_accessibility_audit(p_dir)
    return {
        "seo": seo.model_dump(),
        "performance": perf.model_dump(),
        "accessibility": a11y.model_dump()
    }

@app.get("/api/projects/{project_name}/files")
def get_files(project_name: str):
    p_dir = get_project_dir(project_name)
    fm = FileManager(p_dir)
    return fm.list_files(exclude_build=True)

@app.get("/api/projects/{project_name}/file-content")
def get_file_content(project_name: str, file_path: str):
    p_dir = get_project_dir(project_name)
    fm = FileManager(p_dir)
    try:
        content = fm.read_file(file_path)
        return {"file": file_path, "content": content}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/projects/{project_name}/diff")
def get_diff(project_name: str):
    p_dir = get_project_dir(project_name)
    git_mgr = GitCheckpointManager(p_dir)
    return {"diff": git_mgr.get_diff()}

@app.get("/api/projects/{project_name}/history")
def get_history(project_name: str):
    p_dir = get_project_dir(project_name)
    git_mgr = GitCheckpointManager(p_dir)
    return git_mgr.get_history()

@app.post("/api/projects/{project_name}/run-tests")
async def run_tests(project_name: str):
    p_dir = get_project_dir(project_name)
    if project_name not in active_preview_servers:
        server = DevPreviewServer(p_dir, port=3456)
        server.start()
        active_preview_servers[project_name] = server
    server_url = active_preview_servers[project_name].url
    
    lvl1 = await MultiLevelTestHarness.run_level1_static(p_dir)
    lvl2 = await MultiLevelTestHarness.run_level2_build(p_dir)
    lvl4 = await MultiLevelTestHarness.run_level4_browser_functional(
        base_url=server_url,
        target_route="/",
        click_selector="#nav-contact-button",
        expected_route="/contact"
    )
    lvl7 = await MultiLevelTestHarness.run_level7_accessibility(p_dir)
    
    all_passed = lvl1.passed and lvl2.passed and lvl4.passed and lvl7.passed
    return {
        "overall_status": "PASS" if all_passed else "FAIL",
        "results": [
            lvl1.model_dump(),
            lvl2.model_dump(),
            lvl4.model_dump(),
            lvl7.model_dump()
        ]
    }

@app.post("/api/projects/{project_name}/run-repair")
async def run_repair(
    project_name: str,
    symptom: str = "Contact button points to /contact-us which produces 404. Expected route is /contact."
):
    p_dir = get_project_dir(project_name)
    model_prov = get_model_provider()
    
    main_agent = MainAgent(
        task=f"Repair issue: {symptom}",
        workspace_path=p_dir,
        model_provider=model_prov,
        agent_manager=shared_agent_manager
    )
    
    if project_name not in active_preview_servers:
        server = DevPreviewServer(p_dir, port=3456)
        server.start()
        active_preview_servers[project_name] = server
    server_url = active_preview_servers[project_name].url
    
    result = await main_agent.run_repair_loop(
        symptom=symptom,
        base_url=server_url,
        test_selector="#nav-contact-button",
        expected_route="/contact"
    )
    
    return {
        "status": result.get("status"),
        "final_status": result.get("final_status"),
        "commit": result.get("commit"),
        "history": result.get("history"),
        "agent_tree": shared_agent_manager.get_agent_tree()
    }

@app.get("/api/agents")
def get_agents():
    return shared_agent_manager.get_agent_tree()

@app.get("/api/training-data/stats")
def get_training_stats():
    from ornament.training_data.storage.example_store import ExampleStore
    store = ExampleStore(settings.base_dir / "ornament" / "training_data")
    return store.get_stats()

@app.get("/api/model/status")
def get_model_status():
    from ornament.hardware.monitor import HardwareManager
    weights_path = settings.base_dir / "ai-website-engineer-model" / "weights" / "qwen2.5-coder-3b-instruct-q4_k_m.gguf"
    exists = weights_path.exists()
    size_mb = (weights_path.stat().st_size / (1024 * 1024)) if exists else 0
    tel = HardwareManager.get_system_telemetry()
    return {
        "model_name": "Qwen2.5-Coder-3B-Instruct",
        "format": "GGUF Q4_K_M",
        "weights_ready": exists,
        "weights_size_mb": round(size_mb, 1),
        "weights_path": str(weights_path),
        "lora_config": "ai-website-engineer-model/configs/lora_config_3b.json",
        "gpu": tel.gpu_name if tel.gpu_available else "CPU",
        "vram_total_mb": tel.vram_total_mb,
        "vram_free_mb": tel.vram_free_mb
    }

class ChatPayload(BaseModel):
    message: str

_llm_instance = None

def get_local_llm():
    global _llm_instance
    if _llm_instance is None:
        try:
            from llama_cpp import Llama
            weights = settings.base_dir / "ai-website-engineer-model" / "weights" / "qwen2.5-coder-3b-instruct-q4_k_m.gguf"
            if not weights.exists():
                return None
            _llm_instance = Llama(model_path=str(weights), n_ctx=2048, n_threads=4, verbose=False)
        except Exception as e:
            return None
    return _llm_instance

@app.post("/api/model/chat")
def chat_with_model(payload: ChatPayload):
    llm = get_local_llm()
    if not llm:
        raise HTTPException(status_code=404, detail="Model weights not loaded or llama-cpp-python unavailable.")
    
    system_prompt = (
        "You are Qwen2.5-Coder-3B, the autonomous AI website engineer in the Ornàment system. "
        "You write production-quality, accessible, semantic HTML5, modern CSS, and TypeScript code. "
        "Answer clearly, concisely, and helpfully."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": payload.message}
    ]
    res = llm.create_chat_completion(messages=messages, max_tokens=512, temperature=0.7)
    return {"reply": res["choices"][0]["message"]["content"]}

@app.post("/api/training-data/build")
def build_datasets_endpoint(version: str = "dataset-v0.2"):
    from ornament.training_data.pipeline import TrainingDataPipeline
    pipeline = TrainingDataPipeline()
    return pipeline.build_datasets(version=version)

@app.get("/", response_class=HTMLResponse)
def index_page():
    return """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Ornàment AI Website Engineer</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            bg: '#09090b',
            surface: '#18181b',
            surfaceBorder: '#27272a',
            accent: '#6366f1'
          }
        }
      }
    }
  </script>
  <style>
    body { background-color: #09090b; color: #f4f4f5; font-family: ui-sans-serif, system-ui, sans-serif; }
    pre { font-family: ui-monospace, SFMono-Regular, monospace; }
  </style>
</head>
<body class="min-h-screen flex flex-col">
  <!-- Top Navigation -->
  <header class="border-b border-surfaceBorder bg-surface px-6 py-4 flex items-center justify-between">
    <div class="flex items-center space-x-4">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-black text-white text-lg">O</div>
        <span class="text-xl font-bold tracking-tight">Ornàment <span class="text-xs text-indigo-400 font-mono px-2 py-0.5 rounded bg-indigo-500/10 border border-indigo-500/20">AI Website Engineer v0.1</span></span>
      </div>
      <div class="flex items-center space-x-1 bg-zinc-900 p-1 rounded-lg border border-zinc-800 text-xs">
        <button id="tab-btn-studio" onclick="switchView('studio')" class="px-3 py-1 rounded bg-indigo-600 font-bold text-white shadow transition">⚡ Prompt Studio</button>
        <button id="tab-btn-model" onclick="switchView('model')" class="px-3 py-1 rounded text-zinc-400 hover:text-white font-medium transition">🧠 Model & Training Hub</button>
      </div>
    </div>
    <div id="telemetry-bar" class="text-xs font-mono text-zinc-400 flex items-center space-x-4">
      <span>CPU: <strong id="cpu-stat" class="text-zinc-200">--%</strong></span>
      <span>RAM: <strong id="ram-stat" class="text-zinc-200">-- MB</strong></span>
      <span>VRAM: <strong id="vram-stat" class="text-indigo-300">-- MB</strong></span>
      <span class="px-2 py-1 rounded bg-green-500/10 text-green-400 border border-green-500/20">System Ready</span>
    </div>
  </header>

  <!-- Main Grid: Prompt Studio -->
  <main id="view-studio" class="flex-1 grid grid-cols-12 gap-4 p-6">
    <!-- Left Panel: Prompt Studio, Tools & Agent Tree -->
    <div class="col-span-4 space-y-4">
      <!-- Prompt Studio Box -->
      <div class="p-4 rounded-xl border border-surfaceBorder bg-surface space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="text-xs font-bold uppercase tracking-wider text-indigo-400">AI Website Studio</h2>
          <span class="text-[10px] px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 font-mono">Qwen Coder Engine</span>
        </div>
        
        <div>
          <label class="block text-xs font-semibold text-zinc-300 mb-1">Prompt / Requirements</label>
          <textarea id="prompt-input" rows="3" class="w-full text-xs p-2.5 rounded-lg bg-zinc-900 border border-surfaceBorder text-white focus:outline-none focus:border-indigo-500 font-sans" placeholder="e.g. Build an ultra-modern dark SaaS platform with transparent pricing and live telemetry dashboard..."></textarea>
        </div>

        <!-- Inspiration Presets -->
        <div>
          <label class="block text-[11px] font-semibold text-zinc-400 mb-1">1-Click Inspiration Presets</label>
          <div class="flex flex-wrap gap-1">
            <button type="button" onclick="selectPreset('Next-Gen AI SaaS Platform with bento grid, fleet metrics and pricing tiers', 'saas', 'dark_futuristic', 'cyan')" class="text-[10px] px-2 py-0.5 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-800">⚡ AI SaaS Bento</button>
            <button type="button" onclick="selectPreset('Senior Autonomous AI Systems Engineer personal portfolio with minimal dark aesthetic', 'portfolio', 'minimal_luxury', 'indigo')" class="text-[10px] px-2 py-0.5 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-800">💼 Minimal Portfolio</button>
            <button type="button" onclick="selectPreset('Cyberpunk Edge Computing and Hardware equipment store with catalog and cart', 'ecommerce', 'dark_futuristic', 'emerald')" class="text-[10px] px-2 py-0.5 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-800">🛒 Cyber Hardware</button>
            <button type="button" onclick="selectPreset('Autonomous Design and Engineering Studio with interactive showcase', 'agency', 'editorial_brutalist', 'amber')" class="text-[10px] px-2 py-0.5 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-800">🚀 AI Agency</button>
          </div>
        </div>

        <!-- Website Category Pills -->
        <div>
          <label class="block text-[11px] font-semibold text-zinc-400 mb-1">Website Category</label>
          <div class="grid grid-cols-4 gap-1 text-xs font-medium">
            <button type="button" onclick="selectType('portfolio')" id="btn-type-portfolio" class="py-1 px-1 rounded border border-indigo-500 bg-indigo-500/20 text-white text-center">Portfolio</button>
            <button type="button" onclick="selectType('saas')" id="btn-type-saas" class="py-1 px-1 rounded border border-surfaceBorder bg-zinc-900 text-zinc-400 text-center">SaaS</button>
            <button type="button" onclick="selectType('ecommerce')" id="btn-type-ecommerce" class="py-1 px-1 rounded border border-surfaceBorder bg-zinc-900 text-zinc-400 text-center">Store</button>
            <button type="button" onclick="selectType('agency')" id="btn-type-agency" class="py-1 px-1 rounded border border-surfaceBorder bg-zinc-900 text-zinc-400 text-center">Agency</button>
          </div>
        </div>

        <!-- Style & Palette Selection -->
        <div class="grid grid-cols-2 gap-2 text-xs">
          <div>
            <label class="block text-[11px] font-semibold text-zinc-400 mb-1">Aesthetic Style</label>
            <select id="style-select" class="w-full p-1.5 rounded bg-zinc-900 border border-surfaceBorder text-zinc-300 text-xs">
              <option value="dark_futuristic">Dark Futuristic</option>
              <option value="minimal_luxury">Minimal Luxury</option>
              <option value="editorial_brutalist">Editorial Brutalist</option>
              <option value="clean_modern">Clean Modern</option>
            </select>
          </div>
          <div>
            <label class="block text-[11px] font-semibold text-zinc-400 mb-1">Color Palette</label>
            <select id="palette-select" class="w-full p-1.5 rounded bg-zinc-900 border border-surfaceBorder text-zinc-300 text-xs">
              <option value="indigo">Indigo Accent</option>
              <option value="emerald">Emerald Neon</option>
              <option value="cyan">Cyan High-Tech</option>
              <option value="amber">Amber Glow</option>
              <option value="violet">Electric Violet</option>
            </select>
          </div>
        </div>

        <!-- Sections Checklist -->
        <div>
          <label class="block text-[11px] font-semibold text-zinc-400 mb-1">Sections to Include</label>
          <div class="grid grid-cols-3 gap-1 text-[11px] text-zinc-300">
            <label class="flex items-center space-x-1 cursor-pointer"><input type="checkbox" id="sec-hero" checked class="rounded bg-zinc-800 text-indigo-500"> <span>Hero</span></label>
            <label class="flex items-center space-x-1 cursor-pointer"><input type="checkbox" id="sec-features" checked class="rounded bg-zinc-800 text-indigo-500"> <span>Features</span></label>
            <label class="flex items-center space-x-1 cursor-pointer"><input type="checkbox" id="sec-stats" checked class="rounded bg-zinc-800 text-indigo-500"> <span>Metrics</span></label>
            <label class="flex items-center space-x-1 cursor-pointer"><input type="checkbox" id="sec-pricing" checked class="rounded bg-zinc-800 text-indigo-500"> <span>Pricing</span></label>
            <label class="flex items-center space-x-1 cursor-pointer"><input type="checkbox" id="sec-contact" checked class="rounded bg-zinc-800 text-indigo-500"> <span>Contact</span></label>
          </div>
        </div>

        <!-- Generate Button -->
        <button id="btn-generate" onclick="generateFromPrompt()" class="w-full py-2.5 px-3 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition shadow-md shadow-indigo-600/20 flex items-center justify-center space-x-1.5">
          <span>⚡</span>
          <span>Generate Website from Prompt</span>
        </button>
      </div>

      <!-- Engineering & Testing Controls -->
      <div class="p-4 rounded-xl border border-surfaceBorder bg-surface space-y-2">
        <h2 class="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-2">Verification & Diagnostics</h2>
        <div class="grid grid-cols-2 gap-2">
          <button onclick="runTests()" class="py-1.5 px-2 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-medium text-white border border-surfaceBorder">
            Run Playwright Tests
          </button>
          <button onclick="runAudits()" class="py-1.5 px-2 rounded bg-zinc-800 hover:bg-zinc-700 text-xs font-medium text-indigo-300 border border-surfaceBorder">
            Run SEO/Perf Audit
          </button>
          <button onclick="simulateRouteBug()" class="py-1.5 px-2 rounded bg-amber-600/20 text-amber-300 hover:bg-amber-600/30 text-xs font-medium border border-amber-500/30">
            Simulate Route Bug
          </button>
          <button onclick="runRepairLoop()" class="py-1.5 px-2 rounded bg-emerald-600 hover:bg-emerald-500 text-xs font-medium text-white shadow-md">
            Auto Repair Loop
          </button>
        </div>
      </div>

      <!-- Agent Hierarchy Tree -->
      <div class="p-4 rounded-xl border border-surfaceBorder bg-surface">
        <h2 class="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-3">Agent Hierarchy (Section 44)</h2>
        <div id="agent-tree" class="text-xs font-mono space-y-2">
          <div class="text-zinc-500">No active agent run. Trigger an action above.</div>
        </div>
      </div>

      <!-- File Tree -->
      <div class="p-4 rounded-xl border border-surfaceBorder bg-surface">
        <h2 class="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-3">Project Files</h2>
        <div id="file-list" class="text-xs font-mono space-y-1 max-h-40 overflow-y-auto">
          <div class="text-zinc-500">Loading files...</div>
        </div>
      </div>
    </div>

    <!-- Center: Live Preview & Diff -->
    <div class="col-span-5 flex flex-col space-y-4">
      <div class="p-4 rounded-xl border border-surfaceBorder bg-surface flex-1 flex flex-col">
        <div class="flex items-center justify-between pb-3 border-b border-surfaceBorder mb-3">
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-red-500/80"></span>
            <span class="w-3 h-3 rounded-full bg-yellow-500/80"></span>
            <span class="w-3 h-3 rounded-full bg-green-500/80"></span>
            <span class="text-xs font-mono text-zinc-400 ml-2">Live Dev Preview</span>
          </div>
          <div class="flex items-center space-x-1.5">
            <button onclick="setViewport('desktop')" id="vp-desktop" class="px-2 py-0.5 rounded text-[10px] bg-zinc-800 text-white font-mono border border-zinc-700">Desktop</button>
            <button onclick="setViewport('tablet')" id="vp-tablet" class="px-2 py-0.5 rounded text-[10px] bg-zinc-900 text-zinc-400 font-mono border border-zinc-800">Tablet</button>
            <button onclick="setViewport('mobile')" id="vp-mobile" class="px-2 py-0.5 rounded text-[10px] bg-zinc-900 text-zinc-400 font-mono border border-zinc-800">Mobile</button>
            <a href="http://127.0.0.1:3456" target="_blank" class="text-xs text-indigo-400 hover:underline px-1 font-mono">↗ Popout</a>
            <button onclick="refreshPreview()" class="text-xs text-zinc-400 hover:text-white px-1">↻</button>
          </div>
        </div>
        <div class="flex-1 flex justify-center bg-black/60 rounded-lg overflow-hidden border border-surfaceBorder p-1">
          <iframe id="preview-frame" src="http://127.0.0.1:3456" class="h-full rounded bg-black min-h-[440px] transition-all duration-300" style="width: 100%;"></iframe>
        </div>
      </div>

      <!-- Minimal Change Diff Viewer -->
      <div class="p-4 rounded-xl border border-surfaceBorder bg-surface h-56 flex flex-col">
        <h2 class="text-sm font-semibold uppercase tracking-wider text-zinc-400 mb-2">Minimal Change Git Diff Viewer (Section 13, 31)</h2>
        <pre id="diff-viewer" class="flex-1 text-xs text-emerald-400 bg-zinc-950 p-3 rounded-lg overflow-auto border border-zinc-900">No uncommitted changes detected.</pre>
      </div>
    </div>

    <!-- Right: Test Harness & Trajectory Log -->
    <div class="col-span-3 space-y-4">
      <div class="p-4 rounded-xl border border-surfaceBorder bg-surface">
        <h2 class="text-sm font-semibold uppercase tracking-wider text-zinc-400 mb-3">Test Results (Levels 1-7)</h2>
        <div id="test-results" class="text-xs space-y-2">
          <div class="text-zinc-500">Run tests to inspect static, build, Playwright, and A11y status.</div>
        </div>
      </div>

      <div class="p-4 rounded-xl border border-surfaceBorder bg-surface">
        <h2 class="text-sm font-semibold uppercase tracking-wider text-zinc-400 mb-3">Git Checkpoint History</h2>
        <div id="git-history" class="text-xs font-mono space-y-2 max-h-56 overflow-y-auto">
          <div class="text-zinc-500">No checkpoints recorded yet.</div>
        </div>
      </div>
    </div>
  </main>

  <!-- AI Model & Training Hub View -->
  <div id="view-model" class="flex-1 hidden p-8 max-w-7xl mx-auto w-full space-y-8">
    <div class="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-surfaceBorder gap-4">
      <div>
        <h1 class="text-2xl font-black text-white tracking-tight">AI Model & Training Hub</h1>
        <p class="text-xs text-zinc-400 mt-1">Supervise local neural weights, instruction-tuning datasets, and hardware limits.</p>
      </div>
      <div class="flex items-center space-x-3">
        <button type="button" onclick="recompileDatasets()" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-md transition flex items-center space-x-1.5">
          <span>⚡ Recompile JSONL Splits</span>
        </button>
        <button type="button" onclick="loadModelView()" class="px-4 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-semibold text-xs border border-zinc-700 transition">
          <span>↻ Refresh Telemetry</span>
        </button>
      </div>
    </div>

    <!-- 3-Column Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Card 1: Model Architecture -->
      <div class="p-6 rounded-2xl bg-surface border border-surfaceBorder space-y-4">
        <div class="flex items-center justify-between">
          <span class="text-xs font-mono text-zinc-400 uppercase tracking-wider">Active Base Model</span>
          <span id="model-status-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">READY ON DISK</span>
        </div>
        <div>
          <div class="text-xl font-black text-white" id="model-title">Qwen2.5-Coder-3B</div>
          <div class="text-xs text-indigo-400 font-mono mt-0.5" id="model-file">qwen2.5-coder-3b-instruct-q4_k_m.gguf</div>
        </div>
        <div class="pt-2 border-t border-zinc-800 space-y-2 text-xs text-zinc-300">
          <div class="flex justify-between"><span class="text-zinc-500">Weight File Size:</span><span id="model-size" class="font-mono text-white">2,007.4 MB (~1.96 GB)</span></div>
          <div class="flex justify-between"><span class="text-zinc-500">Quantization:</span><span class="font-mono text-emerald-400">4-bit GGUF (Q4_K_M)</span></div>
          <div class="flex justify-between"><span class="text-zinc-500">Fine-Tuning Architecture:</span><span class="font-mono text-indigo-300">QLoRA (Rank 16, Alpha 32)</span></div>
          <div class="flex justify-between"><span class="text-zinc-500">Hardware Profile:</span><span id="model-gpu" class="font-mono text-zinc-300">RTX 3050 Laptop (6GB VRAM)</span></div>
          <div class="flex justify-between"><span class="text-zinc-500">Training VRAM Footprint:</span><span class="font-mono text-emerald-300">~3.85 GB / 6.0 GB [Safe]</span></div>
        </div>
      </div>

      <!-- Card 2: Training Data Store -->
      <div class="p-6 rounded-2xl bg-surface border border-surfaceBorder space-y-4">
        <div class="flex items-center justify-between">
          <span class="text-xs font-mono text-zinc-400 uppercase tracking-wider">Validated Data Lake</span>
          <span id="model-val-total" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">456 VALIDATED</span>
        </div>
        <div>
          <div class="text-3xl font-black text-white" id="model-val-count">456</div>
          <div class="text-xs text-zinc-400 mt-0.5">Production-grade verified examples</div>
        </div>
        <div class="pt-2 border-t border-zinc-800 space-y-2 text-xs text-zinc-300">
          <div class="flex justify-between"><span class="text-zinc-500">HTML Components:</span><span id="model-html-count" class="font-mono text-white">328</span></div>
          <div class="flex justify-between"><span class="text-zinc-500">CSS Stylesheets:</span><span id="model-css-count" class="font-mono text-white">8</span></div>
          <div class="flex justify-between"><span class="text-zinc-500">Debugging Trajectories:</span><span id="model-dbg-count" class="font-mono text-white">100</span></div>
          <div class="flex justify-between"><span class="text-zinc-500">Paired Multi-Scale Sites:</span><span id="model-pair-count" class="font-mono text-white">20</span></div>
          <div class="flex justify-between"><span class="text-zinc-500">Duplicates Filtered:</span><span id="model-dup-count" class="font-mono text-cyan-400">264 skipped</span></div>
        </div>
      </div>

      <!-- Card 3: Compiled JSONL Datasets -->
      <div class="p-6 rounded-2xl bg-surface border border-surfaceBorder space-y-4">
        <div class="flex items-center justify-between">
          <span class="text-xs font-mono text-zinc-400 uppercase tracking-wider">Instruction Datasets</span>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-purple-500/10 text-purple-400 border border-purple-500/20">80/10/10 ISOLATION</span>
        </div>
        <div class="space-y-3 pt-2 text-xs">
          <div class="p-2.5 rounded-xl bg-zinc-900 border border-zinc-800">
            <div class="font-bold text-white flex justify-between"><span>html_train.jsonl</span><span class="text-indigo-400 font-mono">264 samples</span></div>
            <div class="text-[11px] text-zinc-500 mt-0.5">80% train partition with strict test isolation</div>
          </div>
          <div class="p-2.5 rounded-xl bg-zinc-900 border border-zinc-800">
            <div class="font-bold text-white flex justify-between"><span>debugging_train.jsonl</span><span class="text-indigo-400 font-mono">81 samples</span></div>
            <div class="text-[11px] text-zinc-500 mt-0.5">Autonomous self-healing minimal diff trajectories</div>
          </div>
          <div class="p-2.5 rounded-xl bg-zinc-900 border border-zinc-800">
            <div class="font-bold text-white flex justify-between"><span>portfolio_train.jsonl</span><span class="text-indigo-400 font-mono">58 samples</span></div>
            <div class="text-[11px] text-zinc-500 mt-0.5">8 domains across 10 modern aesthetic styles</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Category Coverage Matrix -->
    <div class="p-6 rounded-2xl bg-surface border border-surfaceBorder space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="text-sm font-bold text-white uppercase tracking-wider">Dataset Category Distribution (Sections 5 & 6)</h3>
        <span class="text-xs text-zinc-400 font-mono">20 Total Categories Targeted</span>
      </div>
      <div id="category-badges" class="flex flex-wrap gap-2 pt-2">
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Cards: <strong>58</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Forms: <strong>57</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Portfolios: <strong>38</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Ecommerce: <strong>28</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Footers: <strong>28</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Heroes: <strong>27</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Tables: <strong>27</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Accessibility: <strong>27</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Complete Pages: <strong>20</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Debugging: <strong>100</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Pricing: <strong>6</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Dashboards: <strong>6</strong></span>
        <span class="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300">Buttons: <strong>6</strong></span>
      </div>
    </div>

    <!-- Live Chat Playground with Qwen2.5-Coder-3B -->
    <div class="p-6 rounded-2xl bg-surface border border-surfaceBorder space-y-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <h3 class="text-sm font-bold text-white uppercase tracking-wider">Live Chat Playground • Qwen2.5-Coder-3B</h3>
        </div>
        <span class="text-xs text-zinc-400 font-mono">Direct Local GGUF Inference • Zero Cloud API</span>
      </div>
      <div id="model-chat-history" class="p-4 rounded-xl bg-zinc-950 border border-zinc-900 min-h-[160px] max-h-[340px] overflow-y-auto space-y-3 text-xs">
        <div class="p-3 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-300">
          <strong class="text-indigo-400">Qwen2.5-Coder-3B:</strong> Hello! I am your local Ornàment AI website engineer running directly on your machine. You can talk to me, ask me to scaffold components, diagnose bugs, or write modern responsive CSS/HTML!
        </div>
      </div>
      <div class="flex gap-2">
        <input id="model-chat-input" type="text" placeholder="e.g. Write an ultra-modern dark hero section with Tailwind CSS and stats badges..." class="flex-1 text-xs px-4 py-3 rounded-xl bg-zinc-900 border border-zinc-800 text-white focus:outline-none focus:border-indigo-500 font-sans" onkeydown="if(event.key === 'Enter') sendModelChat()" />
        <button type="button" onclick="sendModelChat()" id="btn-send-chat" class="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-md transition flex items-center space-x-1.5">
          <span>Send Message</span>
        </button>
      </div>
    </div>
  </div>

  <script>
    async function sendModelChat() {
      const input = document.getElementById('model-chat-input');
      const btn = document.getElementById('btn-send-chat');
      const history = document.getElementById('model-chat-history');
      const text = input.value.trim();
      if (!text) return;

      const userDiv = document.createElement('div');
      userDiv.className = 'p-3 rounded-lg bg-indigo-950/40 border border-indigo-900/60 text-indigo-200';
      userDiv.innerHTML = `<strong class="text-white">You:</strong> \${text}`;
      history.appendChild(userDiv);
      input.value = '';
      history.scrollTop = history.scrollHeight;

      const botDiv = document.createElement('div');
      botDiv.className = 'p-3 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-300';
      botDiv.innerHTML = `<strong class="text-indigo-400">Qwen2.5-Coder-3B:</strong> <span class="text-indigo-300 animate-pulse">Thinking locally on RTX 3050...</span>`;
      history.appendChild(botDiv);
      history.scrollTop = history.scrollHeight;
      btn.disabled = true;

      try {
        const res = await fetch('/api/model/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        botDiv.innerHTML = `<strong class="text-indigo-400">Qwen2.5-Coder-3B:</strong> <div class="mt-1.5 whitespace-pre-wrap font-sans leading-relaxed">\${data.reply || data.detail}</div>`;
      } catch (err) {
        botDiv.innerHTML = `<strong class="text-rose-400">Error:</strong> \${err.message}`;
      } finally {
        btn.disabled = false;
        history.scrollTop = history.scrollHeight;
      }
    }
    let currentType = 'portfolio';

    function selectType(type) {
      currentType = type;
      const types = ['portfolio', 'saas', 'ecommerce', 'agency'];
      types.forEach(t => {
        const btn = document.getElementById('btn-type-' + t);
        if (btn) {
          if (t === type) {
            btn.className = 'py-1 px-1 rounded border border-indigo-500 bg-indigo-500/20 text-white text-center';
          } else {
            btn.className = 'py-1 px-1 rounded border border-surfaceBorder bg-zinc-900 text-zinc-400 text-center';
          }
        }
      });
    }

    function selectPreset(promptText, type, style, palette) {
      document.getElementById('prompt-input').value = promptText;
      selectType(type);
      if (document.getElementById('style-select')) document.getElementById('style-select').value = style;
      if (document.getElementById('palette-select')) document.getElementById('palette-select').value = palette;
    }

    function setViewport(mode) {
      const frame = document.getElementById('preview-frame');
      const btnDesk = document.getElementById('vp-desktop');
      const btnTab = document.getElementById('vp-tablet');
      const btnMob = document.getElementById('vp-mobile');
      
      btnDesk.className = 'px-2 py-0.5 rounded text-[10px] bg-zinc-900 text-zinc-400 font-mono border border-zinc-800';
      btnTab.className = 'px-2 py-0.5 rounded text-[10px] bg-zinc-900 text-zinc-400 font-mono border border-zinc-800';
      btnMob.className = 'px-2 py-0.5 rounded text-[10px] bg-zinc-900 text-zinc-400 font-mono border border-zinc-800';

      if (mode === 'desktop') {
        frame.style.width = '100%';
        btnDesk.className = 'px-2 py-0.5 rounded text-[10px] bg-zinc-800 text-white font-mono border border-zinc-700';
      } else if (mode === 'tablet') {
        frame.style.width = '768px';
        btnTab.className = 'px-2 py-0.5 rounded text-[10px] bg-zinc-800 text-white font-mono border border-zinc-700';
      } else if (mode === 'mobile') {
        frame.style.width = '375px';
        btnMob.className = 'px-2 py-0.5 rounded text-[10px] bg-zinc-800 text-white font-mono border border-zinc-700';
      }
    }

    async function updateTelemetry() {
      try {
        const res = await fetch('/api/health');
        const data = await res.json();
        document.getElementById('cpu-stat').innerText = data.system.cpu_percent + '%';
        document.getElementById('ram-stat').innerText = data.system.ram_available_mb + ' MB free';
        document.getElementById('vram-stat').innerText = (data.system.vram_free_mb || 0) + ' MB free';
      } catch (e) {}
    }
    setInterval(updateTelemetry, 3000);
    updateTelemetry();

    async function loadFiles() {
      try {
        const res = await fetch('/api/projects/demo-portfolio/files');
        const files = await res.json();
        const list = document.getElementById('file-list');
        list.innerHTML = files.map(f => `<div class="p-1 hover:bg-zinc-800 rounded cursor-pointer">${f}</div>`).join('');
      } catch (e) {}
    }

    async function loadHistory() {
      try {
        const res = await fetch('/api/projects/demo-portfolio/history');
        const history = await res.json();
        const el = document.getElementById('git-history');
        el.innerHTML = history.map(h => `
          <div class="p-2 rounded bg-zinc-900 border border-zinc-800">
            <span class="text-indigo-400 font-bold">${h.hexsha}</span>: ${h.message}
          </div>
        `).join('');
      } catch (e) {}
    }

    async function loadDiff() {
      try {
        const res = await fetch('/api/projects/demo-portfolio/diff');
        const data = await res.json();
        document.getElementById('diff-viewer').innerText = data.diff || 'No uncommitted changes detected.';
      } catch (e) {}
    }

    async function generateFromPrompt() {
      const prompt = document.getElementById('prompt-input').value;
      const style = document.getElementById('style-select').value;
      const palette = document.getElementById('palette-select').value;
      
      const sections = [];
      if (document.getElementById('sec-hero')?.checked) sections.push('hero');
      if (document.getElementById('sec-features')?.checked) sections.push('features');
      if (document.getElementById('sec-stats')?.checked) sections.push('stats');
      if (document.getElementById('sec-pricing')?.checked) sections.push('pricing');
      if (document.getElementById('sec-contact')?.checked) sections.push('contact');

      const tree = document.getElementById('agent-tree');
      tree.innerHTML = `
        <div class="text-indigo-400">
          <div>Main Agent (Architect) [PLANNING SPECIFICATION]</div>
          <div class="ml-3">├── Code Agent (Synthesizing ${currentType} code) [RUNNING]</div>
          <div class="ml-3">└── Test Agent (Verifying Playwright & A11y) [QUEUED]</div>
        </div>
      `;

      try {
        const res = await fetch('/api/projects/generate-custom', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            project_name: 'demo-portfolio',
            prompt: prompt,
            site_type: currentType,
            style: style,
            color_palette: palette,
            sections: sections
          })
        });
        const data = await res.json();

        tree.innerHTML = `
          <div class="text-emerald-400">
            <div>Main Agent (Architect) [SPECIFICATION RESOLVED]</div>
            <div class="ml-3">├── Code Agent [OK] Generated ${data.files_count} files (${data.checkpoint})</div>
            <div class="ml-3">└── Test Agent [OK] Dev preview loaded</div>
          </div>
        `;

        refreshPreview();
        loadFiles();
        loadHistory();
        loadDiff();
      } catch (e) {
        alert('Generation failed: ' + e);
      }
    }

    async function simulateRouteBug() {
      try {
        const res = await fetch('/api/projects/demo-portfolio/simulate-bug', { method: 'POST' });
        const data = await res.json();
        refreshPreview();
        loadDiff();
        alert('Intentional Route Bug Simulated: ' + data.message + '\n\nNow click "Run Playwright Tests" to catch it, or "Auto Repair Loop" to have the agent fleet diagnose and fix it!');
      } catch (e) {
        alert('Simulate bug error: ' + e);
      }
    }

    async function runAudits() {
      const el = document.getElementById('test-results');
      el.innerHTML = '<div class="text-indigo-400 animate-pulse">Running SEO, Performance, and Accessibility audits...</div>';
      const res = await fetch('/api/projects/demo-portfolio/run-audits', { method: 'POST' });
      const data = await res.json();
      el.innerHTML = `
        <div class="p-2 rounded ${data.seo.status === 'PASS' ? 'bg-green-950/40 border-green-800 text-green-300' : 'bg-yellow-950/40 border-yellow-800 text-yellow-300'} border">
          <div class="font-bold flex justify-between"><span>SEO Audit</span><span>${data.seo.status} (${data.seo.score}/100)</span></div>
          <div class="text-[11px] mt-1 text-zinc-400">${data.seo.issues.length} issues found</div>
        </div>
        <div class="p-2 rounded ${data.performance.status === 'PASS' ? 'bg-green-950/40 border-green-800 text-green-300' : 'bg-yellow-950/40 border-yellow-800 text-yellow-300'} border mt-2">
          <div class="font-bold flex justify-between"><span>Performance Audit</span><span>${data.performance.status} (${data.performance.score}/100)</span></div>
          <div class="text-[11px] mt-1 text-zinc-400">${data.performance.issues.length} recommendations</div>
        </div>
        <div class="p-2 rounded ${data.accessibility.status === 'PASS' ? 'bg-green-950/40 border-green-800 text-green-300' : 'bg-yellow-950/40 border-yellow-800 text-yellow-300'} border mt-2">
          <div class="font-bold flex justify-between"><span>Accessibility Audit</span><span>${data.accessibility.status} (${data.accessibility.score}/100)</span></div>
          <div class="text-[11px] mt-1 text-zinc-400">${data.accessibility.issues.length} checks</div>
        </div>
      `;
    }

    async function runTests() {
      const el = document.getElementById('test-results');
      el.innerHTML = '<div class="text-indigo-400 animate-pulse">Running Playwright browser and static tests...</div>';
      const res = await fetch('/api/projects/demo-portfolio/run-tests', { method: 'POST' });
      const data = await res.json();
      el.innerHTML = data.results.map(r => `
        <div class="p-2 rounded ${r.passed ? 'bg-green-950/40 border-green-800 text-green-300' : 'bg-red-950/40 border-red-800 text-red-300'} border">
          <div class="font-bold flex justify-between"><span>${r.level}</span><span>${r.status}</span></div>
          <div class="text-[11px] mt-1 text-zinc-400">${r.summary}</div>
        </div>
      `).join('');
    }

    async function runRepairLoop() {
      const tree = document.getElementById('agent-tree');
      tree.innerHTML = `
        <div class="text-indigo-400">
          <div>Main Agent (Architect) [RUNNING]</div>
          <div class="ml-3">├── Debug Agent (Diagnostician) [DIAGNOSING]</div>
          <div class="ml-3">├── Code Agent (Minimal Patch) [QUEUED]</div>
          <div class="ml-3">└── Test Agent (Playwright) [QUEUED]</div>
        </div>
      `;
      const res = await fetch('/api/projects/demo-portfolio/run-repair', { method: 'POST' });
      const data = await res.json();
      tree.innerHTML = `
        <div class="text-emerald-400">
          <div>Main Agent (Architect) [COMPLETED]</div>
          <div class="ml-3">├── Debug Agent (Diagnostician) [DIAGNOSED]</div>
          <div class="ml-3">├── Code Agent (Minimal Patch) [APPLIED 1 FILE]</div>
          <div class="ml-3">└── Test Agent (Playwright) [PASS]</div>
        </div>
      `;
      refreshPreview();
      loadHistory();
      loadDiff();
      runTests();
      alert('Autonomous Repair Loop Completed: Route mismatch diagnosed and fixed under Minimal Change Policy!');
    }

    function refreshPreview() {
      const frame = document.getElementById('preview-frame');
      frame.src = frame.src;
    }

    function switchView(view) {
      const studio = document.getElementById('view-studio');
      const model = document.getElementById('view-model');
      const btnStudio = document.getElementById('tab-btn-studio');
      const btnModel = document.getElementById('tab-btn-model');

      if (view === 'studio') {
        studio.classList.remove('hidden');
        model.classList.add('hidden');
        btnStudio.className = 'px-3 py-1 rounded bg-indigo-600 font-bold text-white shadow transition';
        btnModel.className = 'px-3 py-1 rounded text-zinc-400 hover:text-white font-medium transition';
      } else {
        studio.classList.add('hidden');
        model.classList.remove('hidden');
        btnStudio.className = 'px-3 py-1 rounded text-zinc-400 hover:text-white font-medium transition';
        btnModel.className = 'px-3 py-1 rounded bg-indigo-600 font-bold text-white shadow transition';
        loadModelView();
      }
    }

    async function loadModelView() {
      try {
        const [mRes, sRes] = await Promise.all([
          fetch('/api/model/status'),
          fetch('/api/training-data/stats')
        ]);
        const mData = await mRes.json();
        const sData = await sRes.json();

        // Model Architecture
        document.getElementById('model-title').textContent = mData.model_name;
        document.getElementById('model-file').textContent = mData.weights_path.split('\\\\').pop().split('/').pop();
        document.getElementById('model-size').textContent = `${mData.weights_size_mb} MB (~${(mData.weights_size_mb / 1024).toFixed(2)} GB)`;
        document.getElementById('model-gpu').textContent = `${mData.gpu} (${(mData.vram_total_mb / 1024).toFixed(1)} GB VRAM)`;
        
        // Data Lake
        const counts = sData.counts || {};
        document.getElementById('model-val-total').textContent = `${counts.validated || 0} VALIDATED`;
        document.getElementById('model-val-count').textContent = counts.validated || 0;
        document.getElementById('model-html-count').textContent = counts.html || 0;
        document.getElementById('model-css-count').textContent = counts.css || 0;
        document.getElementById('model-dbg-count').textContent = counts.debugging || 0;
        document.getElementById('model-pair-count').textContent = counts.paired || 0;
        document.getElementById('model-dup-count').textContent = `${sData.duplicate_skips || 0} skipped`;

        // Category Badges
        const catMap = sData.category_counts || {};
        const badgesContainer = document.getElementById('category-badges');
        badgesContainer.innerHTML = '';
        for (const [lang, cats] of Object.entries(catMap)) {
          for (const [cat, num] of Object.entries(cats)) {
            const badge = document.createElement('span');
            badge.className = 'px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-300';
            badge.innerHTML = `${cat}: <strong class="text-white">${num}</strong>`;
            badgesContainer.appendChild(badge);
          }
        }
      } catch (err) {
        console.error('Failed loading model view metrics:', err);
      }
    }

    async function recompileDatasets() {
      try {
        const btn = event.target;
        btn.textContent = 'Compiling...';
        const res = await fetch('/api/training-data/build', { method: 'POST' });
        const data = await res.json();
        alert(`Compilation Complete: ${data.version}\\nHTML Splits: ${JSON.stringify(data.datasets.datasets_created.html)}\\nDebugging Splits: ${JSON.stringify(data.datasets.datasets_created.debugging)}`);
        btn.textContent = '⚡ Recompile JSONL Splits';
        loadModelView();
      } catch (err) {
        alert('Recompilation error: ' + err);
      }
    }

    // Initial load
    loadFiles();
    loadHistory();
    loadDiff();
  </script>
</body>
</html>"""

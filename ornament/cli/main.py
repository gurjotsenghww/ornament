import argparse
import asyncio
import sys
import uvicorn
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ornament.config import settings
from ornament.hardware.monitor import HardwareManager
from ornament.generator.portfolio_generator import PortfolioGenerator
from ornament.git_ops.checkpoint import GitCheckpointManager
from ornament.testing.runner import MultiLevelTestHarness
from ornament.agents.main_agent import MainAgent
from ornament.models.provider.factory import get_model_provider
from ornament.sandbox.dev_server import DevPreviewServer

console = Console()

def cmd_telemetry(args):
    tel = HardwareManager.get_system_telemetry()
    table = Table(title="Ornàment Hardware Telemetry")
    table.add_column("Resource", style="cyan")
    table.add_column("Measurement", style="green")

    table.add_row("CPU Utilization", f"{tel.cpu_percent}% ({tel.cpu_count} logical cores)")
    table.add_row("RAM Total / Available", f"{tel.ram_total_mb:.0f} MB / {tel.ram_available_mb:.0f} MB free ({tel.ram_used_percent}% used)")
    table.add_row("GPU Device", f"{tel.gpu_name if tel.gpu_available else 'None detected'}")
    if tel.gpu_available:
        table.add_row("VRAM Total / Free", f"{tel.vram_total_mb:.0f} MB / {tel.vram_free_mb:.0f} MB free")
        table.add_row("GPU Utilization / Temp", f"{tel.gpu_util_percent}% / {tel.gpu_temp_c}°C")

    console.print(table)
    recs = HardwareManager.get_model_recommendations()
    console.print(Panel(f"[bold yellow]Model Loading Strategy:[/bold yellow] {recs['recommendation']} (Quantization: {recs['quantization']}, Context tokens: {recs['max_context_tokens']})"))

def cmd_generate(args):
    target = settings.workspace_dir / args.name
    site_type = getattr(args, "type", "portfolio").lower()

    if site_type == "ecommerce":
        from ornament.generator.ecommerce_generator import EcommerceGenerator
        console.print(f"[bold cyan][*] Generating E-Commerce Store into: {target}[/bold cyan]")
        res = EcommerceGenerator.generate(target)
        count = res["files_count"]
    elif site_type == "saas":
        from ornament.generator.saas_generator import SaasGenerator
        console.print(f"[bold cyan][*] Generating SaaS Platform into: {target}[/bold cyan]")
        res = SaasGenerator.generate(target)
        count = res["files_count"]
    else:
        console.print(f"[bold cyan][*] Generating Developer Portfolio into: {target}[/bold cyan]")
        res = PortfolioGenerator.generate(target, intentional_bug=args.bug)
        count = len(res["files_created"])

    git_mgr = GitCheckpointManager(target)
    cp = git_mgr.create_checkpoint(f"{site_type.title()} generated", agent_id="main_agent")
    console.print(f"[bold green][OK] Generation complete ({count} files). Git Checkpoint: {cp[:8]}[/bold green]")
    if site_type == "portfolio" and args.bug:
        console.print("[bold red][!] Controlled Bug Introduced: Navbar contact button points to /contact-us instead of /contact[/bold red]")

def cmd_audit(args):
    from ornament.testing.auditors import SiteAuditor
    target = settings.workspace_dir / args.name
    console.print(f"[bold cyan][*] Running SEO, Performance, and Accessibility Audits on: {target}[/bold cyan]")
    
    seo = SiteAuditor.run_seo_audit(target)
    perf = SiteAuditor.run_performance_audit(target)
    a11y = SiteAuditor.run_accessibility_audit(target)

    table = Table(title="Website Engineering Audits")
    table.add_column("Category", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Score", style="white")
    table.add_column("Issues / Notices", style="yellow")

    for rep in [seo, perf, a11y]:
        style = "green" if rep.status == "PASS" else ("yellow" if rep.status == "WARNING" else "red")
        issue_summary = "; ".join([f"[{i.severity}] {i.message}" for i in rep.issues[:2]]) or "Clean"
        table.add_row(rep.category, f"[{style}]{rep.status}[/{style}]", f"{rep.score:.1f}/100", issue_summary)

    console.print(table)

def cmd_benchmark(args):
    import subprocess
    target = settings.workspace_dir / args.name
    console.print(f"[bold cyan][*] Running Ornàment 5-Dimension Evaluation Benchmark on: {target}[/bold cyan]")
    bench_script = settings.base_dir / "ai-website-engineer-model" / "evaluation" / "benchmark_suite.py"
    subprocess.run([sys.executable, str(bench_script), "--project", f"workspace/{args.name}"])

def cmd_test(args):
    target = settings.workspace_dir / args.name
    async def _run():
        server = DevPreviewServer(target, port=3456)
        server.start()
        try:
            console.print("[bold cyan][*] Launching Multi-Level Test Harness (Levels 1, 2, 4, 7)...[/bold cyan]")
            lvl1 = await MultiLevelTestHarness.run_level1_static(target)
            lvl2 = await MultiLevelTestHarness.run_level2_build(target)
            lvl4 = await MultiLevelTestHarness.run_level4_browser_functional(
                base_url=server.url,
                target_route="/",
                click_selector="#nav-contact-button",
                expected_route="/contact"
            )
            lvl7 = await MultiLevelTestHarness.run_level7_accessibility(target)

            table = Table(title="Test Verification Results")
            table.add_column("Level", style="cyan")
            table.add_column("Status", style="bold")
            table.add_column("Summary", style="white")

            for lvl in [lvl1, lvl2, lvl4, lvl7]:
                style = "green" if lvl.passed else "red"
                table.add_row(lvl.level.value, f"[{style}]{lvl.status}[/{style}]", lvl.summary)

            console.print(table)
        finally:
            server.stop()
    asyncio.run(_run())

def cmd_repair(args):
    target = settings.workspace_dir / args.name
    async def _run():
        server = DevPreviewServer(target, port=3456)
        server.start()
        try:
            console.print("[bold cyan][*] Starting Main Agent Autonomous Repair Loop...[/bold cyan]")
            main_agent = MainAgent(
                task=args.symptom,
                workspace_path=target,
                model_provider=get_model_provider()
            )
            res = await main_agent.run_repair_loop(
                symptom=args.symptom,
                base_url=server.url,
                test_selector="#nav-contact-button",
                expected_route="/contact"
            )
            if res.get("final_status") == "PASS":
                console.print(f"[bold green][OK] Repair Succeeded in {res['attempts']} attempt(s)! Commit: {res['commit'][:8]}[/bold green]")
            else:
                console.print(f"[bold red][FAIL] Repair failed: {res}[/bold red]")
        finally:
            server.stop()
    asyncio.run(_run())

def cmd_serve(args):
    console.print(f"[bold green][*] Starting Ornàment UI Server on http://localhost:{args.port}[/bold green]")
    uvicorn.run("ornament.server.api:app", host="0.0.0.0", port=args.port, reload=False)

def main():
    parser = argparse.ArgumentParser(prog="ornament", description="Ornàment AI Website Engineer CLI")
    subparsers = parser.add_subparsers(dest="command")

    # telemetry
    subparsers.add_parser("telemetry", help="Display real-time hardware telemetry and model loading mode")

    # generate
    gen = subparsers.add_parser("generate", help="Scaffold a website project")
    gen.add_argument("--name", default="demo-portfolio", help="Project folder name")
    gen.add_argument("--type", choices=["portfolio", "ecommerce", "saas"], default="portfolio", help="Website category (portfolio, ecommerce, saas)")
    gen.add_argument("--bug", action="store_true", help="Introduce intentional route mismatch bug for debugging demo")

    # audit
    aud = subparsers.add_parser("audit", help="Run SEO, Performance, and Accessibility audits")
    aud.add_argument("--name", default="demo-portfolio")

    # benchmark
    bm = subparsers.add_parser("benchmark", help="Run fixed 5-dimension evaluation benchmark")
    bm.add_argument("--name", default="demo-portfolio")

    # test
    tst = subparsers.add_parser("test", help="Run multi-level test suite")
    tst.add_argument("--name", default="demo-portfolio")

    # repair
    rep = subparsers.add_parser("repair", help="Trigger autonomous repair loop on a symptom")
    rep.add_argument("--name", default="demo-portfolio")
    rep.add_argument("--symptom", default="Contact button produces 404 because it points to /contact-us instead of /contact")

    # download-model
    dl = subparsers.add_parser("download-model", help="Download compatible Qwen GGUF model weights")
    dl.add_argument("--model", choices=["qwen2.5-coder-7b-q4", "qwen2.5-coder-3b-q4", "qwen2.5-coder-1.5b-q4"], default="qwen2.5-coder-7b-q4", help="Model variant to download")

    # serve
    srv = subparsers.add_parser("serve", help="Launch Ornàment Web UI & API Server")
    srv.add_argument("--port", type=int, default=settings.port)

    args = parser.parse_args()
    if args.command == "telemetry":
        cmd_telemetry(args)
    elif args.command == "download-model":
        from ornament.models.downloader import ModelDownloader
        path = ModelDownloader.download_model(args.model)
        console.print(f"[bold green][OK] Model ready at: {path}[/bold green]")
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "audit":
        cmd_audit(args)
    elif args.command == "benchmark":
        cmd_benchmark(args)
    elif args.command == "test":
        cmd_test(args)
    elif args.command == "repair":
        cmd_repair(args)
    elif args.command == "serve":
        cmd_serve(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

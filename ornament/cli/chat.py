"""
Interactive Terminal Chat for Ornàment Qwen 2.5 Coder Model.
Enables real-time conversation directly with the downloaded local GGUF weights.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from ornament.config import settings

console = Console()

def run_chat(model_path: Path = None):
    try:
        from llama_cpp import Llama
    except ImportError:
        console.print("[bold red][!] llama-cpp-python is not installed. Run: pip install llama-cpp-python[/bold red]")
        return

    weights = model_path or (settings.base_dir / "ai-website-engineer-model" / "weights" / "qwen2.5-coder-3b-instruct-q4_k_m.gguf")

    if not weights.exists():
        console.print(f"[bold red][!] Model file not found at: {weights}[/bold red]")
        console.print("[yellow]Download it first using: python -m ornament.cli.main download-model --model qwen2.5-coder-3b-q4[/yellow]")
        return

    console.print(Panel(
        f"[bold cyan]Ornàment Local Model Chat[/bold cyan]\n"
        f"[green]Model:[/green] Qwen2.5-Coder-3B-Instruct (4-bit GGUF)\n"
        f"[green]Weights:[/green] {weights.name} ({weights.stat().st_size / (1024**3):.2f} GB)\n"
        f"[yellow]Type 'exit', 'quit', or 'q' to end the conversation.[/yellow]",
        title="🤖 AI Website Engineer",
        border_style="indigo"
    ))

    console.print("[dim]Loading model weights into memory...[/dim]")
    llm = Llama(
        model_path=str(weights),
        n_ctx=4096,
        n_threads=6,
        verbose=False
    )
    console.print("[bold green][✓] Model loaded! Start typing your messages below:[/bold green]\n")

    system_prompt = (
        "You are Qwen2.5-Coder-3B, an expert autonomous AI website engineer in the Ornàment system. "
        "You write production-quality, accessible, clean HTML5, modern CSS, and TypeScript code. "
        "You are concise, helpful, and follow the minimal change policy."
    )

    history = [{"role": "system", "content": system_prompt}]

    while True:
        try:
            user_input = console.input("[bold cyan]You > [/bold cyan]").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("\n[yellow]Goodbye![/yellow]")
                break

            history.append({"role": "user", "content": user_input})

            console.print("[bold magenta]Qwen3B > [/bold magenta]", end="")
            
            # Streaming output
            full_response = ""
            for chunk in llm.create_chat_completion(
                messages=history,
                max_tokens=1024,
                temperature=0.7,
                stream=True
            ):
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    print(content, end="", flush=True)
                    full_response += content

            print("\n")
            history.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            console.print("\n[yellow]Chat ended by user.[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red][!] Error: {e}[/red]\n")

if __name__ == "__main__":
    run_chat()

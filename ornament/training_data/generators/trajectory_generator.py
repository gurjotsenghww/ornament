"""
Agent Trajectory Generator for the Ornàment Training Data System (Section 21).
Synthesizes multi-turn agentic workflows:
  User Request -> Architect Plan -> Subagent Assignment -> Tool Calls -> File Changes -> Test Verification -> Result
"""

from typing import List, Dict, Any

TRAJECTORY_TEMPLATES = [
    {
        "user_request": "Build an ultra-modern developer portfolio with dark theme, Next.js 14 App Router, and responsive navigation.",
        "plan": [
            "1. Inspect hardware bounds and initialize sandboxed workspace.",
            "2. Scaffold package.json with React 18, Next 14, and Tailwind CSS.",
            "3. Generate accessible Navbar component with verified /contact routing.",
            "4. Construct app/page.tsx with hero, selected works bento grid, and metrics.",
            "5. Execute Level 1 Static, Level 2 Build, and Level 7 A11y tests."
        ],
        "subagent_tasks": [
            {"agent": "MainAgent", "role": "Architect", "action": "Decompose task and verify free VRAM > 1GB"},
            {"agent": "CodeAgent", "role": "Coder", "action": "Generate app/layout.tsx, app/page.tsx, components/Navbar.tsx"},
            {"agent": "TestAgent", "role": "Verifier", "action": "Run MultiLevelTestHarness Levels 1, 2, 4, 7"}
        ],
        "tool_calls": [
            {"tool": "file_manager.create_file", "path": "package.json"},
            {"tool": "file_manager.create_file", "path": "app/page.tsx"},
            {"tool": "test_runner.run_level1_static", "result": "PASS"},
            {"tool": "git_ops.create_checkpoint", "commit": "a1b2c3d4"}
        ],
        "final_result": "SUCCESS: Portfolio scaffolded with 10 files, git checkpoint created, 100% test pass rate."
    }
]

def generate_trajectories(count: int) -> List[Dict[str, Any]]:
    """Generates 'count' agentic workflow trajectory examples."""
    results = []
    for i in range(count):
        tmpl = TRAJECTORY_TEMPLATES[i % len(TRAJECTORY_TEMPLATES)]
        results.append({
            "instruction": tmpl["user_request"],
            "plan": tmpl["plan"],
            "subagent_tasks": tmpl["subagent_tasks"],
            "tool_calls": tmpl["tool_calls"],
            "output": tmpl["final_result"],
            "metadata": {
                "category": "trajectory",
                "difficulty": "advanced",
                "source_type": "generated",
                "license": "MIT"
            }
        })
    return results
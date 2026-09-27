"""
Debugging Trajectory Generator for the Ornàment Training Data System (Section 20).
Generates problem -> code_before -> error -> diagnosis -> minimal_fix -> test -> result trajectories
essential for Ornàment's autonomous self-healing capabilities.
"""

from typing import List, Dict, Any

DEBUGGING_ARCHETYPES = [
    {
        "problem": "Navigation contact button points to non-existent route /contact-us returning 404.",
        "code_before": """<nav aria-label="Main Navigation" class="flex items-center space-x-6">
  <a href="/about" class="text-zinc-400 hover:text-white">About</a>
  <a href="/projects" class="text-zinc-400 hover:text-white">Projects</a>
  <a id="nav-contact-button" href="/contact-us" class="px-4 py-2 bg-indigo-600 text-white rounded">Contact</a>
</nav>""",
        "error": "404 Not Found: Route /contact-us does not exist on preview dev server.",
        "diagnosis": "Route mismatch: Navbar component points to '/contact-us' but active router endpoint is '/contact'.",
        "minimal_fix": """-  <a id="nav-contact-button" href="/contact-us" class="px-4 py-2 bg-indigo-600 text-white rounded">Contact</a>
+  <a id="nav-contact-button" href="/contact" class="px-4 py-2 bg-indigo-600 text-white rounded">Contact</a>""",
        "test": "Playwright Level 4: Click #nav-contact-button and assert target route is /contact with HTTP 200.",
        "result": "passed"
    },
    {
        "problem": "Hero section headshot image fails Level 7 Accessibility audit due to missing alt attribute.",
        "code_before": """<div class="relative w-32 h-32 rounded-full overflow-hidden border-2 border-indigo-500">
  <img src="/images/avatar.jpg" class="w-full h-full object-cover" />
</div>""",
        "error": "WCAG 2.1 Level A Violation: <img> element missing required 'alt' attribute.",
        "diagnosis": "Screen readers cannot announce image content; missing descriptive alt text for avatar photo.",
        "minimal_fix": """-  <img src="/images/avatar.jpg" class="w-full h-full object-cover" />
+  <img src="/images/avatar.jpg" alt="Profile avatar of Senior AI Systems Architect" class="w-full h-full object-cover" />""",
        "test": "MultiLevelTestHarness Level 7: Run accessibility validator and assert zero missing alt attributes.",
        "result": "passed"
    },
    {
        "problem": "Search input in navigation lacks accessible label causing screen reader silence.",
        "code_before": """<form role="search" class="flex items-center">
  <input type="text" class="px-3 py-1 bg-zinc-800 text-white rounded" />
  <button type="submit">Search</button>
</form>""",
        "error": "WCAG A11y Error: Form control element <input type=\"text\"> lacks accessible label or aria-label.",
        "diagnosis": "The input has no <label for=...> and no aria-label attribute.",
        "minimal_fix": """-  <input type="text" class="px-3 py-1 bg-zinc-800 text-white rounded" />
+  <input type="text" aria-label="Search documentation" placeholder="Search documentation..." class="px-3 py-1 bg-zinc-800 text-white rounded" />""",
        "test": "Level 7 Accessibility Audit: Check aria-label accessibility mapping on all input controls.",
        "result": "passed"
    },
    {
        "problem": "Modal backdrop renders behind sticky navbar due to missing z-index stacking hierarchy.",
        "code_before": """.sticky-header {
  position: sticky;
  top: 0;
  z-index: 50;
}
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 40;
}""",
        "error": "Visual clipping: Sticky header obscures modal dialog backdrop and title bar.",
        "diagnosis": "Modal z-index (40) is lower than sticky-header z-index (50). Modals must stack above navigation.",
        "minimal_fix": """-  z-index: 40;
+  z-index: 100;""",
        "test": "Playwright Level 4: Assert modal element is on top of navigation bar when opened.",
        "result": "passed"
    },
    {
        "problem": "Mobile layout breaks with horizontal scrollbar caused by fixed pixel width container.",
        "code_before": """<main class="w-[1200px] mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold">Systems Overview</h1>
</main>""",
        "error": "Responsive Design Failure: Layout width exceeds viewport on mobile screen (375px).",
        "diagnosis": "Hardcoded width w-[1200px] prevents mobile responsiveness. Should use max-w-7xl w-full.",
        "minimal_fix": """-<main class="w-[1200px] mx-auto px-4 py-8">
+<main class="w-full max-w-7xl mx-auto px-4 py-8">""",
        "test": "Playwright Level 4: Emulate iPhone viewport (375px) and assert document.body.scrollWidth == window.innerWidth.",
        "result": "passed"
    },
    {
        "problem": "Form button without explicit type causes unintentional form submission on click.",
        "code_before": """<form class="space-y-4">
  <input type="email" placeholder="Email address" required />
  <button class="bg-zinc-800 text-white px-3 py-1" onclick="toggleAdvancedOptions()">Options</button>
  <button type="submit" class="bg-indigo-600 text-white px-4 py-2">Submit</button>
</form>""",
        "error": "Runtime Form Bug: Clicking 'Options' triggers HTML form submission and page refresh.",
        "diagnosis": "HTML default type for <button> inside a <form> is 'submit'. Auxiliary buttons must specify type='button'.",
        "minimal_fix": """-  <button class="bg-zinc-800 text-white px-3 py-1" onclick="toggleAdvancedOptions()">Options</button>
+  <button type="button" class="bg-zinc-800 text-white px-3 py-1" onclick="toggleAdvancedOptions()">Options</button>""",
        "test": "Playwright Level 4: Click 'Options' button and assert page URL does not reload or submit.",
        "result": "passed"
    },
    {
        "problem": "Unclosed div tag causes layout hierarchy to collapse below hero section.",
        "code_before": """<section class="hero-wrapper">
  <div class="content-box">
    <h1>Autonomous Platform</h1>
    <p>Engineered for high performance.</p>
</section>
<section class="features">
  <h2>Features</h2>
</section>""",
        "error": "HTML Syntax Warning: Expected closing tag </div> for element opened on line 2.",
        "diagnosis": "Missing </div> before </section> causes subsequent features section to be nested inside hero content-box.",
        "minimal_fix": """     <p>Engineered for high performance.</p>
+  </div>
 </section>""",
        "test": "HtmlValidator & Level 1 Static: Assert balanced tag stack with zero unmatched tags.",
        "result": "passed"
    }
]

def generate_debugging(count: int) -> List[Dict[str, Any]]:
    """Generates 'count' realistic web debugging trajectory examples."""
    results = []
    for i in range(count):
        archetype = DEBUGGING_ARCHETYPES[i % len(DEBUGGING_ARCHETYPES)]
        results.append({
            "instruction": f"Diagnose and provide minimal fix for: {archetype['problem']}",
            "context": {
                "framework": "Web Engineering / Minimal Change Policy",
                "test": archetype["test"]
            },
            "output": f"Diagnosis:\n{archetype['diagnosis']}\n\nMinimal Patch:\n```diff\n{archetype['minimal_fix']}\n```\n\nVerification:\n{archetype['test']} -> {archetype['result']}",
            "metadata": {
                "category": "debugging",
                "difficulty": "medium",
                "problem": archetype["problem"],
                "code_before": archetype["code_before"],
                "error": archetype["error"],
                "diagnosis": archetype["diagnosis"],
                "minimal_fix": archetype["minimal_fix"],
                "test": archetype["test"],
                "result": archetype["result"],
                "source_type": "generated",
                "license": "MIT"
            }
        })
    return results

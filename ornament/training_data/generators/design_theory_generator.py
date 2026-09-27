"""
Design Theory, Aesthetics, and Modern Web Craft Generator for Ornàment.
Generates instruction-response training pairs teaching:
1. Mathematical Typographic & Spatial Harmony (Major Third, Perfect Fourth, 8pt grid)
2. 60-30-10 Color Architecture & Dark Luxury Principles (OKLCH, OLED surfaces, contrast)
3. Modern Next-Gen CSS Architecture (Container Queries with container-type, clamp(), Subgrid)
4. Award-Winning UI Aesthetics (Bento grids, inner bevel glow, micro-interactions, spring physics)
5. Agentic Minimal Change Policy (Surgical diffs, root cause diagnosis)
"""

import json
from pathlib import Path
from typing import List, Dict, Any

DESIGN_THEORY_PAIRS: List[Dict[str, Any]] = [
    # --- Category: Typographic & Spatial Systems ---
    {
        "category": "typography_systems",
        "instruction": "Explain the exact mathematical ratio of the Perfect Fourth versus the Major Third typographic scale, and provide an 8-point spatial token system for modern web design.",
        "input": "",
        "output": (
            "### 1. Typographic Scale Ratios\n"
            "A modular typographic scale derives all font sizes from a base size (typically 16px / 1rem) multiplied by a fixed geometric ratio:\n\n"
            "- **Major Third (1.250 / 5:4 ratio)**:\n"
            "  Best for content-dense applications, dashboards, and editorial interfaces where subtle hierarchy is required without excessive vertical consumption.\n"
            "  - Base (Body): 16px (1.000rem)\n"
            "  - Small (Caption): 12.8px (0.800rem)\n"
            "  - Large (H4): 20px (1.250rem)\n"
            "  - X-Large (H3): 25px (1.563rem)\n"
            "  - 2X-Large (H2): 31.25px (1.953rem)\n"
            "  - 3X-Large (H1): 39.06px (2.441rem)\n\n"
            "- **Perfect Fourth (1.333 / 4:3 ratio)**:\n"
            "  Best for high-impact marketing, luxury portfolios, and SaaS landing pages requiring dramatic contrast between display headlines and body copy.\n"
            "  - Base (Body): 16px (1.000rem)\n"
            "  - Small: 12px (0.750rem)\n"
            "  - H4: 21.33px (1.333rem)\n"
            "  - H3: 28.44px (1.777rem)\n"
            "  - H2: 37.92px (2.369rem)\n"
            "  - H1: 50.55px (3.159rem)\n\n"
            "*(Note: The 1.500 ratio is the Perfect Fifth, NOT the Perfect Fourth.)*\n\n"
            "### 2. The 8-Point Spatial Grid System\n"
            "All spacing (padding, margin, gap, sizing) must be multiples of 8px (with a 4px sub-unit for tight UI micro-spacing):\n"
            "- `space-1` (4px): Micro gaps (inline badges, icon offsets)\n"
            "- `space-2` (8px): Tight component padding (compact buttons, tag pills)\n"
            "- `space-3` (12px): Standard button vertical padding, form input offsets\n"
            "- `space-4` (16px): Card internal padding, standard layout gaps\n"
            "- `space-6` (24px): Medium container padding, grid gaps\n"
            "- `space-8` (32px): Card-to-card spacing, desktop section gutters\n"
            "- `space-12` (48px): Section rhythm spacing\n"
            "- `space-16` (64px): Hero and primary section separation\n"
            "- `space-24` (96px+): Dramatic breathing room in luxury editorial layouts"
        ),
        "metadata": {"category": "typography_systems", "difficulty": "expert", "tokens": 420}
    },
    
    # --- Category: Dark Luxury Color Architecture ---
    {
        "category": "color_architecture",
        "instruction": "How do you correctly implement the 60-30-10 color rule for an ultra-modern dark luxury web application? Provide specific Tailwind and hex tokens.",
        "input": "",
        "output": (
            "### The 60-30-10 Rule in Modern Dark Luxury Architecture\n\n"
            "In dark luxury design, we never use pure pitch black (#000000) or pure white (#ffffff) for large surfaces, as this causes harsh visual vibration, optical fatigue, and cheapens the aesthetic.\n\n"
            "1. **60% Dominant Base (Canvas & Negative Space)**:\n"
            "   - Deep, warm-tinted obsidian or zinc base: `#09090b` (`bg-zinc-950`).\n"
            "   - Gives depth, allows illuminated components to float, and supports OLED power efficiency.\n\n"
            "2. **30% Secondary Structure (Surfaces, Cards, Borders & Structural Text)**:\n"
            "   - Layered elevation surfaces: `#18181b` (`bg-zinc-900/60`) with backdrop blur (`backdrop-blur-xl`).\n"
            "   - Subtle translucent borders: `border border-white/10` or `border-zinc-800/80` to define spatial boundaries without heavy drop-shadows.\n"
            "   - Body & supporting typography: `#a1a1aa` (`text-zinc-400`) and `#f4f4f5` (`text-zinc-100`) for headers, ensuring strict WCAG AAA contrast (>7:1).\n\n"
            "3. **10% High-Energy Accent (Focal Points & Primary CTAs)**:\n"
            "   - Vibrant, restrained accent: e.g. Electric Violet (`#6366f1` / `indigo-500`) or Emerald Glow (`#10b981`).\n"
            "   - Applied exclusively to primary CTAs, active status indicators, and subtle radial gradient glow backdrops (`bg-radial-gradient`)."
        ),
        "metadata": {"category": "color_architecture", "difficulty": "expert", "tokens": 360}
    },

    # --- Category: Modern CSS Container Queries ---
    {
        "category": "css_architecture",
        "instruction": "Demonstrate how to properly write a CSS Container Query component. Why must container-type be declared on the parent, and how does it differ from a viewport media query?",
        "input": "",
        "output": (
            "### CSS Container Queries: Correct Implementation\n\n"
            "Unlike `@media` queries that listen to the global viewport width, `@container` queries evaluate against the dimensions of the immediate parent container. This enables **true component modularity**—a card component will adapt identically whether placed in a narrow 300px sidebar or an 800px main content feed.\n\n"
            "#### Critical Requirement:\n"
            "A container query **will fail silently** unless the parent element establishes a containment context using `container-type: inline-size` (or `size`) and an optional `container-name`.\n\n"
            "```css\n"
            "/* 1. Parent establishes containment context */\n"
            ".card-wrapper {\n"
            "  container-type: inline-size;\n"
            "  container-name: feature-card;\n"
            "  width: 100%;\n"
            "}\n"
            "\n"
            "/* 2. Default mobile / narrow container layout (Stacked) */\n"
            ".feature-item {\n"
            "  display: flex;\n"
            "  flex-direction: column;\n"
            "  gap: 1rem;\n"
            "  padding: 1.25rem;\n"
            "  background: #18181b;\n"
            "  border: 1px solid rgba(255, 255, 255, 0.1);\n"
            "  border-radius: 1rem;\n"
            "}\n"
            "\n"
            "/* 3. When the PARENT container exceeds 520px (Horizontal Row) */\n"
            "@container feature-card (min-width: 520px) {\n"
            "  .feature-item {\n"
            "    flex-direction: row;\n"
            "    align-items: center;\n"
            "    padding: 2rem;\n"
            "  }\n"
            "  .feature-item img {\n"
            "    width: 140px;\n"
            "    height: 140px;\n"
            "  }\n"
            "}\n"
            "```"
        ),
        "metadata": {"category": "css_architecture", "difficulty": "expert", "tokens": 380}
    },

    # --- Category: High-End UI Component Elevation ---
    {
        "category": "component_craft",
        "instruction": "Transform a standard generic button into an award-winning, luxury dark-mode button using modern Tailwind CSS with micro-interactions, inner bevels, and spring physics.",
        "input": "<button class=\"bg-blue-600 text-white px-4 py-2 rounded\">Click Here</button>",
        "output": (
            "### Award-Winning Luxury Component Transformation\n\n"
            "#### Aesthetic Deficiencies in Original:\n"
            "- Flat saturated primary blue (#2563eb) looks like default Bootstrap\n"
            "- Lacks depth, tactile feedback, and focus-visible rings\n"
            "- Generic verb \"Click Here\" violates accessible UX guidelines\n\n"
            "#### Elevated Tailwind Implementation:\n"
            "```html\n"
            "<button \n"
            "  type=\"button\"\n"
            "  class=\"group relative inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl\n"
            "         bg-gradient-to-b from-zinc-800 to-zinc-900 \n"
            "         text-xs font-semibold tracking-wide text-zinc-100\n"
            "         border border-white/10\n"
            "         shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15),0_4px_12px_rgba(0,0,0,0.4)]\n"
            "         hover:border-white/20 hover:from-zinc-700 hover:to-zinc-800 hover:text-white\n"
            "         active:scale-[0.98] active:shadow-inner\n"
            "         focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 focus-visible:ring-offset-zinc-950\n"
            "         transition-all duration-200 ease-[cubic-bezier(0.16,1,0.3,1)]\"\n"
            ">\n"
            "  <span>Deploy Application</span>\n"
            "  <svg class=\"w-3.5 h-3.5 text-zinc-400 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition-all duration-200\" \n"
            "       fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\">\n"
            "    <path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M13 7l5 5m0 0l-5 5m5-5H6\" />\n"
            "  </svg>\n"
            "</button>\n"
            "```\n\n"
            "#### Craft Details:\n"
            "1. **Inner Bevel Highlight**: `shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15)]` simulates light catching the top glass edge.\n"
            "2. **Spring Physics**: `cubic-bezier(0.16, 1, 0.3, 1)` gives a snappy, luxurious micro-interaction.\n"
            "3. **Tactile Depress**: `active:scale-[0.98]` creates authentic physical response on click.\n"
            "4. **Accessibility**: Explicit `focus-visible:ring-offset-zinc-950` prevents keyboard focus ring collision."
        ),
        "metadata": {"category": "component_craft", "difficulty": "expert", "tokens": 480}
    },

    # --- Category: Minimal Change Policy Surgical Diff ---
    {
        "category": "minimal_change_policy",
        "instruction": "A developer reports that a website header has an unclosed tag causing DOM tree breakdown. Follow Ornàment's Minimal Change Policy: Diagnose the bug and output ONLY the surgical diff replacement.",
        "input": (
            "```html\n"
            "<header class=\"sticky top-0 z-50 bg-zinc-950/80 backdrop-blur\">\n"
            "  <div class=\"max-w-7xl mx-auto flex items-center justify-between p-4\">\n"
            "    <a href=\"/\" class=\"text-white font-bold\">Ornàment</a>\n"
            "    <nav class=\"flex gap-4\">\n"
            "      <a href=\"/docs\" class=\"text-zinc-400\">Docs</a>\n"
            "      <a href=\"/pricing\" class=\"text-zinc-400\">Pricing</a>\n"
            "    </div>\n"
            "  </div>\n"
            "</header>\n"
            "```"
        ),
        "output": (
            "### Root Cause Diagnosis:\n"
            "The `<nav>` tag is improperly closed with a `</div>` tag on line 7, causing an invalid DOM tree structure and broken parent hierarchy.\n\n"
            "### Surgical Replacement (Minimal Change Policy):\n"
            "```diff\n"
            "-    </div>\n"
            "+    </nav>\n"
            "```\n\n"
            "```json\n"
            "{\n"
            "  \"target_file\": \"header.html\",\n"
            "  \"target_content\": \"    </div>\\n  </div>\",\n"
            "  \"replacement_content\": \"    </nav>\\n  </div>\",\n"
            "  \"lines_changed\": 1\n"
            "}\n"
            "```"
        ),
        "metadata": {"category": "minimal_change_policy", "difficulty": "expert", "tokens": 260}
    }
]

class DesignTheoryGenerator:
    """Generates synthetic design theory and aesthetic craft training examples."""

    @classmethod
    def generate(cls, target_count: int = 100) -> List[Dict[str, Any]]:
        results = []
        base_pairs = DESIGN_THEORY_PAIRS
        
        # Extend with procedural variations across categories
        archetypes = [
            ("Minimal Luxury", "monochromatic obsidian, warm zinc-950, 1px subtle white/10 borders, serif headers with clean sans body"),
            ("Swiss Editorial", "strict grid alignment, bold asymmetric typography, high contrast, generous negative space, geometric discipline"),
            ("Bento Grid SaaS", "multi-cell asymmetrical bento grid, rounded-2xl cards, glowing radial gradients, feature badges, interactive tabs"),
            ("Cyberpunk Glass", "dark translucent glassmorphism, neon cyan/violet accent glows, backdrop-blur-2xl, monospace telemetry fonts"),
            ("Neo-Brutalist", "high-contrast solid borders (2px black), drop-shadow-[4px_4px_0_0_#000], bold uppercase typography, playful tactile buttons")
        ]

        component_types = [
            ("Hero Section", "with floating telemetry badges, fluid typography clamp(), and responsive CTA group"),
            ("Navbar", "with sticky blur backdrop, keyboard-navigable dropdown, and mobile drawer toggle"),
            ("Pricing Matrix", "with tier highlight card, monthly/yearly billing toggle, and feature comparison checklist"),
            ("Feature Bento Grid", "with 3-column asymmetric spans, interactive hover glows, and SVG illustration slots"),
            ("Contact Form", "with floating accessible labels, WCAG compliant error states, and tactile submit button")
        ]

        counter = 1
        # First include the handcrafted master theory pairs
        for p in base_pairs:
            results.append({
                "id": f"theory_{counter:06d}",
                "instruction": p["instruction"],
                "input": p.get("input", ""),
                "output": p["output"],
                "metadata": p.get("metadata", {})
            })
            counter += 1

        # Procedurally synthesize paired design specifications
        for arch_name, arch_desc in archetypes:
            for comp_name, comp_desc in component_types:
                if len(results) >= target_count:
                    break
                
                instruction = (
                    f"Design and engineer a production-ready {comp_name} embodying the {arch_name} aesthetic "
                    f"({comp_desc}). Ensure strict adherence to the 60-30-10 color rule, 8pt spatial grid, "
                    f"and WCAG AA accessibility contrast standards. Provide clean HTML5 + Tailwind CSS."
                )
                
                code_output = (
                    f"### {arch_name} Aesthetic Specification: {comp_name}\n\n"
                    f"**Design Rationale:**\n"
                    f"- **Aesthetic Style:** {arch_name} — utilizing {arch_desc}.\n"
                    f"- **Color Hierarchy:** 60% base canvas (`bg-zinc-950`), 30% structural elevation (`bg-zinc-900/50 border border-white/10`), 10% focal accents.\n"
                    f"- **Spatial System:** 8-point grid rhythm with consistent padding and fluid gap scaling.\n\n"
                    f"```html\n"
                    f"<{ 'section' if 'Section' in comp_name or 'Grid' in comp_name else 'div' } class=\"relative w-full max-w-7xl mx-auto px-6 py-12 bg-zinc-950 text-zinc-100 rounded-3xl border border-zinc-800/80 shadow-2xl overflow-hidden\">\n"
                    f"  <!-- Ambient Glow -->\n"
                    f"  <div class=\"absolute -top-24 -left-24 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none\" aria-hidden=\"true\"></div>\n"
                    f"  \n"
                    f"  <div class=\"relative z-10 space-y-6\">\n"
                    f"    <span class=\"inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-medium bg-zinc-900 border border-zinc-700/60 text-zinc-300\">\n"
                    f"      <span class=\"w-2 h-2 rounded-full bg-emerald-400 animate-pulse\"></span>\n"
                    f"      {arch_name} System\n"
                    f"    </span>\n"
                    f"    <h2 class=\"text-3xl md:text-5xl font-bold tracking-tight text-white leading-tight\">\n"
                    f"      Precision Engineered {comp_name}\n"
                    f"    </h2>\n"
                    f"    <p class=\"max-w-2xl text-base md:text-lg text-zinc-400 font-sans leading-relaxed\">\n"
                    f"      Built with autonomous design intelligence, strict spatial harmonics, and modern tactile micro-interactions.\n"
                    f"    </p>\n"
                    f"  </div>\n"
                    f"</{ 'section' if 'Section' in comp_name or 'Grid' in comp_name else 'div' }>\n"
                    f"```"
                )

                results.append({
                    "id": f"theory_{counter:06d}",
                    "instruction": instruction,
                    "input": "",
                    "output": code_output,
                    "metadata": {
                        "category": "aesthetic_synthesis",
                        "archetype": arch_name,
                        "component": comp_name,
                        "difficulty": "advanced"
                    }
                })
                counter += 1

        return results

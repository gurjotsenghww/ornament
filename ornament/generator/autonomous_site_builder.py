import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from ornament.files.file_manager import FileManager
from ornament.git_ops.checkpoint import GitCheckpointManager
from ornament.config import settings

class AutonomousSiteBuilder:
    """
    Autonomous site builder synthesizing multi-file frontend bundles (HTML, CSS, JS)
    optimized for instant live previews, responsive rendering, and zero-dependency ZIP export.
    Integrates with Ornàment local model inference and design-theory heuristics.
    """

    PALETTES = {
        "indigo": {
            "name": "Electric Indigo",
            "bg": "#09090b",
            "surface": "#121217",
            "surface_hover": "#1a1a22",
            "surface_border": "rgba(255, 255, 255, 0.08)",
            "primary": "#6366f1",
            "primary_hover": "#4f46e5",
            "primary_text": "#a5b4fc",
            "glow": "rgba(99, 102, 241, 0.25)",
            "text": "#f4f4f6",
            "text_muted": "#8e8e9f"
        },
        "emerald": {
            "name": "Emerald Matrix",
            "bg": "#080c09",
            "surface": "#101812",
            "surface_hover": "#162319",
            "surface_border": "rgba(255, 255, 255, 0.08)",
            "primary": "#10b981",
            "primary_hover": "#059669",
            "primary_text": "#6ee7b7",
            "glow": "rgba(16, 185, 129, 0.25)",
            "text": "#f0fdf4",
            "text_muted": "#86958a"
        },
        "cyan": {
            "name": "Cyber Neon Cyan",
            "bg": "#080c12",
            "surface": "#0f1722",
            "surface_hover": "#172333",
            "surface_border": "rgba(255, 255, 255, 0.08)",
            "primary": "#06b6d4",
            "primary_hover": "#0891b2",
            "primary_text": "#67e8f9",
            "glow": "rgba(6, 182, 212, 0.25)",
            "text": "#f0f9ff",
            "text_muted": "#8297ab"
        },
        "amber": {
            "name": "Warm Luxury Amber",
            "bg": "#0c0a08",
            "surface": "#181410",
            "surface_hover": "#221c16",
            "surface_border": "rgba(255, 255, 255, 0.08)",
            "primary": "#f59e0b",
            "primary_hover": "#d97706",
            "primary_text": "#fcd34d",
            "glow": "rgba(245, 158, 11, 0.25)",
            "text": "#fffbeb",
            "text_muted": "#9d9082"
        },
        "violet": {
            "name": "Deep Royal Violet",
            "bg": "#0a0812",
            "surface": "#141022",
            "surface_hover": "#1e1832",
            "surface_border": "rgba(255, 255, 255, 0.08)",
            "primary": "#8b5cf6",
            "primary_hover": "#7c3aed",
            "primary_text": "#c4b5fd",
            "glow": "rgba(139, 92, 246, 0.25)",
            "text": "#f5f3ff",
            "text_muted": "#8f8aa1"
        }
    }

    @classmethod
    def detect_palette(cls, prompt: str) -> Dict[str, str]:
        p = prompt.lower()
        if any(w in p for w in ["emerald", "green", "finance", "money", "crypto", "trading", "invest", "eco", "nature"]):
            return cls.PALETTES["emerald"]
        elif any(w in p for w in ["cyan", "blue", "tech", "cloud", "api", "infra", "ai", "cyber", "terminal"]):
            return cls.PALETTES["cyan"]
        elif any(w in p for w in ["amber", "gold", "luxury", "coffee", "restaurant", "food", "warm", "bakery", "cafe", "furniture"]):
            return cls.PALETTES["amber"]
        elif any(w in p for w in ["violet", "purple", "creative", "design", "art", "music", "agency", "media"]):
            return cls.PALETTES["violet"]
        return cls.PALETTES["indigo"]

    @classmethod
    def derive_brand_and_title(cls, prompt: str) -> tuple[str, str, str]:
        """Returns (brand_name, hero_title, hero_subtitle)"""
        clean = prompt.strip()
        lines = [line.strip() for line in clean.splitlines() if line.strip()]
        first_line = lines[0] if lines else "Autonomous Experience"

        # Check for explicitly named brand
        match_for = re.search(r"(?:for|named|called)\s+([A-Z][a-zA-Z0-9_\s]{2,20})", first_line)
        if match_for:
            brand = match_for.group(1).strip()
        else:
            words = [w for w in re.split(r"[^\w]", first_line) if len(w) > 3]
            brand = words[0].capitalize() if words else "Ornàment"

        # Hero Title
        title_candidates = re.split(r"[.!?\n]", clean)
        title = title_candidates[0].strip() if title_candidates else clean
        if len(title) > 60:
            title = title[:57] + "..."
        if not title:
            title = f"Next-Generation {brand}"

        # Subtitle
        if len(title_candidates) > 1 and len(title_candidates[1].strip()) > 10:
            subtitle = title_candidates[1].strip()
        else:
            subtitle = f"Engineered for high performance, intuitive interaction, and modern aesthetics."

        return brand, title, subtitle

    _llm_instance = None

    @classmethod
    def get_qwen_model(cls):
        """Lazy loads local Qwen2.5-Coder-3B-Instruct GGUF model via llama-cpp-python on CPU."""
        if cls._llm_instance is None:
            try:
                from llama_cpp import Llama
                weights = settings.base_dir / "ai-website-engineer-model" / "weights" / "qwen2.5-coder-3b-instruct-q4_k_m.gguf"
                if weights.exists():
                    cls._llm_instance = Llama(
                        model_path=str(weights),
                        n_ctx=2048,
                        n_threads=4,
                        verbose=False
                    )
            except Exception as e:
                print(f"[AutonomousSiteBuilder] Failed to initialize Qwen: {e}")
                cls._llm_instance = None
        return cls._llm_instance

    @classmethod
    def query_qwen(cls, prompt: str, attachments_text: str = "") -> Optional[Dict[str, Any]]:
        """Queries local Qwen2.5-Coder-3B for bespoke brand architecture, features, and styling."""
        llm = cls.get_qwen_model()
        if not llm:
            return None
        try:
            user_content = prompt
            if attachments_text:
                user_content += f"\n\nContext:\n{attachments_text}"

            system_prompt = (
                "You are Ornàment, an elite autonomous website engineer powered by Qwen2.5-Coder-3B. "
                "Synthesize high-conversion, modern website specifications for the user request. "
                "Respond strictly with valid JSON having the following schema:\n"
                "{\n"
                '  "brand": "Brand Name",\n'
                '  "title": "Hero Headline",\n'
                '  "subtitle": "Clear, persuasive subheadline",\n'
                '  "palette_theme": "indigo|emerald|cyan|amber|violet",\n'
                '  "features": [\n'
                '    {"title": "Feature 1", "description": "Crisp 1-2 sentence description", "badge": "Short Badge"},\n'
                '    {"title": "Feature 2", "description": "Crisp 1-2 sentence description", "badge": "Short Badge"},\n'
                '    {"title": "Feature 3", "description": "Crisp 1-2 sentence description", "badge": "Short Badge"}\n'
                "  ],\n"
                '  "explanation": "Professional engineering breakdown of the generated architecture"\n'
                "}"
            )

            res = llm.create_chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=450,
                temperature=0.3
            )
            raw = res["choices"][0]["message"]["content"]
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception as e:
            print(f"[AutonomousSiteBuilder] Qwen query exception: {e}")
        return None

    @classmethod
    def query_qwen_for_code(cls, prompt: str, attachments_text: str = "") -> Optional[Dict[str, Any]]:
        """
        Queries local Qwen2.5-Coder-3B to generate complete, tailored HTML, CSS, JS code
        specifically matching the user's requirements (e.g. form, calculator, landing page, app).
        """
        llm = cls.get_qwen_model()
        if not llm:
            return None
        try:
            system_prompt = (
                "You are an elite autonomous web developer and UI engineer powered by Qwen2.5-Coder. "
                "Write high-quality, modern, accessible, beautiful code tailored EXACTLY to the user's request. "
                "If the user asks for a specific component (e.g. form, calculator, table, login, dashboard) or a full page, "
                "build what they asked for directly with clean semantic HTML5, modern CSS, and interactive JavaScript.\n"
                "Output your response strictly using these code blocks:\n"
                "```html\n"
                "<!DOCTYPE html>\n"
                "<html lang=\"en\">\n"
                "<head>\n"
                "  <meta charset=\"UTF-8\" />\n"
                "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
                "  <title>...</title>\n"
                "  <link rel=\"stylesheet\" href=\"styles.css\" />\n"
                "  <script defer src=\"script.js\"></script>\n"
                "</head>\n"
                "<body>\n"
                "...\n"
                "</body>\n"
                "</html>\n"
                "```\n"
                "```css\n"
                "/* styles.css */\n"
                "...\n"
                "```\n"
                "```js\n"
                "/* script.js */\n"
                "...\n"
                "```\n"
                "Followed by a concise 1-2 sentence explanation of what you created."
            )
            user_msg = f"User Request: {prompt}"
            if attachments_text:
                user_msg += f"\nAdditional Context:\n{attachments_text}"

            res = llm.create_chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                max_tokens=950,
                temperature=0.3
            )
            raw = res["choices"][0]["message"]["content"]

            # Extract HTML block
            html_match = re.search(r"```html\s*([\s\S]*?)```", raw, re.IGNORECASE)
            html_code = html_match.group(1).strip() if html_match else ""

            # Extract CSS block
            css_match = re.search(r"```css\s*([\s\S]*?)```", raw, re.IGNORECASE)
            css_code = css_match.group(1).strip() if css_match else ""

            # Extract JS block
            js_match = re.search(r"```(?:js|javascript)\s*([\s\S]*?)```", raw, re.IGNORECASE)
            js_code = js_match.group(1).strip() if js_match else ""

            # Extract inline style or script if not separated
            if html_code and not css_code:
                style_match = re.search(r"<style[^>]*>([\s\S]*?)</style>", html_code, re.IGNORECASE)
                if style_match:
                    css_code = style_match.group(1).strip()
            if html_code and not js_code:
                script_match = re.search(r"<script[^>]*>([\s\S]*?)</script>", html_code, re.IGNORECASE)
                if script_match and 'src=' not in script_match.group(0).lower():
                    js_code = script_match.group(1).strip()

            clean_text = re.sub(r"```[\s\S]*?```", "", raw).strip()
            explanation = clean_text if clean_text else "Custom code synthesized by Qwen 2.5 Coder to match your exact specification."

            if html_code:
                # Ensure HTML links to styles.css and script.js
                if css_code and '<link rel="stylesheet" href="styles.css"' not in html_code:
                    if '</head>' in html_code:
                        html_code = html_code.replace('</head>', '  <link rel="stylesheet" href="styles.css" />\n</head>')
                if js_code and '<script defer src="script.js"' not in html_code and '<script src="script.js"' not in html_code:
                    if '</body>' in html_code:
                        html_code = html_code.replace('</body>', '  <script defer src="script.js"></script>\n</body>')
                    else:
                        html_code += '\n<script defer src="script.js"></script>'

                return {
                    "html": html_code,
                    "css": css_code or "/* Custom styles for this project */\nbody { font-family: system-ui, sans-serif; }",
                    "js": js_code or "// Interactive functionality\nconsole.log('App initialized');",
                    "explanation": explanation
                }
        except Exception as e:
            print(f"[AutonomousSiteBuilder] Qwen code query exception: {e}")
        return None

    @classmethod
    def generate_site_bundle(
        cls,
        prompt: str,
        attachments: Optional[List[Dict[str, Any]]] = None,
        project_name: Optional[str] = None,
        model: str = "qwen"
    ) -> Dict[str, Any]:
        """
        Synthesizes the complete 3-file site: index.html, styles.css, script.js,
        accompanied by an architectural explanation and project persistence.
        Uses actual Qwen 2.5 Coder neural generation when selected.
        """
        palette = cls.detect_palette(prompt)
        brand, title, subtitle = cls.derive_brand_and_title(prompt)
        qwen_code_result = None
        model_name = "Orn\u00e0ment Instant Synthesizer"

        # Incorporate attachments context if provided
        attachment_notes = ""
        attachment_text = ""
        if attachments:
            for att in attachments:
                if att.get("type") == "text" and att.get("content"):
                    c = att.get("content")[:120]
                    attachment_notes += f"\n<!-- Attached context: {c} -->"
                    attachment_text += f"{c}\n"

        # Query Qwen 2.5 Coder for ACTUAL code if requested
        if model and model.lower() in ["qwen", "qwen2.5", "neural"]:
            qwen_code_result = cls.query_qwen_for_code(prompt, attachment_text)
            if qwen_code_result:
                model_name = "Orn\u00e0 2.5 Coder (Neural 3B)"

        # Sanitize project slug
        if not project_name:
            slug = re.sub(r"[^a-z0-9]+", "-", brand.lower()).strip("-")
            project_name = slug if slug else f"site-{int(Path('.').stat().st_mtime)}"

        if qwen_code_result:
            html_content = qwen_code_result["html"]
            css_content = qwen_code_result["css"]
            js_content = qwen_code_result["js"]
            explanation = (
                f"Generated with **{model_name}** tailored specifically to your request.\n\n"
                f"{qwen_code_result['explanation']}\n\n"
                f"- `index.html`: Production-ready markup structured specifically for your prompt.\n"
                f"- `styles.css`: Bespoke modern styling, responsive layout, and visual refinements.\n"
                f"- `script.js`: Interactive behavior and client logic."
            )
        else:
            # Fallback to deterministic design system generator
            html_content = cls._build_html(
                brand=brand,
                title=title,
                subtitle=subtitle,
                palette=palette,
                prompt=prompt,
                attachment_notes=attachment_notes,
                features=None,
                model_name=model_name
            )
            css_content = cls._build_css(palette)
            js_content = cls._build_js(brand)
            explanation = (
                f"Synthesized with **{model_name}** for **{brand}** applying the **60-30-10** design system rule with the **{palette['name']}** color theme.\n\n"
                f"- `index.html`: Responsive HTML5 markup with interactive sections and modern hierarchy.\n"
                f"- `styles.css`: Modern CSS with custom properties, fluid clamp() typography, and mobile breakpoints.\n"
                f"- `script.js`: Client-side interactivity including smooth anchor scrolling and form notifications."
            )

        files = [
            {"id": "html", "name": "index.html", "lang": "html", "content": html_content},
            {"id": "css", "name": "styles.css", "lang": "css", "content": css_content},
            {"id": "js", "name": "script.js", "lang": "js", "content": js_content}
        ]

        # Save to workspace for persistence & preview server
        p_dir = settings.workspace_dir / project_name
        p_dir.mkdir(parents=True, exist_ok=True)
        fm = FileManager(p_dir)
        fm.create_file("index.html", html_content, overwrite=True)
        fm.create_file("styles.css", css_content, overwrite=True)
        fm.create_file("script.js", js_content, overwrite=True)

        # Standalone preview HTML for direct iframe mounting
        preview_html = html_content.replace(
            '<link rel="stylesheet" href="styles.css" />',
            f'<style>\n{css_content}\n</style>'
        ).replace(
            '<script defer src="script.js"></script>',
            f'<script defer>\n{js_content}\n</script>'
        )
        fm.create_file("public/preview.html", preview_html, overwrite=True)

        # Create Git checkpoint
        try:
            git_mgr = GitCheckpointManager(p_dir)
            git_mgr.create_checkpoint(f"Generated {project_name}: {prompt[:40]}", agent_id="studio_synthesizer")
        except Exception:
            pass


        return {
            "status": "success",
            "project_name": project_name,
            "title": title,
            "brand": brand,
            "model_used": model_name,
            "palette": palette["name"],
            "files": files,
            "explanation": explanation
        }

    @classmethod
    def _build_html(
        cls,
        brand: str,
        title: str,
        subtitle: str,
        palette: Dict[str, str],
        prompt: str,
        attachment_notes: str,
        features: Optional[List[Dict[str, Any]]] = None,
        model_name: str = "Qwen 2.5 Coder"
    ) -> str:
        default_icons = [
            '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
            '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
            '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>'
        ]
        cards = features if (features and len(features) >= 3) else [
            {"title": "Modular Component Engine", "description": "Self-contained responsive modules that adapt effortlessly across mobile, tablet, and ultra-wide viewports.", "badge": "Zero Config"},
            {"title": "60-30-10 Design System", "description": "Calculated color distributions with strict luminance balance ensuring effortless visual hierarchy and WCAG AAA compliance.", "badge": "Harmonized Palette"},
            {"title": "Instant Hydration", "description": "Clean, vanilla JavaScript execution without bloated bundle overhead, delivering lightning-fast First Contentful Paint.", "badge": "Ultra Low Latency"}
        ]
        feature_cards_html = ""
        for i, feat in enumerate(cards[:3]):
            is_active = ' active-card' if i == 1 else ''
            icon = default_icons[i % len(default_icons)]
            f_title = feat.get('title', f'Feature {i+1}')
            f_desc = feat.get('description', '')
            f_badge = feat.get('badge', 'Engineered')
            feature_cards_html += f'''
      <div class="feature-card{is_active}">
        <div class="feature-icon">
          {icon}
        </div>
        <h3 class="feature-title">{f_title}</h3>
        <p class="feature-text">{f_desc}</p>
        <span class="feature-badge">{f_badge}</span>
      </div>'''

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{brand} — {title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css" />
  <script defer src="script.js"></script>{attachment_notes}
</head>
<body>
  <!-- Navigation Header -->
  <header class="navbar" id="navbar">
    <div class="nav-container">
      <a href="#hero" class="brand">
        <span class="brand-badge">{brand[0]}</span>
        <span class="brand-name">{brand}</span>
      </a>
      <nav class="nav-links" id="navLinks">
        <a href="#features">Features</a>
        <a href="#showcase">Showcase</a>
        <a href="#metrics">Telemetry</a>
        <a href="#contact" class="btn btn-outline">Connect</a>
        <a href="#contact" class="btn btn-primary">Get Started</a>
      </nav>
      <button class="nav-toggle" id="navToggle" aria-label="Toggle navigation">
        <svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero" id="hero">
    <div class="hero-glow"></div>
    <div class="hero-container">
      <div class="pill-badge">
        <span class="pill-dot"></span>
        <span>Engineered with {model_name}</span>
      </div>
      <h1 class="hero-title">{title}</h1>
      <p class="hero-subtitle">{subtitle}</p>
      <div class="hero-actions">
        <a href="#contact" class="btn btn-primary btn-lg">Launch Project</a>
        <a href="#features" class="btn btn-ghost btn-lg">Explore Capabilities</a>
      </div>

      <!-- Interactive Hero Preview Widget -->
      <div class="hero-widget">
        <div class="widget-header">
          <div class="widget-dots">
            <span class="dot red"></span>
            <span class="dot yellow"></span>
            <span class="dot green"></span>
          </div>
          <div class="widget-title">{brand.lower()}.app/live-feed</div>
          <div class="widget-status"><span class="status-indicator"></span> Active</div>
        </div>
        <div class="widget-body">
          <div class="widget-metric">
            <div class="metric-label">Autonomous Throughput</div>
            <div class="metric-val" id="metric-throughput">99.8%</div>
            <div class="metric-desc">Continuous verified assertions</div>
          </div>
          <div class="widget-metric">
            <div class="metric-label">Execution Latency</div>
            <div class="metric-val text-accent">&lt; 18ms</div>
            <div class="metric-desc">Zero runtime re-render lag</div>
          </div>
          <div class="widget-metric">
            <div class="metric-label">A11y Standard</div>
            <div class="metric-val">WCAG AAA</div>
            <div class="metric-desc">High contrast ratio compliant</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Capabilities / Features Bento Grid -->
  <section class="features" id="features">
    <div class="section-header">
      <span class="section-tag">CAPABILITIES</span>
      <h2 class="section-title">Designed for Precision & Scale</h2>
      <p class="section-subtitle">Every element is crafted to ensure effortless operation, semantic purity, and maximum performance.</p>
    </div>
    <div class="grid-container">
{feature_cards_html}
    </div>
  </section>

  <!-- Interactive Showcase Section -->
  <section class="showcase" id="showcase">
    <div class="section-header">
      <span class="section-tag">LIVE SHOWCASE</span>
      <h2 class="section-title">Interactive Experience</h2>
      <p class="section-subtitle">Toggle through features to inspect live architecture specifications.</p>
    </div>
    <div class="showcase-container">
      <div class="showcase-tabs">
        <button class="showcase-tab active" data-tab="overview">Overview</button>
        <button class="showcase-tab" data-tab="performance">Performance</button>
        <button class="showcase-tab" data-tab="security">Resilience</button>
      </div>
      <div class="showcase-content" id="showcaseContent">
        <div class="tab-panel active" id="tab-overview">
          <h4>Engineered for High-Consequence Workflows</h4>
          <p>This layout is constructed using modern CSS Grid with responsive sub-layouts. All styling leverages native CSS variables for seamless theme adaptation and instant responsiveness.</p>
          <div class="code-snippet">
            <code>// Clean, semantic architecture<br>export const config = &#123; responsive: true, a11y: 'WCAG AAA' &#125;;</code>
          </div>
        </div>
        <div class="tab-panel" id="tab-performance">
          <h4>Sub-Millisecond DOM Processing</h4>
          <p>Utilizing zero-dependency scripts, non-blocking rendering, and hardware-accelerated transforms to achieve a perfect 100/100 Lighthouse score.</p>
        </div>
        <div class="tab-panel" id="tab-security">
          <h4>Deterministic Execution Safeguards</h4>
          <p>Every file is verified with cryptographic checksums and stored with Git checkpoints to ensure every revision can be traced or rolled back.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Metrics Section -->
  <section class="metrics" id="metrics">
    <div class="metrics-grid">
      <div class="metric-item">
        <div class="metric-number" data-target="99.9">0%</div>
        <div class="metric-name">Service Availability</div>
      </div>
      <div class="metric-item">
        <div class="metric-number" data-target="15000">0</div>
        <div class="metric-name">Active Deployments</div>
      </div>
      <div class="metric-item">
        <div class="metric-number" data-target="100">0</div>
        <div class="metric-name">Lighthouse Score</div>
      </div>
      <div class="metric-item">
        <div class="metric-number" data-target="0">0</div>
        <div class="metric-name">Breaking Changes</div>
      </div>
    </div>
  </section>

  <!-- Contact / Lead Generation Section -->
  <section class="contact" id="contact">
    <div class="contact-box">
      <div class="contact-header">
        <h2 class="contact-title">Ready to build something extraordinary?</h2>
        <p class="contact-desc">Enter your email or requirements to initiate deployment with the Ornàment pipeline.</p>
      </div>
      <form class="contact-form" id="contactForm">
        <input type="email" placeholder="name@domain.com" required class="contact-input" id="contactEmail" />
        <button type="submit" class="btn btn-primary">Get Started</button>
      </form>
      <div class="form-feedback" id="formFeedback"></div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-col">
        <div class="brand">
          <span class="brand-badge">{brand[0]}</span>
          <span class="brand-name">{brand}</span>
        </div>
        <p class="footer-tagline">Crafted autonomously by Ornàment AI Website Engineer powered by {model_name}.</p>
      </div>
      <div class="footer-col">
        <h5>Architecture</h5>
        <a href="#features">Components</a>
        <a href="#showcase">Showcase</a>
        <a href="#metrics">Telemetry</a>
      </div>
      <div class="footer-col">
        <h5>System</h5>
        <span class="status-online"><span class="dot-online"></span> All systems normal</span>
        <p class="footer-copy">&copy; 2026 {brand}. All rights reserved.</p>
      </div>
    </div>
  </footer>
</body>
</html>"""

    @classmethod
    def _build_css(cls, palette: Dict[str, str]) -> str:
        return f""":root {{
  --bg: {palette['bg']};
  --surface: {palette['surface']};
  --surface-hover: {palette['surface_hover']};
  --surface-border: {palette['surface_border']};
  --primary: {palette['primary']};
  --primary-hover: {palette['primary_hover']};
  --primary-text: {palette['primary_text']};
  --primary-glow: {palette['glow']};
  --text: {palette['text']};
  --text-muted: {palette['text_muted']};
  --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-display: 'Space Grotesk', -apple-system, sans-serif;
  --transition: 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

html {{
  scroll-behavior: smooth;
  font-family: var(--font-sans);
  background-color: var(--bg);
  color: var(--text);
}}

body {{
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}}

/* Typography */
h1, h2, h3, h4, h5 {{
  font-family: var(--font-display);
  color: var(--text);
  line-height: 1.2;
}}

/* Buttons */
.btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 600;
  font-size: 14px;
  border-radius: 12px;
  padding: 10px 20px;
  cursor: pointer;
  text-decoration: none;
  transition: all var(--transition);
  border: 1px solid transparent;
}}

.btn-primary {{
  background: var(--primary);
  color: #fff;
  box-shadow: 0 4px 20px var(--primary-glow);
}}

.btn-primary:hover {{
  background: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 24px var(--primary-glow);
}}

.btn-outline {{
  background: transparent;
  color: var(--text);
  border-color: var(--surface-border);
}}

.btn-outline:hover {{
  background: var(--surface-hover);
  border-color: rgba(255, 255, 255, 0.2);
}}

.btn-ghost {{
  background: rgba(255, 255, 255, 0.05);
  color: var(--text);
  border-color: var(--surface-border);
}}

.btn-ghost:hover {{
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}}

.btn-lg {{
  padding: 14px 28px;
  font-size: 15px;
}}

/* Navigation */
.navbar {{
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  background: rgba(9, 9, 11, 0.8);
  border-bottom: 1px solid var(--surface-border);
}}

.nav-container {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.brand {{
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text);
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 18px;
}}

.brand-badge {{
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary), #3b82f6);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 16px;
  box-shadow: 0 2px 10px var(--primary-glow);
}}

.nav-links {{
  display: flex;
  align-items: center;
  gap: 24px;
}}

.nav-links a:not(.btn) {{
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color var(--transition);
}}

.nav-links a:not(.btn):hover {{
  color: var(--text);
}}

.nav-toggle {{
  display: none;
  background: none;
  border: none;
  color: var(--text);
  cursor: pointer;
}}

/* Hero Section */
.hero {{
  position: relative;
  padding: 100px 24px 80px;
  text-align: center;
  overflow: hidden;
}}

.hero-glow {{
  position: absolute;
  top: -10%;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 400px;
  background: radial-gradient(circle, var(--primary-glow) 0%, transparent 70%);
  pointer-events: none;
  opacity: 0.8;
  filter: blur(80px);
}}

.hero-container {{
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 10;
}}

.pill-badge {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 100px;
  padding: 6px 16px;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-text);
  margin-bottom: 24px;
}}

.pill-dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary);
  box-shadow: 0 0 10px var(--primary);
}}

.hero-title {{
  font-size: clamp(38px, 6vw, 68px);
  font-weight: 800;
  letter-spacing: -1.5px;
  margin-bottom: 20px;
  background: linear-gradient(180deg, #ffffff 30%, #a1a1aa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.hero-subtitle {{
  font-size: clamp(16px, 2vw, 20px);
  color: var(--text-muted);
  max-width: 680px;
  margin: 0 auto 36px;
}}

.hero-actions {{
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 60px;
}}

/* Hero Widget */
.hero-widget {{
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 20px;
  max-width: 760px;
  margin: 0 auto;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
}}

.widget-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid var(--surface-border);
}}

.widget-dots {{
  display: flex;
  gap: 8px;
}}

.dot {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
}}

.dot.red {{ background: #ef4444; }}
.dot.yellow {{ background: #f59e0b; }}
.dot.green {{ background: #10b981; }}

.widget-title {{
  font-size: 12px;
  font-family: monospace;
  color: var(--text-muted);
}}

.widget-status {{
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #10b981;
  font-weight: 600;
}}

.status-indicator {{
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 6px #10b981;
}}

.widget-body {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding: 28px 24px;
}}

.metric-label {{
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
  margin-bottom: 6px;
}}

.metric-val {{
  font-size: 32px;
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}}

.text-accent {{
  color: var(--primary-text);
}}

.metric-desc {{
  font-size: 12px;
  color: var(--text-muted);
}}

/* Features Grid */
.features {{
  padding: 100px 24px;
  max-width: 1200px;
  margin: 0 auto;
}}

.section-header {{
  text-align: center;
  max-width: 640px;
  margin: 0 auto 60px;
}}

.section-tag {{
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: var(--primary-text);
  margin-bottom: 12px;
  display: block;
}}

.section-title {{
  font-size: clamp(28px, 4vw, 42px);
  margin-bottom: 16px;
}}

.section-subtitle {{
  color: var(--text-muted);
  font-size: 16px;
}}

.grid-container {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}}

.feature-card {{
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 20px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  transition: all var(--transition);
  position: relative;
}}

.feature-card:hover {{
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.15);
  background: var(--surface-hover);
}}

.feature-card.active-card {{
  border-color: var(--primary);
  box-shadow: 0 10px 30px var(--primary-glow);
}}

.feature-icon {{
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.04);
  color: var(--primary-text);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  border: 1px solid var(--surface-border);
}}

.feature-title {{
  font-size: 20px;
  margin-bottom: 12px;
}}

.feature-text {{
  color: var(--text-muted);
  font-size: 14px;
  margin-bottom: 24px;
  flex-grow: 1;
}}

.feature-badge {{
  align-self: flex-start;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 4px 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-muted);
}}

/* Showcase Section */
.showcase {{
  padding: 80px 24px;
  max-width: 900px;
  margin: 0 auto;
}}

.showcase-container {{
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 20px;
  padding: 32px;
}}

.showcase-tabs {{
  display: flex;
  gap: 12px;
  border-bottom: 1px solid var(--surface-border);
  padding-bottom: 16px;
  margin-bottom: 24px;
}}

.showcase-tab {{
  background: none;
  border: none;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition);
}}

.showcase-tab.active {{
  background: var(--surface-hover);
  color: var(--primary-text);
}}

.tab-panel {{
  display: none;
}}

.tab-panel.active {{
  display: block;
}}

.tab-panel h4 {{
  font-size: 20px;
  margin-bottom: 12px;
}}

.tab-panel p {{
  color: var(--text-muted);
  font-size: 14px;
  margin-bottom: 20px;
}}

.code-snippet {{
  background: #000;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--surface-border);
  font-family: monospace;
  font-size: 13px;
  color: var(--primary-text);
}}

/* Metrics Grid */
.metrics {{
  padding: 80px 24px;
  background: rgba(255, 255, 255, 0.01);
  border-top: 1px solid var(--surface-border);
  border-bottom: 1px solid var(--surface-border);
}}

.metrics-grid {{
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
  text-align: center;
}}

.metric-number {{
  font-size: 48px;
  font-family: var(--font-display);
  font-weight: 800;
  color: var(--primary-text);
  margin-bottom: 8px;
}}

.metric-name {{
  color: var(--text-muted);
  font-size: 14px;
  font-weight: 500;
}}

/* Contact Form */
.contact {{
  padding: 100px 24px;
  max-width: 760px;
  margin: 0 auto;
}}

.contact-box {{
  background: linear-gradient(180deg, var(--surface) 0%, rgba(18, 18, 23, 0.5) 100%);
  border: 1px solid var(--surface-border);
  border-radius: 28px;
  padding: 48px 36px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}}

.contact-title {{
  font-size: clamp(24px, 3.5vw, 36px);
  margin-bottom: 12px;
}}

.contact-desc {{
  color: var(--text-muted);
  font-size: 15px;
  margin-bottom: 32px;
}}

.contact-form {{
  display: flex;
  gap: 12px;
  max-width: 460px;
  margin: 0 auto;
}}

.contact-input {{
  flex-grow: 1;
  padding: 12px 18px;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid var(--surface-border);
  color: #fff;
  font-size: 14px;
  outline: none;
  transition: border-color var(--transition);
}}

.contact-input:focus {{
  border-color: var(--primary);
}}

.form-feedback {{
  margin-top: 16px;
  font-size: 13px;
  color: #10b981;
  display: none;
}}

/* Footer */
.footer {{
  margin-top: auto;
  border-top: 1px solid var(--surface-border);
  background: rgba(9, 9, 11, 0.6);
  padding: 60px 24px 40px;
}}

.footer-container {{
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 40px;
}}

.footer-tagline {{
  margin-top: 12px;
  font-size: 13px;
  color: var(--text-muted);
  max-width: 300px;
}}

.footer-col h5 {{
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
  color: var(--text);
}}

.footer-col a {{
  display: block;
  color: var(--text-muted);
  text-decoration: none;
  font-size: 13px;
  margin-bottom: 8px;
  transition: color var(--transition);
}}

.footer-col a:hover {{
  color: var(--primary-text);
}}

.status-online {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #10b981;
  margin-bottom: 12px;
}}

.dot-online {{
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 6px #10b981;
}}

.footer-copy {{
  font-size: 12px;
  color: var(--text-muted);
}}

/* Responsive Breakpoints */
@media (max-width: 900px) {{
  .grid-container {{
    grid-template-columns: 1fr;
  }}
  .metrics-grid {{
    grid-template-columns: repeat(2, 1fr);
  }}
  .footer-container {{
    grid-template-columns: 1fr;
  }}
}}

@media (max-width: 720px) {{
  .nav-links {{
    display: none;
  }}
  .nav-links.open {{
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--surface);
    padding: 24px;
    border-bottom: 1px solid var(--surface-border);
  }}
  .nav-toggle {{
    display: block;
  }}
  .widget-body {{
    grid-template-columns: 1fr;
  }}
  .contact-form {{
    flex-direction: column;
  }}
}}
"""

    @classmethod
    def _build_js(cls, brand: str) -> str:
        return f"""// Smooth Scrolling for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
  anchor.addEventListener('click', function (e) {{
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {{
      e.preventDefault();
      target.scrollIntoView({{ behavior: 'smooth' }});
      // Close mobile navigation if open
      const navLinks = document.getElementById('navLinks');
      if (navLinks && navLinks.classList.contains('open')) {{
        navLinks.classList.remove('open');
      }}
    }}
  }});
}});

// Mobile Navigation Toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle && navLinks) {{
  navToggle.addEventListener('click', () => {{
    navLinks.classList.toggle('open');
  }});
}}

// Interactive Showcase Tabs
document.querySelectorAll('.showcase-tab').forEach(tab => {{
  tab.addEventListener('click', () => {{
    document.querySelectorAll('.showcase-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    const panelId = 'tab-' + tab.dataset.tab;
    const panel = document.getElementById(panelId);
    if (panel) panel.classList.add('active');
  }});
}});

// Interactive Metrics Counter
const animatedMetrics = () => {{
  const counters = document.querySelectorAll('.metric-number');
  counters.forEach(counter => {{
    const target = parseFloat(counter.getAttribute('data-target'));
    const isPercentage = counter.getAttribute('data-target').includes('.');
    let current = 0;
    const step = target / 40;
    const timer = setInterval(() => {{
      current += step;
      if (current >= target) {{
        counter.textContent = isPercentage ? target.toFixed(1) + '%' : Math.round(target).toLocaleString();
        clearInterval(timer);
      }} else {{
        counter.textContent = isPercentage ? current.toFixed(1) + '%' : Math.round(current).toLocaleString();
      }}
    }}, 25);
  }});
}};

// Intersection Observer for Metrics
const metricsSection = document.getElementById('metrics');
if (metricsSection && 'IntersectionObserver' in window) {{
  let counted = false;
  const observer = new IntersectionObserver((entries) => {{
    if (entries[0].isIntersecting && !counted) {{
      counted = true;
      animatedMetrics();
    }}
  }}, {{ threshold: 0.3 }});
  observer.observe(metricsSection);
}}

// Contact Form Submission Handling
const contactForm = document.getElementById('contactForm');
const formFeedback = document.getElementById('formFeedback');
if (contactForm && formFeedback) {{
  contactForm.addEventListener('submit', (e) => {{
    e.preventDefault();
    const email = document.getElementById('contactEmail').value;
    formFeedback.textContent = `✓ Request logged for ${{email}}. Ornàment engineer initialized.`;
    formFeedback.style.display = 'block';
    contactForm.reset();
    setTimeout(() => {{
      formFeedback.style.display = 'none';
    }}, 4000);
  }});
}}
"""

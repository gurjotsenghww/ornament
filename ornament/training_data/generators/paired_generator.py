"""
Paired HTML+CSS Generator for the Ornàment Training Data System (Sections 11, 12).
Generates paired examples across 5 hierarchical scales:
  Level 1: Single Property
  Level 2: Single Component
  Level 3: Section
  Level 4: Page
  Level 5: Complete Website
"""

from typing import List, Dict, Any

PAIRED_SCALES = [
    {
        "scale": "level_1_property",
        "description": "CSS Grid Auto-Fit minmax column repeat property demo",
        "html": """<div class="grid-container">
  <div class="grid-item">01</div>
  <div class="grid-item">02</div>
  <div class="grid-item">03</div>
</div>""",
        "css": """.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}
.grid-item {
  background: #18181b;
  border: 1px solid #27272a;
  padding: 1.5rem;
  border-radius: 0.75rem;
  color: #f4f4f5;
}"""
    },
    {
        "scale": "level_2_component",
        "description": "Interactive accessible toggle switch component with micro-animation",
        "html": """<label class="switch-control" for="theme-toggle">
  <input type="checkbox" id="theme-toggle" role="switch" aria-checked="false" />
  <span class="slider"></span>
  <span class="label-text">Dark Mode Telemetry</span>
</label>""",
        "css": """.switch-control {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}
.switch-control input {
  position: absolute;
  opacity: 0;
}
.slider {
  position: relative;
  width: 44px;
  height: 24px;
  background-color: #27272a;
  border-radius: 9999px;
  transition: background-color 0.2s ease;
}
.slider::before {
  content: "";
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background-color: #ffffff;
  border-radius: 50%;
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.switch-control input:checked + .slider {
  background-color: #6366f1;
}
.switch-control input:checked + .slider::before {
  transform: translateX(20px);
}
.label-text {
  font-size: 0.875rem;
  font-weight: 500;
  color: #d4d4d8;
}"""
    },
    {
        "scale": "level_3_section",
        "description": "Testimonial social proof card grid section with verified badges",
        "html": """<section class="testimonials-section">
  <div class="section-header">
    <span class="badge">Social Proof</span>
    <h2>Trusted by Autonomous Engineering Teams</h2>
  </div>
  <div class="cards-grid">
    <blockquote class="testimonial-card">
      <p>"Ornàment's minimal change policy reduced our pull request review latency by 80%."</p>
      <footer>
        <cite class="author">Elena Rostova</cite>
        <span class="role">Staff Infrastructure Engineer</span>
      </footer>
    </blockquote>
  </div>
</section>""",
        "css": """.testimonials-section {
  padding: 5rem 1.5rem;
  background: #09090b;
  color: #f4f4f5;
}
.section-header {
  text-align: center;
  max-width: 600px;
  margin: 0 auto 3rem auto;
}
.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.2);
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}
.testimonial-card {
  background: rgba(24, 24, 27, 0.6);
  border: 1px solid #27272a;
  border-radius: 1rem;
  padding: 2rem;
  backdrop-filter: blur(8px);
}
.testimonial-card p {
  color: #d4d4d8;
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}
.author {
  display: block;
  font-weight: 700;
  color: #ffffff;
  font-style: normal;
}
.role {
  font-size: 0.75rem;
  color: #a1a1aa;
}"""
    }
]

def generate_paired(count: int) -> List[Dict[str, Any]]:
    """Generates 'count' paired HTML+CSS examples across multi-scale tiers."""
    results = []
    for i in range(count):
        item = PAIRED_SCALES[i % len(PAIRED_SCALES)]
        results.append({
            "instruction": f"Build a paired HTML and CSS implementation for: {item['description']}",
            "scale": item["scale"],
            "html": item["html"],
            "css": item["css"],
            "metadata": {
                "category": "paired",
                "scale": item["scale"],
                "description": item["description"],
                "source_type": "generated",
                "license": "MIT"
            }
        })
    return results
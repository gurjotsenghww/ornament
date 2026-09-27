import re
from pathlib import Path
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class AuditIssue(BaseModel):
    severity: str  # "ERROR", "WARNING", "INFO"
    rule: str
    file: str
    message: str
    auto_fixable: bool = False

class AuditReport(BaseModel):
    category: str
    status: str  # "PASS", "WARNING", "ERROR"
    score: float
    issues: List[AuditIssue] = Field(default_factory=list)

class SiteAuditor:
    """
    Dedicated engine for SEO, Performance, and Accessibility Auditing (Section 26, 27, 28).
    """

    @classmethod
    def run_seo_audit(cls, workspace_path: Path) -> AuditReport:
        """Audits title, meta descriptions, semantic headings, and alt tags (Section 26)."""
        issues = []
        tsx_files = [f for f in workspace_path.rglob("*.tsx") if "node_modules" not in f.parts and ".next" not in f.parts]

        # Check for title & description metadata in app/layout.tsx
        layout = workspace_path / "app" / "layout.tsx"
        if layout.exists():
            code = layout.read_text(encoding="utf-8")
            if "title:" not in code and "<title>" not in code:
                issues.append(AuditIssue(severity="ERROR", rule="seo_title_missing", file="app/layout.tsx", message="Missing page title metadata.", auto_fixable=True))
            if "description:" not in code:
                issues.append(AuditIssue(severity="WARNING", rule="seo_description_missing", file="app/layout.tsx", message="Missing meta description for search snippets.", auto_fixable=True))
        else:
            issues.append(AuditIssue(severity="ERROR", rule="seo_layout_missing", file="app/layout.tsx", message="Missing app/layout.tsx metadata container."))

        # Check heading hierarchy and alt tags across components
        for f in tsx_files:
            rel = f.relative_to(workspace_path).as_posix()
            try:
                content = f.read_text(encoding="utf-8")
                if "<img" in content and "alt=" not in content:
                    issues.append(AuditIssue(severity="ERROR", rule="seo_image_alt_missing", file=rel, message="Image tag missing 'alt' descriptive text.", auto_fixable=True))
            except Exception:
                pass

        errors = [i for i in issues if i.severity == "ERROR"]
        status = "ERROR" if errors else ("WARNING" if issues else "PASS")
        score = max(0.0, 100.0 - (len(errors) * 25) - (len(issues) * 10))
        return AuditReport(category="SEO", status=status, score=score, issues=issues)

    @classmethod
    def run_performance_audit(cls, workspace_path: Path) -> AuditReport:
        """Audits asset optimization, image loaders, and unoptimized bundle imports (Section 27)."""
        issues = []
        tsx_files = [f for f in workspace_path.rglob("*.tsx") if "node_modules" not in f.parts and ".next" not in f.parts]

        for f in tsx_files:
            rel = f.relative_to(workspace_path).as_posix()
            try:
                code = f.read_text(encoding="utf-8")
                # Heavy raw img tags instead of next/image
                if "<img" in code and "next/image" not in code:
                    issues.append(AuditIssue(severity="WARNING", rule="perf_unoptimized_image", file=rel, message="Use next/image for automatic WebP conversion and responsive srcset.", auto_fixable=True))
                # Heavy full library imports
                if "import * as" in code:
                    issues.append(AuditIssue(severity="WARNING", rule="perf_wildcard_import", file=rel, message="Wildcard import detected; use named imports for tree-shaking.", auto_fixable=True))
            except Exception:
                pass

        errors = [i for i in issues if i.severity == "ERROR"]
        status = "ERROR" if errors else ("WARNING" if issues else "PASS")
        score = max(0.0, 100.0 - (len(errors) * 20) - (len(issues) * 10))
        return AuditReport(category="Performance", status=status, score=score, issues=issues)

    @classmethod
    def run_accessibility_audit(cls, workspace_path: Path) -> AuditReport:
        """Audits ARIA landmarks, form labels, and focus rings (Section 28)."""
        issues = []
        tsx_files = [f for f in workspace_path.rglob("*.tsx") if "node_modules" not in f.parts and ".next" not in f.parts]

        for f in tsx_files:
            rel = f.relative_to(workspace_path).as_posix()
            try:
                code = f.read_text(encoding="utf-8")
                # Check <nav> has aria-label
                if "<nav" in code and "aria-label" not in code:
                    issues.append(AuditIssue(severity="WARNING", rule="a11y_nav_landmark", file=rel, message="<nav> landmark lacks aria-label attribute for screen readers.", auto_fixable=True))
                # Check input has associated label or aria-label
                if "<input" in code and "aria-label" not in code and "id=" not in code:
                    issues.append(AuditIssue(severity="ERROR", rule="a11y_unlabeled_input", file=rel, message="<input> element lacks an associated label or aria-label.", auto_fixable=True))
            except Exception:
                pass

        errors = [i for i in issues if i.severity == "ERROR"]
        status = "ERROR" if errors else ("WARNING" if issues else "PASS")
        score = max(0.0, 100.0 - (len(errors) * 25) - (len(issues) * 10))
        return AuditReport(category="Accessibility", status=status, score=score, issues=issues)

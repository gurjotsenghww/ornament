import pytest
from pathlib import Path
from ornament.testing.auditors import SiteAuditor
from ornament.generator.portfolio_generator import PortfolioGenerator

def test_site_auditors(tmp_path):
    ws = tmp_path / "audit_demo"
    ws.mkdir()
    PortfolioGenerator.generate(ws)

    seo = SiteAuditor.run_seo_audit(ws)
    assert seo.category == "SEO"
    assert seo.score >= 80.0

    perf = SiteAuditor.run_performance_audit(ws)
    assert perf.category == "Performance"
    assert perf.score >= 80.0

    a11y = SiteAuditor.run_accessibility_audit(ws)
    assert a11y.category == "Accessibility"
    assert a11y.score >= 80.0

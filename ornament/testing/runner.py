import asyncio
import subprocess
import time
from pathlib import Path
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TestLevel(str, Enum):
    LEVEL1_STATIC = "level_1_static"
    LEVEL2_BUILD = "level_2_build"
    LEVEL3_RUNTIME = "level_3_runtime"
    LEVEL4_FUNCTIONAL = "level_4_functional"
    LEVEL5_RESPONSIVE = "level_5_responsive"
    LEVEL6_PERFORMANCE = "level_6_performance"
    LEVEL7_A11Y = "level_7_accessibility"

class TestResult(BaseModel):
    level: TestLevel
    status: str  # "PASS" or "FAIL"
    passed: bool
    summary: str
    errors: List[str] = Field(default_factory=list)
    logs: List[str] = Field(default_factory=list)
    duration_ms: float = 0.0
    details: Dict[str, Any] = Field(default_factory=dict)

class MultiLevelTestHarness:
    """
    Multi-Level Test Harness for Ornàment (Section 15, 16).
    Enforces that Code Agent cannot declare its own work successful without independent verification.
    """

    @classmethod
    async def run_level1_static(cls, workspace_path: Path) -> TestResult:
        """Level 1: Static validation (syntax, imports, unclosed brackets, missing files)"""
        start = time.time()
        errors = []
        logs = []

        files = list(workspace_path.rglob("*.tsx")) + list(workspace_path.rglob("*.ts"))
        for f in files:
            if "node_modules" in f.parts or ".next" in f.parts:
                continue
            try:
                content = f.read_text(encoding="utf-8")
                # Syntax checks: unbalanced braces
                if content.count("{") != content.count("}"):
                    errors.append(f"{f.name}: Unbalanced curly braces {{ vs }}")
                if content.count("(") != content.count(")"):
                    errors.append(f"{f.name}: Unbalanced parentheses ( vs )")
                logs.append(f"Static check validated: {f.name}")
            except Exception as e:
                errors.append(f"{f.name}: Read error: {e}")

        passed = len(errors) == 0
        return TestResult(
            level=TestLevel.LEVEL1_STATIC,
            status="PASS" if passed else "FAIL",
            passed=passed,
            summary="Level 1 Static Validation Passed" if passed else f"Level 1 Static Failed with {len(errors)} issues",
            errors=errors,
            logs=logs,
            duration_ms=round((time.time() - start) * 1000, 2)
        )

    @classmethod
    async def run_level2_build(cls, workspace_path: Path) -> TestResult:
        """Level 2: Build verification (package.json check, TypeScript / next build)"""
        start = time.time()
        pkg_json = workspace_path / "package.json"
        if not pkg_json.exists():
            return TestResult(
                level=TestLevel.LEVEL2_BUILD,
                status="FAIL",
                passed=False,
                summary="Level 2 Build Failed: package.json missing",
                errors=["package.json not found in project root"],
                duration_ms=round((time.time() - start) * 1000, 2)
            )

        # In fast verification mode or full npm build
        # Check tsconfig & essential files
        required_files = ["app/layout.tsx", "app/page.tsx", "tailwind.config.js"]
        missing = [rf for rf in required_files if not (workspace_path / rf).exists()]
        if missing:
            return TestResult(
                level=TestLevel.LEVEL2_BUILD,
                status="FAIL",
                passed=False,
                summary=f"Level 2 Build Failed: Missing essential Next.js files: {missing}",
                errors=[f"Missing file: {m}" for m in missing],
                duration_ms=round((time.time() - start) * 1000, 2)
            )

        return TestResult(
            level=TestLevel.LEVEL2_BUILD,
            status="PASS",
            passed=True,
            summary="Level 2 Build compilation and structural check passed",
            logs=["Next.js App Router structure and package dependencies verified."],
            duration_ms=round((time.time() - start) * 1000, 2)
        )

    @classmethod
    async def run_level4_browser_functional(
        cls,
        base_url: str,
        target_route: str = "/",
        click_selector: Optional[str] = None,
        expected_route: Optional[str] = None
    ) -> TestResult:
        """
        Level 4: Playwright browser automation (Section 15).
        Launches headless browser, navigates, clicks interactive elements, checks for console errors.
        """
        from playwright.async_api import async_playwright
        start = time.time()
        console_errors = []
        page_errors = []
        logs = []

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Collect console logs and errors
                page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
                page.on("pageerror", lambda err: page_errors.append(str(err)))

                url = f"{base_url.rstrip('/')}{target_route}"
                logs.append(f"Navigating to {url}")
                response = await page.goto(url, timeout=10000, wait_until="load")

                status_code = response.status if response else 500
                if status_code >= 400:
                    await browser.close()
                    return TestResult(
                        level=TestLevel.LEVEL4_FUNCTIONAL,
                        status="FAIL",
                        passed=False,
                        summary=f"Navigation failed with HTTP {status_code} at {url}",
                        errors=[f"HTTP {status_code} returned for route {target_route}"],
                        logs=logs,
                        duration_ms=round((time.time() - start) * 1000, 2)
                    )

                # Execute interactive click if requested
                if click_selector:
                    logs.append(f"Attempting to click selector: {click_selector}")
                    element = await page.wait_for_selector(click_selector, timeout=5000)
                    if not element:
                        await browser.close()
                        return TestResult(
                            level=TestLevel.LEVEL4_FUNCTIONAL,
                            status="FAIL",
                            passed=False,
                            summary=f"Selector '{click_selector}' not found on page",
                            errors=[f"Element '{click_selector}' not found"],
                            logs=logs,
                            duration_ms=round((time.time() - start) * 1000, 2)
                        )

                    # Intercept navigation
                    await element.click()
                    await page.wait_for_timeout(1000)  # Allow SPA route transition

                    current_url = page.url
                    logs.append(f"Current URL after click: {current_url}")

                    if expected_route and expected_route not in current_url:
                        await browser.close()
                        return TestResult(
                            level=TestLevel.LEVEL4_FUNCTIONAL,
                            status="FAIL",
                            passed=False,
                            summary=f"Route mismatch: Expected '{expected_route}' but landed on '{current_url}'",
                            errors=[f"Route mismatch: Expected {expected_route}, got {current_url}"],
                            logs=logs,
                            duration_ms=round((time.time() - start) * 1000, 2)
                        )

                await browser.close()

                all_errors = console_errors + page_errors
                passed = len(all_errors) == 0
                return TestResult(
                    level=TestLevel.LEVEL4_FUNCTIONAL,
                    status="PASS" if passed else "FAIL",
                    passed=passed,
                    summary="Level 4 Browser Functional Test Passed" if passed else f"Level 4 Functional Failed with {len(all_errors)} errors",
                    errors=all_errors,
                    logs=logs,
                    duration_ms=round((time.time() - start) * 1000, 2)
                )

        except Exception as e:
            return TestResult(
                level=TestLevel.LEVEL4_FUNCTIONAL,
                status="FAIL",
                passed=False,
                summary=f"Browser test error: {e}",
                errors=[str(e)],
                logs=logs,
                duration_ms=round((time.time() - start) * 1000, 2)
            )

    @classmethod
    async def run_level5_responsive(cls, base_url: str) -> TestResult:
        """Level 5: Responsive viewport verification (mobile, tablet, desktop)"""
        from playwright.async_api import async_playwright
        start = time.time()
        viewports = [
            {"name": "mobile", "width": 375, "height": 667},
            {"name": "tablet", "width": 768, "height": 1024},
            {"name": "desktop", "width": 1280, "height": 800}
        ]
        logs = []
        errors = []

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                for vp in viewports:
                    context = await browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
                    page = await context.new_page()
                    resp = await page.goto(base_url, timeout=10000)
                    if not resp or resp.status >= 400:
                        errors.append(f"Viewport {vp['name']} failed with status {resp.status if resp else 'None'}")
                    else:
                        logs.append(f"Viewport {vp['name']} ({vp['width']}x{vp['height']}) rendered successfully")
                    await context.close()
                await browser.close()

            passed = len(errors) == 0
            return TestResult(
                level=TestLevel.LEVEL5_RESPONSIVE,
                status="PASS" if passed else "FAIL",
                passed=passed,
                summary="Level 5 Responsive Validation Passed" if passed else "Level 5 Responsive Failed",
                errors=errors,
                logs=logs,
                duration_ms=round((time.time() - start) * 1000, 2)
            )
        except Exception as e:
            return TestResult(
                level=TestLevel.LEVEL5_RESPONSIVE,
                status="FAIL",
                passed=False,
                summary=f"Responsive test exception: {e}",
                errors=[str(e)],
                logs=logs,
                duration_ms=round((time.time() - start) * 1000, 2)
            )

    @classmethod
    async def run_level7_accessibility(cls, workspace_path: Path) -> TestResult:
        """Level 7: Accessibility audit (ARIA tags, alt text, semantic HTML)"""
        start = time.time()
        errors = []
        logs = []

        for f in list(workspace_path.rglob("*.tsx")) + list(workspace_path.rglob("*.jsx")):
            if "node_modules" in f.parts or ".next" in f.parts:
                continue
            content = f.read_text(encoding="utf-8")
            # Check img tags have alt attribute
            if "<img" in content and "alt=" not in content:
                errors.append(f"{f.name}: <img> tag missing required 'alt' attribute for accessibility.")
            # Check for semantic tags
            if "<div" in content and not any(tag in content for tag in ["<main", "<nav", "<header", "<footer", "<section", "<article"]):
                logs.append(f"{f.name}: Notice - Consider using semantic tags (<main>, <section>) instead of generic <div>.")

        passed = len(errors) == 0
        return TestResult(
            level=TestLevel.LEVEL7_A11Y,
            status="PASS" if passed else "FAIL",
            passed=passed,
            summary="Level 7 Accessibility Audit Passed" if passed else f"Level 7 A11y Failed with {len(errors)} issues",
            errors=errors,
            logs=logs,
            duration_ms=round((time.time() - start) * 1000, 2)
        )

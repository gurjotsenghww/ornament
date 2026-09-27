import time
from playwright.sync_api import sync_playwright

def run_test():
    print("[*] Launching headless browser to test custom Ornàment Studio...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        
        print("[*] Navigating to http://localhost:5050/...")
        page.goto("http://localhost:5050/", wait_until="networkidle")
        
        # Verify page title and header
        assert "Ornàment" in page.title() or "Ornament" in page.title()
        print(f"[OK] Page title verified: {page.title()}")
        
        greeting = page.locator("#greetingHeading").inner_text()
        print(f"[OK] Greeting detected: {greeting}")
        
        # Type prompt
        prompt_input = page.locator("#promptInput")
        prompt_text = "Create a luxury portfolio for an autonomous AI architect with dark mode, interactive terminal, and contact form"
        prompt_input.fill(prompt_text)
        print(f"[OK] Filled prompt: {prompt_text[:50]}...")
        
        # Click submit
        page.locator("#submitBtn").click()
        print("[*] Clicked Submit button...")
        
        # Verify Activity Panel appears
        activity_panel = page.locator(".activity-panel").first
        activity_panel.wait_for(state="visible", timeout=5000)
        print("[OK] Activity Panel appeared!")
        
        # Wait for generation to complete and Code Explorer to appear
        print("[*] Waiting for autonomous generation to complete...")
        code_explorer = page.locator(".code-explorer").first
        code_explorer.wait_for(state="visible", timeout=20000)
        print("[OK] Code Explorer rendered successfully!")
        
        # Verify files are populated
        tab_buttons = page.locator(".ce-tab").all()
        tab_names = [b.inner_text().strip() for b in tab_buttons]
        print(f"[OK] Tabs present: {tab_names}")
        assert any("index.html" in t for t in tab_names)
        assert any("styles.css" in t for t in tab_names)
        assert any("script.js" in t for t in tab_names)
        
        # Switch to Preview tab
        preview_btn = page.locator('.ce-toggle-btn[data-view="preview"]').first
        preview_btn.click()
        time.sleep(1)
        
        iframe = page.locator(".ce-iframe").first
        assert iframe.is_visible()
        print("[OK] Preview iframe verified!")
        
        # Test Templates modal in sidebar
        templates_nav = page.locator("#templatesNavItem")
        templates_nav.click()
        modal = page.locator("#previewModal")
        modal.wait_for(state="visible", timeout=3000)
        modal_title = page.locator("#previewTitle").inner_text()
        print(f"[OK] Templates modal opened: {modal_title}")
        page.locator("#previewClose").click()
        time.sleep(0.5)
        
        # Save screenshot
        screenshot_path = "workspace/studio_verified.png"
        page.screenshot(path=screenshot_path)
        print(f"[OK] Screenshot saved to {screenshot_path}")
        
        browser.close()
        print("[SUCCESS] All custom frontend features verified successfully!")

if __name__ == "__main__":
    run_test()

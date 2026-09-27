import time
import zipfile
import io
from playwright.sync_api import sync_playwright

def test_all():
    print("[*] Starting comprehensive feature validation for custom studio...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        print("[*] Navigating to http://localhost:5050/...")
        page.goto("http://localhost:5050/", wait_until="networkidle")

        # 1. Test Prompt Submission
        prompt_input = page.locator("#promptInput")
        prompt_input.fill("Build an eco-friendly organic coffee shop landing page")
        page.locator("#submitBtn").click()

        print("[*] Waiting for site generation...")
        page.locator(".code-explorer").first.wait_for(state="visible", timeout=15000)
        print("[OK] Generation completed and CodeExplorer rendered.")

        # 2. Test Code vs Preview Switch
        code_tab_btn = page.locator('.ce-toggle-btn[data-view="code"]').first
        preview_tab_btn = page.locator('.ce-toggle-btn[data-view="preview"]').first
        
        code_tab_btn.click()
        assert page.locator(".ce-code-view").first.is_visible()
        print("[OK] Switched to Code tab.")

        # 3. Test File Switching (styles.css & script.js)
        css_tab = page.locator('.ce-tab[data-file="css"]').first
        css_tab.click()
        time.sleep(0.3)
        code_text = page.locator(".ce-code-lines").first.inner_text()
        assert ":root" in code_text or "color" in code_text
        print("[OK] Switched to styles.css and verified syntax lines.")

        js_tab = page.locator('.ce-tab[data-file="js"]').first
        js_tab.click()
        time.sleep(0.3)
        code_text_js = page.locator(".ce-code-lines").first.inner_text()
        assert "document" in code_text_js or "addEventListener" in code_text_js
        print("[OK] Switched to script.js and verified JavaScript lines.")

        # 4. Test Copy button
        copy_btn = page.locator('[data-action="copy"]').first
        copy_btn.click()
        time.sleep(0.5)
        print("[OK] Copy action triggered.")

        # 5. Test Download ZIP
        with page.expect_download() as download_info:
            page.locator('[data-action="download"]').first.click()
        download = download_info.value
        zip_path = "workspace/test_download.zip"
        download.save_as(zip_path)
        print(f"[OK] Downloaded ZIP file: {download.suggested_filename}")

        with zipfile.ZipFile(zip_path, 'r') as z:
            names = z.namelist()
            print(f"[OK] ZIP contents: {names}")
            assert "index.html" in names
            assert "styles.css" in names
            assert "script.js" in names
        print("[OK] ZIP file verified with all 3 core website files.")

        # 6. Test Settings Modal (Hardware Telemetry)
        page.locator("#settingsNavItem").click()
        page.locator("#previewModal").wait_for(state="visible", timeout=3000)
        title = page.locator("#previewTitle").inner_text()
        assert "Settings" in title or "Telemetry" in title
        body_text = page.locator("#previewBody").inner_text()
        assert "NVIDIA RTX 3050" in body_text or "Hardware" in body_text
        print(f"[OK] Settings modal loaded telemetry: {body_text.splitlines()[0]}")
        page.locator("#previewClose").click()
        time.sleep(0.3)

        # 7. Test Projects Modal
        page.locator("#projectsNavItem").click()
        page.locator("#previewModal").wait_for(state="visible", timeout=3000)
        proj_title = page.locator("#previewTitle").inner_text()
        assert "Projects" in proj_title
        print(f"[OK] Projects modal loaded: {proj_title}")
        page.locator("#previewClose").click()
        time.sleep(0.3)

        # 8. Test Design Systems Modal
        page.locator("#designSystemsNavItem").click()
        page.locator("#previewModal").wait_for(state="visible", timeout=3000)
        ds_body = page.locator("#previewBody").inner_text()
        assert "Electric Indigo" in ds_body
        print("[OK] Design Systems modal verified.")
        page.locator("#previewClose").click()
        time.sleep(0.3)

        # 9. Test Deploy Modal
        page.locator("#deployNavItem").click()
        page.locator("#previewModal").wait_for(state="visible", timeout=3000)
        deploy_body = page.locator("#previewBody").inner_text()
        assert "ZIP Export" in deploy_body
        print("[OK] Deploy modal verified.")
        page.locator("#previewClose").click()
        time.sleep(0.3)

        # 10. Test Page Refresh & LocalStorage Persistence
        print("[*] Reloading page to test chat persistence...")
        page.reload(wait_until="networkidle")
        time.sleep(1)
        history_items = page.locator(".history-item").all()
        print(f"[OK] Found {len(history_items)} saved chat(s) in sidebar history.")
        assert len(history_items) > 0
        history_items[0].click()
        time.sleep(0.5)
        assert page.locator(".chat-message").count() > 0
        print("[OK] Chat session successfully restored from localStorage with all messages!")

        # Take final screenshot
        page.screenshot(path="workspace/studio_all_features_verified.png")
        print("[OK] Final screenshot saved to workspace/studio_all_features_verified.png")

        browser.close()
        print("\n=======================================================")
        print("   ALL 10 FEATURE SUITES PASSED WITH 100% SUCCESS!    ")
        print("=======================================================")

if __name__ == "__main__":
    test_all()

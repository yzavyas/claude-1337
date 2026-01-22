"""
Visual test for claude-1337 clean design.
"""
from playwright.sync_api import sync_playwright
import time

PORT = 5174

def test_clean_design():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})

        print(f"Testing against http://localhost:{PORT}/")

        # Homepage
        page.goto(f'http://localhost:{PORT}/')
        page.wait_for_load_state('networkidle')
        time.sleep(0.5)
        page.screenshot(path='tests/screenshots/home.png', full_page=False)
        print("✓ Homepage captured")

        # Ethos - should show actual content
        page.goto(f'http://localhost:{PORT}/ethos/')
        page.wait_for_load_state('networkidle')
        time.sleep(0.5)
        page.screenshot(path='tests/screenshots/ethos.png', full_page=False)

        ethos_content = page.content()
        if 'WORK IN PROGRESS' in ethos_content:
            print("✗ Ethos shows WIP placeholder")
        elif 'the goal' in ethos_content.lower():
            print("✓ Ethos shows actual content")
        else:
            print("○ Ethos content uncertain")

        # Explore
        page.goto(f'http://localhost:{PORT}/explore/')
        page.wait_for_load_state('networkidle')
        time.sleep(0.5)
        page.screenshot(path='tests/screenshots/explore.png', full_page=False)
        print("✓ Explore captured")

        # Start
        page.goto(f'http://localhost:{PORT}/start/')
        page.wait_for_load_state('networkidle')
        time.sleep(0.5)
        page.screenshot(path='tests/screenshots/start.png', full_page=False)
        print("✓ Start captured")

        browser.close()
        print("\n✓ Test complete - screenshots in tests/screenshots/")

if __name__ == '__main__':
    test_clean_design()

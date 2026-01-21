"""Page rendering tests for the experience site.

Run with: python tests/pages.py
Requires: playwright (pip install playwright && playwright install chromium)
"""
from playwright.sync_api import sync_playwright

BASE_URL = 'http://localhost:5173'

PAGES = [
    ('/explore/explanation/', 'explanation'),
    ('/explore/explanation/ethos/', 'ethos'),
    ('/explore/explanation/collaborative-intelligence/', 'collab'),
    ('/explore/explanation/collaborative-intelligence/extended-mind/', 'extended'),
    ('/explore/reference/research/', 'research'),
    ('/explore/reference/catalog/', 'catalog'),
    ('/start/', 'start'),
    ('/', 'home'),
]


def test_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 900})

        results = []
        for path, name in PAGES:
            try:
                page.goto(f'{BASE_URL}{path}', timeout=10000)
                page.wait_for_load_state('networkidle', timeout=5000)
                results.append((name, 'OK', None))
                print(f'✓ {name}')
            except Exception as e:
                results.append((name, 'FAIL', str(e)))
                print(f'✗ {name}: {e}')

        browser.close()

        failed = [r for r in results if r[1] == 'FAIL']
        if failed:
            print(f'\n{len(failed)} failed')
            return 1
        print(f'\nAll {len(results)} pages OK')
        return 0


def test_mermaid():
    """Test that mermaid diagrams render."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f'{BASE_URL}/explore/explanation/ethos/')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)  # Wait for mermaid async render

        svg_count = page.locator('.mermaid-wrapper svg').count()
        browser.close()

        if svg_count > 0:
            print(f'✓ Mermaid: {svg_count} diagrams rendered')
            return 0
        else:
            print('✗ Mermaid: no diagrams found')
            return 1


if __name__ == '__main__':
    import sys
    exit_code = test_pages()
    exit_code += test_mermaid()
    sys.exit(exit_code)

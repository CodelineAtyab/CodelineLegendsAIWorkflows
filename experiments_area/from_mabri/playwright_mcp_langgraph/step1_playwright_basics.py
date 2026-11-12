"""Step 1 - Plain Playwright: YOU write the steps, Playwright clicks them.

Opens the local registration form in a visible (headed) Chromium window,
checks that validation rejects an empty form, then registers successfully.

Run:  uv run python step1_playwright_basics.py
"""

from pathlib import Path

from playwright.sync_api import expect, sync_playwright

FORM_URL = (Path(__file__).parent / "demo_site" / "index.html").resolve().as_uri()
FULL_NAME = "Mohammed Al Abri"


def main() -> None:
    with sync_playwright() as p:
        # headless=False -> you SEE the browser; slow_mo pauses 500 ms per action.
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto(FORM_URL)

        # Locators are lazy "recipes" for finding elements. They are resolved
        # (and auto-waited) only when an action like .click() runs.
        register_button = page.get_by_role("button", name="Register")
        result = page.get_by_role("status")

        # 1) Negative test: an empty form must be rejected.
        register_button.click()
        expect(result).to_contain_text("Full name must be at least 3 characters")
        print("Empty form rejected ->", result.inner_text())

        # 2) Fill every field using user-facing labels (no CSS selectors).
        page.get_by_label("Full name").fill(FULL_NAME)
        page.get_by_label("Email").fill("mabri@example.com")
        page.get_by_label("Discipline").select_option("software")
        page.get_by_label("Years of experience").fill("3")
        page.get_by_label("I accept the terms").check()

        # 3) Positive test: submit and assert the exact success message.
        register_button.click()
        expect(result).to_have_text(f"Registered {FULL_NAME} as a software engineer.")
        print("Registration succeeded ->", result.inner_text())

        page.screenshot(path="outputs/step1_success.png")
        print("Screenshot saved to outputs/step1_success.png")
        browser.close()


if __name__ == "__main__":
    main()

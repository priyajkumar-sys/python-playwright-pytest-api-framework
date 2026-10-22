import pytest
from playwright.sync_api import Playwright, Page

@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture(scope="session")
def base_url():
    return "https://www.saucedemo.com"

@pytest.fixture
def logged_in_page(page: Page, base_url):
    page.goto(base_url)
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    return page
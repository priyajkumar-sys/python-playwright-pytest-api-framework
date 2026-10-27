import pytest
from playwright.sync_api import Playwright, Page, Browser, BrowserContext
from collections.abc import Generator
from config import STANDARD_USERNAME, VALID_PASSWORD
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture(scope="session")
def base_url():
    return "https://www.saucedemo.com"

@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)

@pytest.fixture(scope="function")
def logged_in_page(browser: Browser) -> Generator[Page, None, None]:
    context = browser.new_context()

    try:
        page = context.new_page()

        login_page = LoginPage(page)
        login_page.login(
            "https://www.saucedemo.com",
            STANDARD_USERNAME,
            VALID_PASSWORD
        )

        page.wait_for_url("**/inventory.html")

        yield page

    finally:
        context.close()

@pytest.fixture
def cart_page(logged_in_page: Page) -> CartPage:
    return CartPage(logged_in_page)

@pytest.fixture
def inventory_page(logged_in_page: Page) -> InventoryPage:
    return InventoryPage(logged_in_page)

@pytest.fixture
def checkout_page(logged_in_page: Page) -> CheckoutPage:
    return CheckoutPage(logged_in_page)
import json
from pathlib import Path

import pytest
from playwright.sync_api import Playwright, Page, Browser, BrowserContext
from collections.abc import Generator

from Utils.apiBase import APIUtils
from config import STANDARD_USERNAME, VALID_PASSWORD
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.lazy_catalog_page import LazyCatPage
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

@pytest.fixture
def lazy_catalog_page(logged_in_page: Page) -> LazyCatPage:
    catalog = LazyCatPage(logged_in_page)
    catalog.page.goto("https://www.saucedemo.com/dynamic-catalog-lazy-load.html")
    return catalog

BASE_DIR = Path(__file__).resolve().parent


@pytest.fixture
def load_payload():
    def _load(filename):
        filepath = BASE_DIR / "test_data/api_payloads" / filename
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    return _load

@pytest.fixture
def api_context(playwright: Playwright):
    api = playwright.request.new_context(base_url="https://restful-booker.herokuapp.com")
    yield api
    api.dispose()

@pytest.fixture
def auth_headers(api_context, load_payload):
    client = APIUtils(api_context)
    credentials = load_payload("auth.json")
    return client.authenticate(credentials)

@pytest.fixture
def created_booking(api_context, load_payload):
    payload = load_payload("create_booking.json")
    response = api_context.post("/booking", data=payload)
    assert response.status == 200
    booking_id = response.json()["bookingid"]
    return booking_id



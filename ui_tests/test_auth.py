from playwright.sync_api import Page, expect
import time
import pytest
from pages.login_page import LoginPage

def test_login_with_invalid_password(page:Page, base_url, login_page: LoginPage, saucedemo_credentials):
    username = saucedemo_credentials["sauceDemoInvalidUsername"]
    password = saucedemo_credentials["sauceDemoInvalidPassword"]
    login_page.attempt_login(base_url, username, password)
    expect(page.get_by_text("Epic sadface: Username and password do not match any user in this service")).to_be_visible()
    expect(page).to_have_url(base_url.rstrip("/") + "/")

def test_locked_out_user_login(page: Page, base_url, login_page: LoginPage, saucedemo_credentials):
    username = saucedemo_credentials["sauceDemoLockedOutUsername"]
    password = saucedemo_credentials["sauceDemoPassword"]
    login_page.attempt_login(base_url, username, password)
    expect(page.get_by_text("Epic sadface: Sorry, this user has been locked out.")).to_be_visible()
    expect(page).to_have_url(base_url.rstrip("/") + "/")

def test_performance_glitch_user_login(
    page: Page,
    base_url,
    login_page: LoginPage,
    saucedemo_credentials
):
    login_page.page.goto(base_url)
    username = saucedemo_credentials["sauceDemoPerformanceglitchUsername"]
    password = saucedemo_credentials["sauceDemoPassword"]
    login_page.enter_credentials(username, password)
    start_time = time.perf_counter()
    login_page.submit_login()
    expect(page).to_have_url(
        base_url.rstrip("/") + "/inventory.html",
        timeout=15000)
    expect(page.locator(".inventory_item")).to_have_count(
        6, timeout=15000)
    login_duration = time.perf_counter() - start_time
    print(f"\nLogin duration: {login_duration:.2f} seconds")

def test_valid_login(base_url, login_page: LoginPage, saucedemo_credentials):
    username = saucedemo_credentials["sauceDemoValidUsername"]
    password = saucedemo_credentials["sauceDemoPassword"]
    login_page.login(base_url, username, password)
    expect(login_page.page).to_have_url(
        base_url.rstrip("/") + "/inventory.html")
    expect(login_page.page.get_by_test_id("inventory-container")).to_be_visible()

def test_error_user_login(page: Page, base_url, login_page: LoginPage, saucedemo_credentials):
    username = saucedemo_credentials["sauceDemoErrorUsername"]
    password = saucedemo_credentials["sauceDemoPassword"]
    login_page.attempt_login(base_url, username, password)
    expect(page).to_have_url(base_url.rstrip("/") + "/inventory.html")
    expect(page.get_by_test_id("inventory-container")).to_be_visible()

def test_visual_user_login(page: Page, base_url, login_page: LoginPage, saucedemo_credentials):
    username = saucedemo_credentials["sauceDemoVisualUsername"]
    password = saucedemo_credentials["sauceDemoPassword"]
    login_page.login(base_url, username, password)
    expect(page).to_have_url(base_url.rstrip("/") + "/inventory.html")
    expect(page.get_by_test_id("inventory-container")).to_be_visible()

@pytest.mark.parametrize(
    argnames="username_key,password_key,expected_error",
    argvalues=[
        ("", "", "Epic sadface: Username is required"),
        ("", "sauceDemoPassword", "Epic sadface: Username is required"),
        ("sauceDemoValidUsername", "", "Epic sadface: Password is required"),
    ],
    ids=[
        "both-fields-empty",
        "username-empty",
        "password-empty",
    ],
)
def test_login_required_fields(
    page: Page,
    base_url,
    username_key,
    password_key,
    expected_error,
    login_page: LoginPage,
    load_payload
):
    data = load_payload("saucedemo_credentials.json")
    credentials = data["user_credentials"][0]

    username = credentials[username_key] if username_key else ""
    password = credentials[password_key] if password_key else ""

    login_page.attempt_login(base_url, username, password)

    expect(page.get_by_text(expected_error)).to_be_visible()
    expect(page).to_have_url(base_url.rstrip("/") + "/")

@pytest.mark.parametrize(
    "login_credentials",
    [
        "sauceDemoValidUsername",
        "sauceDemoErrorUsername",
        "sauceDemoVisualUsername"
    ],
    indirect=True
)
def test_successful_login(
    page: Page,
    base_url,
    login_page: LoginPage,
    login_credentials
):
    login_page.login(
        base_url,
        login_credentials["username"],
        login_credentials["password"]
    )

    expect(page).to_have_url(
        base_url.rstrip("/") + "/inventory.html"
    )
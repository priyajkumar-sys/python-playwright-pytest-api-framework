from playwright.sync_api import Page, expect

# chromium headless mode using 1 browser context
# browser = playwright.chromium.launch(headless=False)
# context = browser.new_context()
# page = context.new_page()
# page.goto("http....")

def test_login_with_invalid_password(page:Page, base_url):
    page.goto(base_url)
    page.locator("#user-name").fill("problem_user")
    page.locator("#password").fill("secret_sauces1")
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text("Epic sadface: Username and password do not match any user in this service")).to_be_visible()
    expect(page).to_have_url(base_url.rstrip("/") + "/")

def test_valid_login(page:Page, base_url, logged_in_page):
    page = logged_in_page
    expect(page).to_have_url(base_url + "/inventory.html")
    expect(page.get_by_test_id("inventory-container")).to_be_visible()


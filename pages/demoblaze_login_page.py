from playwright.sync_api import Page, expect


class DBLoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.login_modal = page.locator("#login2")
        self.username_input = page.locator("#loginusername")
        self.password_input = page.locator("#loginpassword")
        self.login_button = page.get_by_role("link", name="Log in")
        self.submit_button = page.get_by_role("button", name="Log in")

    def enter_credentials(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)

    def login(self, base_url, username, password):
        self.page.goto(base_url)
        self.login_button.click()
        # Wait for the modal to become visible
        expect(self.login_modal).to_be_visible()
        self.enter_credentials(username, password)
        self.submit_button.click()


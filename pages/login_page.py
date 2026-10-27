from playwright.sync_api import Page


class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.get_by_role("button", name="Login")

    def enter_credentials(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)

    def submit_login(self):
        self.login_button.click()

    def login(self, base_url, username, password):
        self.page.goto(base_url)
        self.enter_credentials(username, password)
        self.submit_login()


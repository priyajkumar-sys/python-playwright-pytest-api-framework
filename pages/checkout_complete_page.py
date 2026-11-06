from playwright.sync_api import Page, expect

from config import SAUCEDEMO_URL


class CheckoutCompletePage:

    def __init__(self, page: Page):
        self.page = page
        self.complete_header = page.get_by_test_id("complete-header")
        self.complete_text = page.get_by_test_id("complete-text")
        self.back_home_button = page.get_by_test_id("back-to-products")

    def verify_order_success(self):
        expect(self.page).to_have_url(
            SAUCEDEMO_URL + "/checkout-complete.html"
        )

        expect(self.complete_header).to_have_text(
            "Thank you for your order!"
        )

        expect(self.complete_text).to_be_visible()


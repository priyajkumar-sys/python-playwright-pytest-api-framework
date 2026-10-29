from playwright.sync_api import Page


class CheckoutPage:

    def __init__(self, page: Page):
        self.page = page
        self.page_title = page.get_by_text("Checkout: Your Information", exact=True)
        self.checkout_button = page.get_by_role("button", name="checkout")
        self.first_name = page.get_by_placeholder("First Name")
        self.last_name = page.get_by_placeholder("Last Name")
        self.pincode = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.error_message = page.get_by_test_id("error")
        self.sub_total = page.get_by_test_id("subtotal-label")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.cart_items = page.locator(".cart_item")
        self.finish_button = page.get_by_role("button", name="Finish")
        self.complete_header = page.get_by_test_id("complete-header")
        self.complete_text = page.get_by_test_id("complete-text")
        self.download_pdf_button = page.get_by_role("button", name="Generate PDF order")

    def start_checkout(self):
        self.checkout_button.click()

    def enter_customer_information(
            self, first_name, last_name, postal_code
    ):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.pincode.fill(postal_code)

    def continue_checkout(self):
        self.continue_button.click()
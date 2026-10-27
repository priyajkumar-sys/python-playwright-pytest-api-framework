from playwright.sync_api import Page


class CartPage:

    def __init__(self, page: Page):
        self.page = page
        self.cart_page_title = page.get_by_text("Your Cart", exact=True)
        self.cart_page_quantity_title = page.get_by_text("QTY", exact=True)
        self.cart_page_desc_title = page.get_by_text("Description", exact=True)
        self.cart_page_cont_shop_button = page.get_by_test_id("continue-shopping")
        self.cart_page_cont_shop_button = page.get_by_test_id("checkout")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.add_cart_buttons = page.get_by_role("button", name="Add to cart")
        self.remove_cart_buttons = page.get_by_role("button", name="Remove")
        self.cart_items = page.locator(".cart_item")

    def open_cart(self):
        self.page.get_by_test_id("shopping-cart-link").click()



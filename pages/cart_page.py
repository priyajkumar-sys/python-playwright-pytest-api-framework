from playwright.sync_api import Page, expect

from pages.checkout_page import CheckoutPage


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
        self.cart_item_cost = page.get_by_test_id("inventory-item-price")

    def open_cart(self):
        self.page.get_by_test_id("shopping-cart-link").click()
        self.page.wait_for_url("**/cart.html")
        return CartPage(self.page)

    def checkout(self) -> CheckoutPage:
        self.page.get_by_test_id("checkout").click()
        self.page.wait_for_url("**/checkout-step-one.html")
        return CheckoutPage(self.page)

    def verify_product(self, product_name: str):
        product = self.page.get_by_test_id("inventory-item-name").filter(
            has_text=product_name
        )
        expect(product).to_be_visible()


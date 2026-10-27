import random

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from playwright.sync_api import Page, expect
import pytest

class TestCheckout:

    page: Page

    def test_checkout_page_loads(self, checkout_page: CheckoutPage, inventory_page: InventoryPage, cart_page: CartPage):
        all_items = inventory_page.inventory_items
        expect(all_items.first).to_be_visible()
        random_item = random.choice(all_items.all())
        random_item.get_by_role("button", name="Add to cart").click()
        cart_page.open_cart()
        expect(cart_page.page).to_have_url("https://www.saucedemo.com/cart.html")
        checkout_page.start_checkout()
        expect(checkout_page.page).to_have_url(
            "https://www.saucedemo.com/checkout-step-one.html"
        )
        expect(checkout_page.first_name).to_be_visible()
        expect(checkout_page.last_name).to_be_visible()
        expect(checkout_page.pincode).to_be_visible()

    def test_checkout_required_fields_error_validation(self, cart_page: CartPage, inventory_page: InventoryPage, checkout_page: CheckoutPage):
        # Add product and navigate to checkout
        inventory_page.inventory_items.first.get_by_role(
            "button", name="Add to cart").click()
        cart_page.open_cart()
        checkout_page.start_checkout()

        # Validation 1: All fields empty
        checkout_page.continue_checkout()
        expect(checkout_page.error_message).to_have_text("Error: First Name is required")

        # Validation 2: Last name missing
        checkout_page.first_name.fill("Priya")
        checkout_page.continue_checkout()
        expect(checkout_page.error_message).to_have_text("Error: Last Name is required")

        # Validation 3: Postal code missing
        checkout_page.last_name.fill("Kumar")
        checkout_page.continue_checkout()
        expect(checkout_page.error_message).to_have_text("Error: Postal Code is required")
        expect(checkout_page.page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    def test_valid_checkout_information(self, cart_page: CartPage, inventory_page: InventoryPage,
                                      checkout_page: CheckoutPage):
        # Add product and navigate to checkout
        inventory_page.inventory_items.first.get_by_role(
            "button", name="Add to cart").click()
        cart_page.open_cart()
        checkout_page.start_checkout()
        checkout_page.first_name.fill("Priya")
        checkout_page.last_name.fill("Kumar")
        checkout_page.pincode.fill("60061")
        checkout_page.continue_checkout()
        expect(checkout_page.page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

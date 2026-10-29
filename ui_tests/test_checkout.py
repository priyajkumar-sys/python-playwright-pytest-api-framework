import random
import time
from decimal import Decimal
from pathlib import Path

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
        checkout_page.enter_customer_information("Priya", "Kumar", "60061")
        checkout_page.continue_checkout()
        expect(checkout_page.page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

    def test_items_total_price_accurate(self, cart_page: CartPage, inventory_page: InventoryPage, checkout_page: CheckoutPage):
        all_items = inventory_page.inventory_items
        expect(all_items).to_have_count(6)
        selected_items = random.sample(all_items.all(), 2)
        for item in selected_items:
            item.get_by_role("button", name="Add to cart").click()
        cart_page.open_cart()
        all_prices = cart_page.cart_item_cost.all_text_contents()
        prices = [Decimal(price.replace("$", "")) for price in all_prices]
        expected_sum_price = sum(prices)
        checkout_page.start_checkout()
        checkout_page.enter_customer_information("Priya", "Kumar", "60061")
        checkout_page.continue_checkout()
        sum_price = checkout_page.sub_total.inner_text()
        actual_sum_price = Decimal(sum_price.split("$")[1]).quantize(Decimal("0.01"))
        assert actual_sum_price == expected_sum_price

    def test_cancelling_checkout_preserves_cart(self, cart_page: CartPage, inventory_page: InventoryPage, checkout_page: CheckoutPage):
        all_items = inventory_page.inventory_items
        expect(all_items).to_have_count(6)
        selected_items = random.sample(all_items.all(), 3)
        for item in selected_items:
            item.get_by_role("button", name="Add to cart").click()
        cart_page.open_cart()
        checkout_page.start_checkout()
        checkout_page.enter_customer_information("Priya", "Kumar", "60061")
        checkout_page.continue_checkout()
        expect(checkout_page.page.get_by_role(
            "button", name="Cancel")).to_be_visible()
        expected_item_count = checkout_page.cart_items.count()
        checkout_page.cancel_button.click()
        cart_page.open_cart()
        actual_item_count = cart_page.cart_items.count()
        assert actual_item_count == expected_item_count

    def test_successful_order_completion(self, cart_page: CartPage, inventory_page: InventoryPage, checkout_page: CheckoutPage):
        all_items = inventory_page.inventory_items
        expect(all_items).to_have_count(6)
        selected_items = random.sample(all_items.all(), 2)
        for item in selected_items:
            item.get_by_role("button", name="Add to cart").click()
        cart_page.open_cart()
        all_prices = cart_page.cart_item_cost.all_text_contents()
        prices = [Decimal(price.replace("$", "")) for price in all_prices]
        checkout_page.start_checkout()
        checkout_page.enter_customer_information("Priya", "Kumar", "60061")
        checkout_page.continue_checkout()
        checkout_page.finish_button.click()
        expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
        expect(checkout_page.complete_text).to_have_text("Your order has been dispatched, and will arrive just as fast as the pony can get there!")

    def test_generate_order_pdf(self, cart_page: CartPage, inventory_page: InventoryPage, checkout_page: CheckoutPage):
        all_items = inventory_page.inventory_items
        expect(all_items).to_have_count(6)
        selected_items = random.sample(all_items.all(), 2)
        for item in selected_items:
            item.get_by_role("button", name="Add to cart").click()
        cart_page.open_cart()
        all_prices = cart_page.cart_item_cost.all_text_contents()
        prices = [Decimal(price.replace("$", "")) for price in all_prices]
        checkout_page.start_checkout()
        checkout_page.enter_customer_information("Priya", "Kumar", "60061")
        checkout_page.continue_checkout()
        checkout_page.finish_button.click()
        expect(checkout_page.page).to_have_url(
            "https://www.saucedemo.com/checkout-complete.html")
        with checkout_page.page.expect_download() as download_info:
            checkout_page.download_pdf_button.click()
        download = download_info.value
        assert download.suggested_filename.endswith(".pdf")
        assert download.failure() is None
        pdf_path = Path(download.path())
        assert pdf_path.exists()
        assert pdf_path.stat().st_size > 0
        with pdf_path.open("rb") as pdf_file:
            assert pdf_file.read(5) == b"%PDF-"



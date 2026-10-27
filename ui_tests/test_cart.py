import random

from playwright.sync_api import Page, expect
from conftest import base_url
import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


class TestInventory:

    page: Page

    def test_add_product_to_cart(self, cart_page: CartPage):
        add_buttons = cart_page.add_cart_buttons
        expect(add_buttons.first).to_be_visible()
        add_buttons = cart_page.add_cart_buttons.all()
        random_button = random.choice(add_buttons)
        random_button.click()
        expect(cart_page.cart_badge).to_have_text("1")

    def test_remove_product_from_cart(self, cart_page: CartPage):
        add_buttons = cart_page.add_cart_buttons
        expect(add_buttons.first).to_be_visible()
        add_buttons = cart_page.add_cart_buttons.all()
        random_button = random.choice(add_buttons)
        random_button.click()
        expect(cart_page.cart_badge).to_have_text("1")
        cart_page.remove_cart_buttons.click()
        expect(cart_page.cart_badge).not_to_be_visible()

    def test_correct_product_added_to_cart(self, cart_page: CartPage, inventory_page: InventoryPage):
        all_items = inventory_page.inventory_items
        expect(all_items.first).to_be_visible()
        random_item = random.choice(all_items.all())
        expected_item_name = random_item.get_by_test_id(
            "inventory-item-name"
        ).inner_text()
        random_item.get_by_role("button", name="Add to cart").click()
        cart_page.open_cart()
        expect(cart_page.page).to_have_url("https://www.saucedemo.com/cart.html")
        actual_item_name = cart_page.page.locator(
            ".cart_item"
        ).get_by_test_id("inventory-item-name").inner_text()
        assert actual_item_name == expected_item_name


    def test_multiple_products_added_to_cart(self, cart_page: CartPage, inventory_page: InventoryPage):
        all_items = inventory_page.inventory_items
        expect(all_items).to_have_count(6)
        selected_items = random.sample(all_items.all(), 3)
        for item in selected_items:
            item.get_by_role("button", name="Add to cart").click()
        expect(cart_page.cart_badge).to_have_text("3")

    def test_continue_shopping_from_cart(self, cart_page: CartPage, inventory_page: InventoryPage):
        all_items = inventory_page.inventory_items
        expect(all_items.first).to_be_visible()
        random_item = random.choice(all_items.all())
        random_item.get_by_role("button", name="Add to cart").click()
        cart_page.open_cart()
        cart_page.page.get_by_role("button", name="Continue Shopping").click()
        expect(inventory_page.inventory_items).to_have_count(6)
        expect(cart_page.cart_badge).to_have_text("1")
        expect(random_item.get_by_role("button", name="Remove")).to_be_visible()








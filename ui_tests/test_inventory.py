from pages.inventory_page import InventoryPage
from playwright.sync_api import Page, expect
import pytest

class TestInventory:

    page: Page

    def test_inventory_page_loads(self, inventory_page: InventoryPage):
        expect(inventory_page.inventory_container).to_be_visible()
        expect(inventory_page.page_title).to_be_visible()

    def test_inventory_count(self, inventory_page: InventoryPage):
        expect(inventory_page.inventory_items).to_have_count(6)

    def test_product_details(self, inventory_page: InventoryPage):
        for item in inventory_page.inventory_items.all():
            name = item.get_by_test_id("inventory-item-name")
            price = item.get_by_test_id("inventory-item-price")
            expect(name).to_be_visible()
            expect(price).to_be_visible()
            assert name.inner_text().strip() != ""
            assert price.inner_text().strip() != ""

    def test_sort_products_a_to_z(self, inventory_page: InventoryPage):
        inventory_page.sort_by_name_a_to_z()
        product_names = inventory_page.inventory_name.all_text_contents()
        expected_names = sorted(product_names)
        assert product_names == expected_names

    def test_sort_products_z_to_a(self, inventory_page: InventoryPage):
        inventory_page.sort_by_name_z_to_a()
        product_names = inventory_page.inventory_name.all_text_contents()
        expected_names = sorted(product_names, reverse=True)
        assert product_names == expected_names

    def test_sort_price_low_to_high(self, inventory_page: InventoryPage):
        inventory_page.sort_by_price_low_to_high()
        product_prices = inventory_page.inventory_price.all_text_contents()
        prices = [float(price.replace("$", "")) for price in product_prices]
        expected_prices = sorted(prices)
        assert prices == expected_prices

    def test_sort_price_high_to_low(self, inventory_page: InventoryPage):
        inventory_page.sort_by_price_high_to_low()
        prices = inventory_page.inventory_price.all_text_contents()
        prices = [float(price.replace("$", "")) for price in prices]
        expected_prices = sorted(prices, reverse=True)
        assert prices == expected_prices






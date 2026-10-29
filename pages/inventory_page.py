from playwright.sync_api import Page


class InventoryPage:

    def __init__(self, page: Page):
        self.page = page
        self.inventory_items = page.get_by_test_id("inventory-item")
        self.inventory_container = page.get_by_test_id("inventory-container")
        self.page_title = page.get_by_text("Swag Labs", exact=True)
        self.inventory_title = page.get_by_text("Products", exact=True)
        self.inventory_name = page.get_by_test_id("inventory-item-name")
        self.inventory_price = page.get_by_test_id("inventory-item-price")
        self.sort_dropdown = page.get_by_test_id("product-sort-container")

    def sort_by_name_a_to_z(self):
        self.sort_dropdown.select_option("az")

    def sort_by_name_z_to_a(self):
        self.sort_dropdown.select_option("za")

    def sort_by_price_low_to_high(self):
        self.sort_dropdown.select_option("lohi")

    def sort_by_price_high_to_low(self):
        self.sort_dropdown.select_option("hilo")





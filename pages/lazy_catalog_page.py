from playwright.sync_api import Page


class LazyCatPage:

    def __init__(self, page: Page):
        self.page = page
        self.page_title = page.get_by_text("Dynamic Catalog - Lazy Load", exact=True)
        self.catalog_container = page.get_by_test_id("dynamic-catalog-lazy-load-container")
        self.items = page.locator(".dynamic_catalog_card")
        self.item_name = page.locator(".dynamic_catalog_card_name")
from pages.lazy_catalog_page import LazyCatPage
from playwright.sync_api import Page, expect
import pytest

class TestCheckout:

    page: Page

    def test_products_load_on_scroll(self, lazy_catalog_page: LazyCatPage):
        expect(lazy_catalog_page.page_title).to_be_visible()
        expect(lazy_catalog_page.catalog_container).to_be_visible()
        initial_items_count = lazy_catalog_page.items.count()
        lazy_catalog_page.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        expect(lazy_catalog_page.items.nth(initial_items_count)).to_be_attached(timeout=10000)
        final_items_count = lazy_catalog_page.items.count()
        assert final_items_count > initial_items_count




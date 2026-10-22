from playwright.sync_api import Page, expect
from conftest import base_url


def test_ui_dynamic_validations(page:Page, base_url):
    page.goto(base_url)
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    item1 = page.locator(".inventory_item").filter(has_text="Sauce Labs Bike Light")
    item1.get_by_role("button", name="Add to cart").click()
    item2 = page.locator(".inventory_item").filter(has_text="Test.allTheThings() T-Shirt (Red)")
    item2.get_by_role("button", name="Add to cart").click()
    # page.get_by_role("button", name="Cart", exact=False).click()
    page.get_by_test_id("shopping-cart-link").click()
    expect(page).to_have_url(base_url + "/cart.html")
    expect(page.get_by_text("Sauce Labs Bike Light", exact=True)).to_be_visible()
    expect(page.locator(".cart_item")).to_have_count(2)


# This is basically accepting an alert box - an event listener
# lamda are anonymous one-liner functions - accepts a parameter which is dialog here
# page.on("dialog", lamda dialog: dialog.accept())






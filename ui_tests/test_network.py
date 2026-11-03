import pytest
from playwright.sync_api import Page, expect

from config import DB_USERNAME1, DB_PASSWORD1
from conftest import load_payload


def intercept_response(route, fake_payload):
    route.fulfill(
        json = fake_payload
    )


@pytest.mark.parametrize(
    "demoblaze_logged_in_page",
    [(DB_USERNAME1, DB_PASSWORD1)],
    indirect=True,
    ids=["user1"]
)
def test_network_intercept_response(demoblaze_logged_in_page ,load_payload):
    page = demoblaze_logged_in_page
    fake_payload = load_payload("fake_payload.json")
    page.goto("https://www.demoblaze.com/")
    page.route("https://api.demoblaze.com/viewcart", lambda route: intercept_response(route, fake_payload))
    page.get_by_role("link", name="Cart").click()
    expect(page.locator("#tbodyid tr")).to_have_count(0)

def intercept_request(route):
    route.abort()

@pytest.mark.parametrize(
    "demoblaze_logged_in_page",
    [(DB_USERNAME1, DB_PASSWORD1)],
    indirect=True,
    ids=["user1"]
)
def test_network_intercept_request(demoblaze_logged_in_page):
    page = demoblaze_logged_in_page
    page.route("**/viewcart", intercept_request)
    page.get_by_role("link", name="Cart").click()






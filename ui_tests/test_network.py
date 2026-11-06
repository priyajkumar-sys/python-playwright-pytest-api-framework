from urllib import request

import pytest
from playwright.sync_api import Page, expect, Playwright
from Utils.apiBase import APIUtils
from config import DB_USERNAME1, DB_PASSWORD1, DB_USERNAME2, DB_PASSWORD2, DEMOBLAZE_URL
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
    page.goto(DEMOBLAZE_URL)
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

def test_session_storage(playwright: Playwright,load_payload):
    # 1. Create API context for Demoblaze
    api_context = playwright.request.new_context(
        base_url="https://api.demoblaze.com"
    )

    try:
        # 2. Authenticate using Demoblaze credentials
        api_utils = APIUtils(api_context)
        credentials = {
            "username": DB_USERNAME2,
            "password": DB_PASSWORD2
        }

        response = api_utils.authenticate("/login", credentials)

        # 3. Inspect the authentication response
        print("Status:", response.status)
        print("Response type:", response.headers.get("content-type"))

    finally:
        api_context.dispose()








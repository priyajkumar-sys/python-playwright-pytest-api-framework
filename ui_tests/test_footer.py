import re
from playwright.sync_api import Page, expect
import pytest

#this has child window handling
@pytest.mark.parametrize(
    "social_icon, expected_url",
    [
        ("social-x", "x.com"),
        ("social-facebook", "facebook.com"),
        ("social-linkedin", "linkedin.com"),
    ]
)
def test_footer_section(page:Page, logged_in_page, social_icon, expected_url):
    page = logged_in_page
    with page.expect_popup() as new_social_page:
        page.get_by_test_id("social-x").click()

    child_page = new_social_page.value
    expect(child_page).to_have_url(re.compile(r"x\.com"))
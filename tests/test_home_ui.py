"""Home page UI test suite for automationexercise.com.

Covers Test Case 10, 25, 26 published at
https://www.automationexercise.com/test_cases.
"""

import allure

from pages.home_page import HomePage
from utils.allure_steps import step


@allure.feature("Home Page UI")
@allure.title("Test Case 10: Verify Subscription in home page")
def test_verify_subscription_in_home_page(home_page: HomePage):
    """Test Case 10: Verify Subscription in home page."""
    page = home_page.page
    email = "qa_home_subscribe_check@example.com"

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Scroll down to footer"):
        home_page.scroll_to_footer()

    with step(page, "5. Verify text 'SUBSCRIPTION'"):
        home_page.verify_subscription_heading_visible()

    with step(page, f"6. Enter email address '{email}' in input and click arrow button"):
        home_page.subscribe(email)

    with step(page, "7. Verify success message 'You have been successfully subscribed!' is visible"):
        home_page.verify_subscription_success()


@allure.feature("Home Page UI")
@allure.title("Test Case 25: Verify Scroll Up using 'Arrow' button and Scroll Down functionality")
def test_scroll_up_using_arrow_button(home_page: HomePage):
    """Test Case 25: Verify Scroll Up using 'Arrow' button and Scroll Down functionality."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4-5. Scroll down page to bottom and verify 'SUBSCRIPTION' is visible"):
        home_page.verify_scrolled_to_bottom_with_subscription()

    with step(page, "6. Click on arrow at bottom right side to move upward"):
        home_page.click_scroll_up_arrow()

    with step(page, "7. Verify that page is scrolled up and hero text is visible on screen"):
        home_page.verify_scrolled_to_top()


@allure.feature("Home Page UI")
@allure.title("Test Case 26: Verify Scroll Up without 'Arrow' button and Scroll Down functionality")
def test_scroll_up_without_arrow_button(home_page: HomePage):
    """Test Case 26: Verify Scroll Up without 'Arrow' button and Scroll Down functionality."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4-5. Scroll down page to bottom and verify 'SUBSCRIPTION' is visible"):
        home_page.verify_scrolled_to_bottom_with_subscription()

    with step(page, "6. Scroll up page to top WITHOUT the arrow button"):
        home_page.scroll_to_top_without_arrow()

    with step(page, "7. Verify that page is scrolled up and hero text is visible on screen"):
        home_page.verify_scrolled_to_top()

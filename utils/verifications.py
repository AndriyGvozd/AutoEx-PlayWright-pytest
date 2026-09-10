"""Test-facing assertion helpers, kept deliberately separate from pages/.

Page Objects (pages/*.py) only encapsulate locators and page interactions;
they never assert pass/fail outcomes about test correctness. These
`assert_*` functions are that separate verification layer: each one takes
the Page Object(s) it needs, reads the locators/data they expose, and makes
the actual `expect()`/`assert` calls. Tests call these instead of embedding
assertions inline or inside a Page Object method, keeping "how to interact
with the page" and "what counts as correct" as two independent concerns.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from playwright.sync_api import expect

if TYPE_CHECKING:
    from pages.account_created_page import AccountCreatedPage
    from pages.account_deleted_page import AccountDeletedPage
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage
    from pages.contact_us_page import ContactUsPage
    from pages.home_page import HomePage
    from pages.payment_page import PaymentPage
    from pages.product_detail_page import ProductDetailPage
    from pages.products_page import ProductsPage
    from pages.signup_login_page import SignupLoginPage


# --- Home page -------------------------------------------------------------


def assert_home_page_visible(home_page: "HomePage") -> None:
    expect(home_page.page).to_have_url(re.compile(r"automationexercise\.com"))
    expect(home_page.logo).to_be_visible()


def assert_logged_in_as(home_page: "HomePage", username: str) -> None:
    expect(home_page.logged_in_as_text).to_be_visible()
    expect(home_page.logged_in_as_text).to_contain_text(f"Logged in as {username}")


def assert_navigated_to_test_cases_page(home_page: "HomePage") -> None:
    expect(home_page.page).to_have_url(re.compile(r"/test_cases$"))


def assert_recommended_items_visible(home_page: "HomePage") -> None:
    expect(home_page.recommended_heading).to_be_visible()
    expect(home_page.recommended_items.first).to_be_visible()


def assert_scrolled_to_top(home_page: "HomePage") -> None:
    expect(home_page.hero_text.first).to_be_visible(timeout=15000)


# --- Subscription (shared markup/ids between HomePage and CartPage) --------


def assert_subscription_heading_visible(page_with_subscription) -> None:
    expect(page_with_subscription.subscribe_heading).to_be_visible()
    expect(page_with_subscription.subscribe_heading).to_have_text("Subscription")


def assert_subscription_success(page_with_subscription) -> None:
    expect(page_with_subscription.subscribe_success_message).to_be_visible()
    expect(page_with_subscription.subscribe_success_message).to_contain_text(
        "You have been successfully subscribed!"
    )


# --- Signup / Login ----------------------------------------------------------


def assert_new_user_signup_visible(signup_login_page: "SignupLoginPage") -> None:
    expect(signup_login_page.new_user_signup_heading).to_be_visible()


def assert_login_to_account_visible(signup_login_page: "SignupLoginPage") -> None:
    expect(signup_login_page.page).to_have_url(re.compile(r"/login$"))
    expect(signup_login_page.login_to_account_heading).to_be_visible()


def assert_login_error_visible(signup_login_page: "SignupLoginPage") -> None:
    expect(signup_login_page.login_error_message).to_be_visible()


def assert_signup_error_visible(signup_login_page: "SignupLoginPage") -> None:
    expect(signup_login_page.signup_error_message).to_be_visible()


# --- Registration ------------------------------------------------------------


def assert_account_info_visible(signup_page) -> None:
    expect(signup_page.account_info_heading).to_be_visible()


def assert_account_created(account_created_page: "AccountCreatedPage") -> None:
    expect(account_created_page.account_created_heading).to_be_visible()
    expect(account_created_page.account_created_heading).to_have_text("Account Created!")


def assert_account_deleted(account_deleted_page: "AccountDeletedPage") -> None:
    expect(account_deleted_page.account_deleted_heading).to_be_visible()
    expect(account_deleted_page.account_deleted_heading).to_have_text("Account Deleted!")


# --- Products ------------------------------------------------------------


def assert_all_products_page_visible(products_page: "ProductsPage") -> None:
    expect(products_page.page).to_have_url(re.compile(r"/products$"))
    expect(products_page.all_products_heading).to_be_visible()


def assert_searched_products_visible(products_page: "ProductsPage", search_term: str | None = None) -> None:
    """Waits for the 'Searched Products' heading to appear.

    The live site's search endpoint is noticeably slower than regular
    navigation and, under sustained load, can occasionally drop the request
    entirely rather than just being slow. If the heading never shows up and
    the original search term is known, retry the search once before failing
    for good.
    """
    try:
        expect(products_page.searched_products_heading).to_be_visible(timeout=15000)
    except AssertionError:
        if search_term is None:
            raise
        products_page.search_product(search_term)
        expect(products_page.searched_products_heading).to_be_visible(timeout=15000)


def assert_search_results_visible(products_page: "ProductsPage") -> None:
    """Verify at least one product is displayed for the search.

    The site's search matches on name, category and brand, so individual
    product names aren't guaranteed to contain the search term.
    """
    expect(products_page.products_list.first).to_be_visible()
    assert products_page.products_list.count() > 0, "Expected at least one searched product"


def assert_category_visible(products_page: "ProductsPage") -> None:
    expect(products_page.category_heading).to_be_visible()


def assert_brands_visible(products_page: "ProductsPage") -> None:
    expect(products_page.brands_heading).to_be_visible()


def assert_brand_link_visible(products_page: "ProductsPage", brand: str) -> None:
    expect(products_page.brand_link(brand)).to_be_visible()


def assert_category_products_title(products_page: "ProductsPage", expected_title: str) -> None:
    expect(products_page.products_title).to_have_text(expected_title)


def assert_brand_products_title(products_page: "ProductsPage", expected_title: str) -> None:
    expect(products_page.products_title).to_have_text(expected_title)


def assert_product_detail_visible(product_detail_page: "ProductDetailPage") -> None:
    expect(product_detail_page.page).to_have_url(re.compile(r"/product_details/\d+"))
    expect(product_detail_page.product_name).to_be_visible()
    expect(product_detail_page.product_category).to_be_visible()
    expect(product_detail_page.product_price).to_be_visible()
    expect(product_detail_page.product_availability).to_be_visible()
    expect(product_detail_page.product_condition).to_be_visible()
    expect(product_detail_page.product_brand).to_be_visible()


def assert_write_review_link_visible(product_detail_page: "ProductDetailPage") -> None:
    expect(product_detail_page.write_review_link).to_be_visible()


def assert_review_success_visible(product_detail_page: "ProductDetailPage") -> None:
    expect(product_detail_page.review_success_message).to_be_visible()
    expect(product_detail_page.review_success_message).to_contain_text("Thank you for your review.")


# --- Cart ------------------------------------------------------------


def assert_cart_page_visible(cart_page: "CartPage") -> None:
    expect(cart_page.page).to_have_url(re.compile(r"/view_cart"))


def assert_product_in_cart(cart_page: "CartPage", product_name: str) -> None:
    expect(cart_page.product_row(product_name)).to_be_visible()


def assert_product_not_in_cart(cart_page: "CartPage", product_name: str) -> None:
    expect(cart_page.product_row(product_name)).to_have_count(0)


def assert_product_quantity_in_cart(cart_page: "CartPage", product_name: str, expected_quantity: str) -> None:
    expect(cart_page.product_quantity(product_name)).to_have_text(expected_quantity)


# --- Checkout ------------------------------------------------------------


def assert_checkout_page_visible(checkout_page: "CheckoutPage") -> None:
    expect(checkout_page.page).to_have_url(re.compile(r"/checkout$"))
    expect(checkout_page.address_details_heading).to_be_visible()
    expect(checkout_page.review_order_heading).to_be_visible()


def assert_address_matches_user(checkout_page: "CheckoutPage", user: dict) -> None:
    """Asserts both the delivery and billing address blocks contain the
    same address fields that were filled into `unique_user_data()` at
    registration time.
    """
    fields = (
        "first_name",
        "last_name",
        "address1",
        "address2",
        "city",
        "state",
        "zipcode",
        "country",
        "mobile_number",
    )
    for label, address_locator in (
        ("delivery", checkout_page.delivery_address),
        ("billing", checkout_page.billing_address),
    ):
        expect(address_locator).to_be_visible()
        text = address_locator.inner_text()
        for field in fields:
            assert user[field] in text, (
                f"Expected {label} address to contain {user[field]!r} ({field}), got: {text!r}"
            )


# --- Payment ------------------------------------------------------------


def assert_order_placed_success(payment_page: "PaymentPage") -> None:
    expect(payment_page.order_placed_heading).to_be_visible(timeout=15000)
    expect(payment_page.order_placed_heading).to_contain_text("Order Placed!")
    expect(payment_page.order_placed_message).to_contain_text("Congratulations! Your order has been confirmed!")


# --- Contact Us ------------------------------------------------------------


def assert_get_in_touch_visible(contact_us_page: "ContactUsPage") -> None:
    expect(contact_us_page.get_in_touch_heading).to_be_visible()


def assert_contact_us_success_visible(contact_us_page: "ContactUsPage") -> None:
    expect(contact_us_page.success_message).to_be_visible(timeout=15000)
    expect(contact_us_page.success_message).to_contain_text(
        "Success! Your details have been submitted successfully."
    )

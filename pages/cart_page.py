from __future__ import annotations

import re
from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.checkout_page import CheckoutPage
    from pages.signup_login_page import SignupLoginPage


class CartPage(BasePage):
    """Cart page object.

    Cart rows use the live id pattern `#product-<id>` per row, with
    `.cart_description`, `.cart_price`, `.cart_quantity`, `.cart_total`
    columns and a `.cart_quantity_delete` remove link per row (verified
    against the live `#cart_info_table` markup).
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_rows = page.locator("#cart_info_table tbody tr")
        self.subscribe_heading = page.locator(".single-widget h2", has_text="Subscription")
        self.subscribe_email_input = page.locator("#susbscribe_email")
        self.subscribe_button = page.locator("#subscribe")
        self.subscribe_success_message = page.locator("#success-subscribe")
        self.proceed_to_checkout_button = page.locator("a.check_out", has_text="Proceed To Checkout")
        # Shown instead of navigating when the cart is not empty but the user
        # isn't logged in yet (verified live: an in-page modal, not a real
        # page transition — the URL stays at /view_cart).
        self.checkout_modal_register_login_link = page.locator("#checkoutModal a[href='/login']")

    def goto(self):
        self.page.goto(f"{self.URL}/view_cart")

    def verify_cart_page_visible(self):
        expect(self.page).to_have_url(re.compile(r"/view_cart"))

    def _row_by_product_name(self, product_name: str):
        return self.cart_rows.filter(has=self.page.locator(".cart_description", has_text=product_name))

    def verify_product_in_cart(self, product_name: str):
        row = self.page.locator("#cart_info_table .cart_description", has_text=product_name)
        expect(row).to_be_visible()

    def get_product_price(self, product_name: str) -> str:
        row = self._row_by_product_name(product_name)
        return row.locator(".cart_price p").inner_text()

    def get_product_total(self, product_name: str) -> str:
        row = self._row_by_product_name(product_name)
        return row.locator(".cart_total .cart_total_price").inner_text()

    def verify_product_quantity(self, product_name: str, expected_quantity: str):
        row = self._row_by_product_name(product_name)
        expect(row.locator(".cart_quantity button")).to_have_text(expected_quantity)

    def remove_product(self, product_name: str):
        row = self._row_by_product_name(product_name)
        row.locator(".cart_quantity_delete").click()
        expect(row).not_to_be_visible()

    def verify_product_not_in_cart(self, product_name: str):
        row = self.page.locator("#cart_info_table .cart_description", has_text=product_name)
        expect(row).to_have_count(0)

    def click_proceed_to_checkout(self) -> "CheckoutPage":
        """Clicks 'Proceed To Checkout'.

        When logged in this is a real navigation to /checkout. When not
        logged in, the site instead shows an in-page 'Register / Login
        account to proceed on checkout.' modal and stays on /view_cart — use
        `click_register_login_from_checkout_modal` in that case instead of
        the returned CheckoutPage.

        The click occasionally lands without triggering the navigation (same
        live-site flakiness as the products sidebar accordion), so retry
        once before giving up if neither the /checkout navigation nor the
        modal shows up.
        """
        self.proceed_to_checkout_button.click()
        checkout_url = re.compile(r"/checkout$")
        modal = self.checkout_modal_register_login_link
        try:
            expect(self.page).to_have_url(checkout_url, timeout=5000)
        except AssertionError:
            try:
                expect(modal).to_be_visible(timeout=1000)
            except AssertionError:
                self.proceed_to_checkout_button.click()
                try:
                    expect(self.page).to_have_url(checkout_url, timeout=5000)
                except AssertionError:
                    expect(modal).to_be_visible(timeout=5000)

        from pages.checkout_page import CheckoutPage

        return CheckoutPage(self.page)

    def click_register_login_from_checkout_modal(self) -> "SignupLoginPage":
        self.checkout_modal_register_login_link.click()

        from pages.signup_login_page import SignupLoginPage

        return SignupLoginPage(self.page)

    def scroll_to_subscription(self):
        self.subscribe_heading.scroll_into_view_if_needed()

    def verify_subscription_heading_visible(self):
        expect(self.subscribe_heading).to_be_visible()
        expect(self.subscribe_heading).to_have_text("Subscription")

    def subscribe(self, email: str):
        self.subscribe_email_input.fill(email)
        self.subscribe_button.click()

    def verify_subscription_success(self):
        expect(self.subscribe_success_message).to_be_visible()
        expect(self.subscribe_success_message).to_contain_text("You have been successfully subscribed!")

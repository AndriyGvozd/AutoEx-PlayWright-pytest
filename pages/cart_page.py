from __future__ import annotations

import re
from typing import TYPE_CHECKING

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages import registry
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

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
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
        self.page.goto(f"{self.base_url}/view_cart")

    def product_row(self, product_name: str):
        """Locator for the cart row matching `product_name` (empty/no-match if absent)."""
        return self.cart_rows.filter(has=self.page.locator(".cart_description", has_text=product_name))

    def product_quantity(self, product_name: str):
        return self.product_row(product_name).locator(".cart_quantity button")

    def get_product_price(self, product_name: str) -> str:
        return self.product_row(product_name).locator(".cart_price p").inner_text()

    def get_product_total(self, product_name: str) -> str:
        return self.product_row(product_name).locator(".cart_total .cart_total_price").inner_text()

    def remove_product(self, product_name: str):
        row = self.product_row(product_name)
        row.locator(".cart_quantity_delete").click()
        try:
            row.wait_for(state="hidden", timeout=5000)
        except PlaywrightTimeoutError:
            pass  # the caller's own assertion will surface the failure with a clear message

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
        modal shows up. These are synchronization waits (Page.wait_for_url /
        Locator.wait_for), not test assertions.
        """
        self.proceed_to_checkout_button.click()
        checkout_url = re.compile(r"/checkout$")
        modal = self.checkout_modal_register_login_link
        try:
            self.page.wait_for_url(checkout_url, timeout=5000)
        except PlaywrightTimeoutError:
            try:
                modal.wait_for(state="visible", timeout=1000)
            except PlaywrightTimeoutError:
                self.proceed_to_checkout_button.click()
                try:
                    self.page.wait_for_url(checkout_url, timeout=5000)
                except PlaywrightTimeoutError:
                    modal.wait_for(state="visible", timeout=5000)

        return registry.checkout_page(self.page, self.base_url)

    def click_register_login_from_checkout_modal(self) -> "SignupLoginPage":
        self.checkout_modal_register_login_link.click()
        return registry.signup_login_page(self.page, self.base_url)

    def scroll_to_subscription(self):
        self.subscribe_heading.scroll_into_view_if_needed()

    def subscribe(self, email: str):
        self.subscribe_email_input.fill(email)
        self.subscribe_button.click()

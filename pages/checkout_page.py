from __future__ import annotations

import re
from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.payment_page import PaymentPage


class CheckoutPage(BasePage):
    """Checkout page object (/checkout).

    Verified live: reachable only while logged in with a non-empty cart —
    otherwise Cart's 'Proceed To Checkout' shows a modal instead (see
    CartPage.click_register_login_from_checkout_modal). Renders an "Address
    Details" block with `#address_delivery` / `#address_invoice` lists (each
    populated straight from the account's registered address), followed by a
    "Review Your Order" cart table, a comment textarea, and a 'Place Order'
    link that navigates to /payment.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.address_details_heading = page.locator("h2.heading", has_text="Address Details")
        self.review_order_heading = page.locator("h2.heading", has_text="Review Your Order")
        self.delivery_address = page.locator("#address_delivery")
        self.billing_address = page.locator("#address_invoice")
        self.comment_textarea = page.locator("textarea[name='message']")
        self.place_order_button = page.locator("a.check_out", has_text="Place Order")

    def verify_checkout_page_visible(self):
        expect(self.page).to_have_url(re.compile(r"/checkout$"))
        expect(self.address_details_heading).to_be_visible()
        expect(self.review_order_heading).to_be_visible()

    def verify_address_matches_user(self, user: dict):
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
            ("delivery", self.delivery_address),
            ("billing", self.billing_address),
        ):
            expect(address_locator).to_be_visible()
            text = address_locator.inner_text()
            for field in fields:
                assert user[field] in text, (
                    f"Expected {label} address to contain {user[field]!r} "
                    f"({field}), got: {text!r}"
                )

    def enter_comment(self, comment: str):
        self.comment_textarea.fill(comment)

    def click_place_order(self) -> "PaymentPage":
        self.place_order_button.click()

        from pages.payment_page import PaymentPage

        return PaymentPage(self.page)

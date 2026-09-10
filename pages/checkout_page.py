from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page

from pages import registry
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

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.address_details_heading = page.locator("h2.heading", has_text="Address Details")
        self.review_order_heading = page.locator("h2.heading", has_text="Review Your Order")
        self.delivery_address = page.locator("#address_delivery")
        self.billing_address = page.locator("#address_invoice")
        self.comment_textarea = page.locator("textarea[name='message']")
        self.place_order_button = page.locator("a.check_out", has_text="Place Order")

    def enter_comment(self, comment: str):
        self.comment_textarea.fill(comment)

    def click_place_order(self) -> "PaymentPage":
        self.place_order_button.click()
        return registry.payment_page(self.page, self.base_url)

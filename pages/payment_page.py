from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from playwright.sync_api import Page

from pages import registry
from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.account_deleted_page import AccountDeletedPage
    from pages.home_page import HomePage


class PaymentPage(BasePage):
    """Payment + order-confirmation page object.

    Covers both /payment (the card form) and the /payment_done/<order_id>
    confirmation it redirects to on submit, since the flow is one continuous
    step from the test's perspective.

    Quirk verified live: the card form does carry a `#success_message` node
    with the text "Your order has been placed successfully!", but it's only
    unhidden by an inline `onsubmit` handler a split second before the
    browser navigates away to /payment_done/<order_id> — by the time
    Playwright could assert on it the page has usually already navigated, so
    it isn't a reliable signal. The confirmation page itself instead shows a
    'Order Placed!' heading (`[data-qa='order-placed']`) with the text
    "Congratulations! Your order has been confirmed!" — that's the reliable
    equivalent of the official test text's success message (see
    `utils/verifications.py::assert_order_placed_success`).
    """

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.name_on_card_input = page.locator("[data-qa='name-on-card']")
        self.card_number_input = page.locator("[data-qa='card-number']")
        self.cvc_input = page.locator("[data-qa='cvc']")
        self.expiry_month_input = page.locator("[data-qa='expiry-month']")
        self.expiry_year_input = page.locator("[data-qa='expiry-year']")
        self.pay_button = page.locator("[data-qa='pay-button']")

        self.order_placed_heading = page.locator("[data-qa='order-placed']")
        self.order_placed_message = page.locator("#form p")
        self.download_invoice_link = page.locator("a[href^='/download_invoice/']")
        self.continue_button = page.locator("[data-qa='continue-button']")
        self.delete_account_link = page.locator("a[href='/delete_account']")

    def pay(self, name_on_card: str, card_number: str, cvc: str, expiry_month: str, expiry_year: str):
        """Fills the card form and clicks 'Pay and Confirm Order'.

        Single call mirroring SignupPage.complete_registration, so the
        field-filling sequence has one source of truth across tests.
        """
        self.name_on_card_input.fill(name_on_card)
        self.card_number_input.fill(card_number)
        self.cvc_input.fill(cvc)
        self.expiry_month_input.fill(expiry_month)
        self.expiry_year_input.fill(expiry_year)
        self.pay_button.click()

    def download_invoice(self, destination: Path) -> Path:
        """Clicks 'Download Invoice' and saves the resulting download to
        `destination`, returning it. Caller should assert the file exists
        with nonzero size.
        """
        with self.page.expect_download() as download_info:
            self.download_invoice_link.click()
        download = download_info.value
        download.save_as(str(destination))
        return destination

    def click_continue(self) -> "HomePage":
        self.continue_button.click()
        return registry.home_page(self.page, self.base_url)

    def click_delete_account(self) -> "AccountDeletedPage":
        self.delete_account_link.click()
        return registry.account_deleted_page(self.page, self.base_url)

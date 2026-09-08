from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.home_page import HomePage


class AccountCreatedPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.account_created_heading = page.locator("[data-qa='account-created']")
        self.continue_button = page.locator("[data-qa='continue-button']")

    def verify_account_created(self):
        expect(self.account_created_heading).to_be_visible()
        expect(self.account_created_heading).to_have_text("Account Created!")

    def click_continue(self) -> "HomePage":
        self.continue_button.click()

        from pages.home_page import HomePage

        return HomePage(self.page)

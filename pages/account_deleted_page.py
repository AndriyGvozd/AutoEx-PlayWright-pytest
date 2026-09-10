from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page

from pages import registry
from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.home_page import HomePage


class AccountDeletedPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.account_deleted_heading = page.locator("[data-qa='account-deleted']")
        self.continue_button = page.locator("[data-qa='continue-button']")

    def click_continue(self) -> "HomePage":
        self.continue_button.click()
        return registry.home_page(self.page, self.base_url)

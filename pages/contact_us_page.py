from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages import registry
from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.home_page import HomePage


class ContactUsPage(BasePage):
    """Contact Us page object.

    Form fields verified against the live DOM: `data-qa` attributes on
    name/email/subject/message, `input[name='upload_file']` for the file
    input, and `input[data-qa='submit-button']` for Submit. Submitting the
    form triggers a native `window.confirm()` dialog, so the caller must
    register a `page.once("dialog", ...)` handler right before calling
    `submit()`.
    """

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.get_in_touch_heading = page.locator("h2", has_text="Get In Touch")
        self.name_input = page.locator("input[data-qa='name']")
        self.email_input = page.locator("input[data-qa='email']")
        self.subject_input = page.locator("input[data-qa='subject']")
        self.message_input = page.locator("textarea[data-qa='message']")
        self.upload_file_input = page.locator("input[name='upload_file']")
        self.submit_button = page.locator("input[data-qa='submit-button']")
        self.success_message = page.locator(".status.alert-success:visible")
        # There are two 'Home' links on this page (the header logo and the
        # nav's 'Home' item); scope to the one with the house icon, which is
        # the actual nav button referred to by this step.
        self.home_button = page.locator("a[href='/']:has(i.fa-home)")

    def goto(self):
        self.page.goto(f"{self.base_url}/contact_us")

    def fill_contact_form(self, name: str, email: str, subject: str, message: str):
        # The page's own submit-handling JS can still be wiring itself up
        # right after navigation; without waiting for the network to go
        # quiet first, a fast fill+submit can race it and the click
        # silently does nothing (no request is ever sent).
        self.page.wait_for_load_state("networkidle")
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.subject_input.fill(subject)
        self.message_input.fill(message)

    def upload_file(self, file_path: str):
        self.upload_file_input.set_input_files(file_path)

    def submit(self):
        # The native confirm() dialog must be handled BEFORE the click that
        # triggers it, not after.
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.submit_button.click()

        # The submit occasionally races with the page's ad/analytics scripts
        # and the AJAX response is a touch slow to land, so wait generously
        # for the success message and retry the submit once if it never
        # shows up. A synchronization wait (Locator.wait_for), not a test
        # assertion -- the caller makes the actual content assertion.
        try:
            self.success_message.wait_for(state="visible", timeout=15000)
        except PlaywrightTimeoutError:
            self.page.once("dialog", lambda dialog: dialog.accept())
            self.submit_button.click()
            self.success_message.wait_for(state="visible", timeout=15000)

    def click_home(self) -> "HomePage":
        self.home_button.click()
        return registry.home_page(self.page, self.base_url)

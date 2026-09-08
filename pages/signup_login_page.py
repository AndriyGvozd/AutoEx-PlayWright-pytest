from __future__ import annotations

import re
from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.home_page import HomePage
    from pages.signup_page import SignupPage


class SignupLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.new_user_signup_heading = page.locator("h2", has_text="New User Signup!")
        self.signup_name_input = page.locator("[data-qa='signup-name']")
        self.signup_email_input = page.locator("[data-qa='signup-email']")
        self.signup_button = page.locator("[data-qa='signup-button']")
        self.signup_error_message = page.locator(".signup-form p", has_text="Email Address already exist!")

        self.login_to_account_heading = page.locator("h2", has_text="Login to your account")
        self.login_email_input = page.locator("[data-qa='login-email']")
        self.login_password_input = page.locator("[data-qa='login-password']")
        self.login_button = page.locator("[data-qa='login-button']")
        self.login_error_message = page.locator(".login-form p", has_text="Your email or password is incorrect!")

    def verify_new_user_signup_visible(self):
        expect(self.new_user_signup_heading).to_be_visible()

    def signup(self, name: str, email: str) -> "SignupPage":
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()

        from pages.signup_page import SignupPage

        return SignupPage(self.page)

    def verify_login_to_account_visible(self):
        expect(self.page).to_have_url(re.compile(r"/login$"))
        expect(self.login_to_account_heading).to_be_visible()

    def login(self, email: str, password: str) -> "HomePage":
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_button.click()

        from pages.home_page import HomePage

        return HomePage(self.page)

    def verify_login_error_visible(self):
        expect(self.login_error_message).to_be_visible()

    def verify_signup_error_visible(self):
        expect(self.signup_error_message).to_be_visible()

from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page

from pages import registry
from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.home_page import HomePage
    from pages.signup_page import SignupPage


class SignupLoginPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
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

    def signup(self, name: str, email: str) -> "SignupPage":
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()
        return registry.signup_page(self.page, self.base_url)

    def login(self, email: str, password: str) -> "HomePage":
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_button.click()
        return registry.home_page(self.page, self.base_url)

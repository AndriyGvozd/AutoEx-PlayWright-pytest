from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.account_created_page import AccountCreatedPage


class SignupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.account_info_heading = page.locator("h2", has_text="Enter Account Information")

        self.title_mr_radio = page.locator("#id_gender1")
        self.title_mrs_radio = page.locator("#id_gender2")
        self.password_input = page.locator("#password")
        self.days_select = page.locator("#days")
        self.months_select = page.locator("#months")
        self.years_select = page.locator("#years")

        self.newsletter_checkbox = page.locator("#newsletter")
        self.optin_checkbox = page.locator("#optin")

        self.first_name_input = page.locator("#first_name")
        self.last_name_input = page.locator("#last_name")
        self.company_input = page.locator("#company")
        self.address1_input = page.locator("#address1")
        self.address2_input = page.locator("#address2")
        self.country_select = page.locator("#country")
        self.state_input = page.locator("#state")
        self.city_input = page.locator("#city")
        self.zipcode_input = page.locator("#zipcode")
        self.mobile_number_input = page.locator("#mobile_number")

        self.create_account_button = page.locator("[data-qa='create-account']")

    def verify_account_info_visible(self):
        expect(self.account_info_heading).to_be_visible()

    def fill_account_info(self, title: str, password: str, day: str, month: str, year: str):
        if title.lower() == "mr":
            self.title_mr_radio.check()
        else:
            self.title_mrs_radio.check()
        self.password_input.fill(password)
        self.days_select.select_option(day)
        self.months_select.select_option(month)
        self.years_select.select_option(year)

    def check_newsletter(self):
        self.newsletter_checkbox.check()

    def check_special_offers(self):
        self.optin_checkbox.check()

    def fill_address_info(
        self,
        first_name: str,
        last_name: str,
        company: str,
        address1: str,
        address2: str,
        country: str,
        state: str,
        city: str,
        zipcode: str,
        mobile_number: str,
    ):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.company_input.fill(company)
        self.address1_input.fill(address1)
        self.address2_input.fill(address2)
        self.country_select.select_option(country)
        self.state_input.fill(state)
        self.city_input.fill(city)
        self.zipcode_input.fill(zipcode)
        self.mobile_number_input.fill(mobile_number)

    def click_create_account(self) -> "AccountCreatedPage":
        self.create_account_button.click()

        from pages.account_created_page import AccountCreatedPage

        return AccountCreatedPage(self.page)

    def complete_registration(self, user: dict) -> "AccountCreatedPage":
        """Fills the whole 'Enter Account Information' form from a user data dict
        and submits it. Single source of truth for the field-filling sequence so
        it isn't repeated across tests/fixtures.
        """
        self.fill_account_info(
            title=user["title"],
            password=user["password"],
            day=user["day"],
            month=user["month"],
            year=user["year"],
        )
        self.check_newsletter()
        self.check_special_offers()
        self.fill_address_info(
            first_name=user["first_name"],
            last_name=user["last_name"],
            company=user["company"],
            address1=user["address1"],
            address2=user["address2"],
            country=user["country"],
            state=user["state"],
            city=user["city"],
            zipcode=user["zipcode"],
            mobile_number=user["mobile_number"],
        )
        return self.click_create_account()

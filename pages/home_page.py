from __future__ import annotations

import re
from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.signup_login_page import SignupLoginPage

if TYPE_CHECKING:
    from pages.account_deleted_page import AccountDeletedPage
    from pages.cart_page import CartPage
    from pages.contact_us_page import ContactUsPage
    from pages.products_page import ProductsPage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.signup_login_link = page.locator("#header a[href='/login']")
        self.logo = page.locator(".logo")
        self.logged_in_as_text = page.locator(".shop-menu", has_text="Logged in as")
        self.delete_account_link = page.locator("a[href='/delete_account']")
        self.logout_link = page.locator("a[href='/logout']")
        self.products_link = page.locator("#header a[href='/products']")
        self.test_cases_link = page.locator("#header a[href='/test_cases']")
        self.cart_link = page.locator("#header a[href='/view_cart']")
        self.contact_us_link = page.locator("#header a[href='/contact_us']")
        self.recommended_heading = page.locator("h2.title", has_text="recommended items")
        # The carousel (owl-carousel) clones slides for its infinite-loop effect, so the
        # DOM holds far more `.product-image-wrapper` nodes than are actually on screen.
        # Scope to :visible so `.first`/`.nth()` always resolve to a currently-shown slide.
        self.recommended_items = page.locator("#recommended-item-carousel .product-image-wrapper:visible")
        # Footer subscription form: same markup/ids as CartPage's (verified live).
        self.subscribe_heading = page.locator(".single-widget h2", has_text="Subscription")
        self.subscribe_email_input = page.locator("#susbscribe_email")
        self.subscribe_button = page.locator("#subscribe")
        self.subscribe_success_message = page.locator("#success-subscribe")
        # jQuery "scroll to top" arrow, fixed-position, shown once the page is scrolled down.
        self.scroll_up_arrow = page.locator("#scrollUp")
        # The top slider carousel keeps every slide's markup in the DOM and
        # only shows the active one (auto-rotating), so scope to :visible to
        # always resolve to whichever slide is currently on screen.
        self.hero_text = page.locator(
            ".carousel-inner h2:visible", has_text="Full-Fledged practice website for Automation Engineers"
        )

    def verify_home_page_visible(self):
        expect(self.page).to_have_url(re.compile(r"automationexercise\.com"))
        expect(self.logo).to_be_visible()

    def click_signup_login(self) -> SignupLoginPage:
        self.signup_login_link.click()
        return SignupLoginPage(self.page)

    def verify_logged_in_as(self, username: str):
        expect(self.logged_in_as_text).to_be_visible()
        expect(self.logged_in_as_text).to_contain_text(f"Logged in as {username}")

    def click_delete_account(self) -> "AccountDeletedPage":
        self.delete_account_link.click()

        from pages.account_deleted_page import AccountDeletedPage

        return AccountDeletedPage(self.page)

    def click_logout(self) -> SignupLoginPage:
        self.logout_link.click()
        return SignupLoginPage(self.page)

    def click_products(self) -> "ProductsPage":
        self.products_link.click()

        from pages.products_page import ProductsPage

        return ProductsPage(self.page)

    def click_test_cases(self):
        self.test_cases_link.click()
        expect(self.page).to_have_url(re.compile(r"/test_cases$"))

    def click_cart(self) -> "CartPage":
        self.cart_link.click()

        from pages.cart_page import CartPage

        return CartPage(self.page)

    def scroll_to_footer(self):
        self.page.locator("#footer").scroll_into_view_if_needed()

    def scroll_to_bottom(self):
        self.page.keyboard.press("End")

    def verify_recommended_items_visible(self):
        expect(self.recommended_heading).to_be_visible()
        expect(self.recommended_items.first).to_be_visible()

    def add_recommended_product_to_cart(self, index: int = 0):
        self.recommended_items.nth(index).locator("a.add-to-cart").click()

    def click_contact_us(self) -> "ContactUsPage":
        self.contact_us_link.click()

        from pages.contact_us_page import ContactUsPage

        return ContactUsPage(self.page)

    def scroll_to_subscription(self):
        self.subscribe_heading.scroll_into_view_if_needed()

    def verify_subscription_heading_visible(self):
        expect(self.subscribe_heading).to_be_visible()
        expect(self.subscribe_heading).to_have_text("Subscription")

    def subscribe(self, email: str):
        self.subscribe_email_input.fill(email)
        self.subscribe_button.click()

    def verify_subscription_success(self):
        expect(self.subscribe_success_message).to_be_visible()
        expect(self.subscribe_success_message).to_contain_text("You have been successfully subscribed!")

    def verify_scrolled_to_bottom_with_subscription(self):
        """Scrolls to the bottom of the page and verifies the subscription
        section is visible. Shared by the arrow/no-arrow scroll-up tests so
        they differ only in how they scroll back up, not in this setup."""
        self.scroll_to_bottom()
        self.verify_subscription_heading_visible()

    def click_scroll_up_arrow(self):
        expect(self.scroll_up_arrow).to_be_visible(timeout=10000)
        self.scroll_up_arrow.click()

    def scroll_to_top_without_arrow(self):
        self.page.evaluate("window.scrollTo(0, 0)")

    def verify_scrolled_to_top(self):
        """Verifies the page is back at the top by checking the hero text
        (in the top slider) is visible on screen."""
        expect(self.hero_text.first).to_be_visible(timeout=15000)

    def click_view_cart_from_modal(self) -> "CartPage":
        # The 'Add to cart' confirmation is a Bootstrap modal that fades in; wait
        # for it to actually be visible before clicking, to avoid racing the animation.
        modal_link = self.page.locator(".modal-content a[href='/view_cart']")
        expect(modal_link).to_be_visible(timeout=10000)
        modal_link.click()

        from pages.cart_page import CartPage

        return CartPage(self.page)

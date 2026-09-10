from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages import registry
from pages.base_page import BasePage
from pages.signup_login_page import SignupLoginPage

if TYPE_CHECKING:
    from pages.account_deleted_page import AccountDeletedPage
    from pages.cart_page import CartPage
    from pages.contact_us_page import ContactUsPage
    from pages.products_page import ProductsPage


class HomePage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
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
        self.view_cart_modal_link = page.locator(".modal-content a[href='/view_cart']")

    def click_signup_login(self) -> SignupLoginPage:
        self.signup_login_link.click()
        return registry.signup_login_page(self.page, self.base_url)

    def click_delete_account(self) -> "AccountDeletedPage":
        self.delete_account_link.click()
        return registry.account_deleted_page(self.page, self.base_url)

    def click_logout(self) -> SignupLoginPage:
        self.logout_link.click()
        return registry.signup_login_page(self.page, self.base_url)

    def click_products(self) -> "ProductsPage":
        self.products_link.click()
        return registry.products_page(self.page, self.base_url)

    def click_test_cases(self):
        self.test_cases_link.click()

    def click_cart(self) -> "CartPage":
        self.cart_link.click()
        return registry.cart_page(self.page, self.base_url)

    def scroll_to_footer(self):
        self.page.locator("#footer").scroll_into_view_if_needed()

    def scroll_to_bottom(self):
        self.page.keyboard.press("End")

    def get_recommended_product_name(self, index: int = 0) -> str:
        return self.recommended_items.nth(index).locator("p").inner_text()

    def add_recommended_product_to_cart(self, index: int = 0):
        self.recommended_items.nth(index).locator("a.add-to-cart").click()

    def click_contact_us(self) -> "ContactUsPage":
        self.contact_us_link.click()
        return registry.contact_us_page(self.page, self.base_url)

    def scroll_to_subscription(self):
        self.subscribe_heading.scroll_into_view_if_needed()

    def subscribe(self, email: str):
        self.subscribe_email_input.fill(email)
        self.subscribe_button.click()

    def click_scroll_up_arrow(self):
        # The arrow is only shown/interactive once the page has scrolled far
        # enough down for it to fade in; wait for that rather than assert it,
        # since this is UI-settling synchronization, not a test verification.
        self.scroll_up_arrow.wait_for(state="visible", timeout=10000)
        self.scroll_up_arrow.click()

    def scroll_to_top_without_arrow(self):
        self.page.evaluate("window.scrollTo(0, 0)")

    def click_view_cart_from_modal(self) -> "CartPage":
        # The 'Add to cart' confirmation is a Bootstrap modal that fades in;
        # wait for it to actually be visible before clicking, to avoid racing
        # the animation. This is a synchronization wait, not a test
        # assertion, so it uses Locator.wait_for rather than expect().
        try:
            self.view_cart_modal_link.wait_for(state="visible", timeout=10000)
        except PlaywrightTimeoutError:
            pass  # let the click below raise its own clear timeout error
        self.view_cart_modal_link.click()
        return registry.cart_page(self.page, self.base_url)

from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages import registry
from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.cart_page import CartPage


class ProductDetailPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.product_name = page.locator(".product-information h2")
        self.product_category = page.locator(".product-information p", has_text="Category:")
        self.product_price = page.locator(".product-information span span")
        self.product_availability = page.locator(".product-information p", has_text="Availability:")
        self.product_condition = page.locator(".product-information p", has_text="Condition:")
        self.product_brand = page.locator(".product-information p", has_text="Brand:")
        self.quantity_input = page.locator("#quantity")
        self.add_to_cart_button = page.locator(".product-information button.cart")
        self.write_review_link = page.locator("a", has_text="Write Your Review")

        self.review_name_input = page.locator("#name")
        self.review_email_input = page.locator("#email")
        self.review_text_input = page.locator("#review")
        self.review_submit_button = page.locator("#button-review")
        self.review_success_message = page.locator("#review-section .alert-success")

        self.view_cart_link = page.locator(".modal-content a[href='/view_cart']")

    def set_quantity(self, quantity: int):
        self.quantity_input.fill(str(quantity))

    def add_to_cart(self):
        self.add_to_cart_button.click()

    def click_view_cart(self) -> "CartPage":
        # The 'Add to cart' confirmation is a Bootstrap modal that fades in; wait
        # for the link inside it to actually be visible before clicking. Under
        # live-site load the AJAX add-to-cart call itself can occasionally be
        # dropped so the modal never opens at all, not just a slow fade-in -
        # if it's still hidden after the wait, retry the add-to-cart click once.
        # These are synchronization waits (Locator.wait_for), not test assertions.
        try:
            self.view_cart_link.wait_for(state="visible", timeout=10000)
        except PlaywrightTimeoutError:
            self.add_to_cart()
            self.view_cart_link.wait_for(state="visible", timeout=10000)
        self.view_cart_link.click()
        return registry.cart_page(self.page, self.base_url)

    def write_review(self, name: str, email: str, review: str):
        self.review_name_input.fill(name)
        self.review_email_input.fill(email)
        self.review_text_input.fill(review)
        self.review_submit_button.click()

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.cart_page import CartPage
    from pages.product_detail_page import ProductDetailPage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.all_products_heading = page.locator("h2.title", has_text="All Products")
        self.products_list = page.locator(".product-image-wrapper")
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.searched_products_heading = page.locator("h2.title", has_text="Searched Products")
        self.view_cart_modal_link = page.locator(".modal-content a[href='/view_cart']")

    def goto(self):
        self.page.goto(f"{self.URL}/products")

    def verify_all_products_page_visible(self):
        expect(self.page).to_have_url(re.compile(r"/products$"))
        expect(self.all_products_heading).to_be_visible()

    def click_view_product(self, index: int = 0) -> "ProductDetailPage":
        self.products_list.nth(index).locator(".choose a", has_text="View Product").click()

        from pages.product_detail_page import ProductDetailPage

        return ProductDetailPage(self.page)

    def search_product(self, product_name: str) -> "ProductsPage":
        self.search_input.fill(product_name)
        self.search_button.click()
        return self

    def verify_searched_products_visible(self, product_name: str | None = None):
        """Waits for the 'Searched Products' heading to appear.

        The live site's search endpoint is noticeably slower than regular
        navigation and, under sustained load (e.g. a full test-suite run),
        can occasionally drop the request entirely rather than just being
        slow. A generous timeout alone doesn't cover that case, so if the
        heading never shows up and the original search term is known, retry
        the search once before failing for good.
        """
        try:
            expect(self.searched_products_heading).to_be_visible(timeout=15000)
        except AssertionError:
            if product_name is None:
                raise
            self.search_product(product_name)
            expect(self.searched_products_heading).to_be_visible(timeout=15000)

    def verify_search_results_visible(self):
        """Verify at least one product is displayed for the search.

        The site's search matches on name, category and brand, so individual
        product names aren't guaranteed to contain the search term.
        """
        expect(self.products_list.first).to_be_visible()
        assert self.products_list.count() > 0, "Expected at least one searched product"

    def click_category(self, category: str, subcategory: str) -> "ProductsPage":
        toggle = self.page.locator(f"a[href='#{category}']")
        panel = self.page.locator(f"#{category}")

        # The sidebar is a Bootstrap collapse accordion animated open on click. It's
        # occasionally missed under live-site load (the click lands before the JS
        # handler is ready), so retry the toggle click once before giving up.
        toggle.scroll_into_view_if_needed()
        toggle.click()
        try:
            expect(panel).to_have_class(re.compile(r"\bin\b"), timeout=5000)
        except AssertionError:
            toggle.click()
            expect(panel).to_have_class(re.compile(r"\bin\b"), timeout=5000)

        panel.locator("a", has_text=subcategory).click()
        return self

    def click_brand(self, brand: str) -> "ProductsPage":
        self.page.locator(f"a[href='/brand_products/{brand}']").click()
        return self

    def verify_category_products_title(self, expected_title: str):
        title = self.page.locator("h2.title")
        expect(title).to_have_text(expected_title)

    def verify_brand_products_title(self, expected_title: str):
        title = self.page.locator("h2.title")
        expect(title).to_have_text(expected_title)

    def add_product_to_cart_by_index(self, index: int = 0):
        product = self.products_list.nth(index)
        product.hover()
        product.locator(".product-overlay a.add-to-cart").click()

    def click_continue_shopping(self):
        self.page.locator("button", has_text="Continue Shopping").click()

    def click_view_cart_from_modal(self) -> "CartPage":
        # The 'Add to cart' confirmation is a Bootstrap modal that fades in; wait
        # for it to actually be visible before clicking, to avoid racing the animation.
        expect(self.view_cart_modal_link).to_be_visible(timeout=10000)
        self.view_cart_modal_link.click()

        from pages.cart_page import CartPage

        return CartPage(self.page)

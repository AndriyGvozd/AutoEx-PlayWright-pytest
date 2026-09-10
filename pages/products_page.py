from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages import registry
from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.cart_page import CartPage
    from pages.product_detail_page import ProductDetailPage


class ProductsPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.all_products_heading = page.locator("h2.title", has_text="All Products")
        self.products_list = page.locator(".product-image-wrapper")
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.searched_products_heading = page.locator("h2.title", has_text="Searched Products")
        self.view_cart_modal_link = page.locator(".modal-content a[href='/view_cart']")
        self.category_heading = page.locator("h2", has_text="Category")
        self.brands_heading = page.locator("h2", has_text="Brands")
        self.products_title = page.locator("h2.title")

    def goto(self):
        self.page.goto(f"{self.base_url}/products")

    def get_product_name(self, index: int = 0) -> str:
        return self.products_list.nth(index).locator(".productinfo p").inner_text()

    def get_product_price(self, index: int = 0) -> str:
        return self.products_list.nth(index).locator(".productinfo h2").inner_text()

    def click_view_product(self, index: int = 0) -> "ProductDetailPage":
        self.products_list.nth(index).locator(".choose a", has_text="View Product").click()
        return registry.product_detail_page(self.page, self.base_url)

    def search_product(self, product_name: str) -> "ProductsPage":
        self.search_input.fill(product_name)
        self.search_button.click()
        return self

    def brand_link(self, brand: str):
        return self.page.locator(f"a[href='/brand_products/{brand}']")

    def click_category(self, category: str, subcategory: str) -> "ProductsPage":
        toggle = self.page.locator(f"a[href='#{category}']")
        # The sidebar is a Bootstrap collapse accordion animated open on
        # click, so scope the panel locator to only match once its "in"
        # (open) class is actually applied -- a pure synchronization wait,
        # not a test assertion. It's occasionally missed under live-site
        # load (the click lands before the JS handler is ready), so retry
        # the toggle click once before giving up.
        open_panel = self.page.locator(f"#{category}.in")

        toggle.scroll_into_view_if_needed()
        toggle.click()
        try:
            open_panel.wait_for(state="visible", timeout=5000)
        except PlaywrightTimeoutError:
            toggle.click()
            open_panel.wait_for(state="visible", timeout=5000)

        open_panel.locator("a", has_text=subcategory).click()
        return self

    def click_brand(self, brand: str) -> "ProductsPage":
        self.brand_link(brand).click()
        return self

    def add_product_to_cart_by_index(self, index: int = 0):
        product = self.products_list.nth(index)
        product.hover()
        product.locator(".product-overlay a.add-to-cart").click()

    def click_continue_shopping(self):
        self.page.locator("button", has_text="Continue Shopping").click()

    def click_view_cart_from_modal(self) -> "CartPage":
        # The 'Add to cart' confirmation is a Bootstrap modal that fades in;
        # wait for it to actually be visible before clicking, to avoid
        # racing the animation. Synchronization wait, not a test assertion.
        try:
            self.view_cart_modal_link.wait_for(state="visible", timeout=10000)
        except PlaywrightTimeoutError:
            pass  # let the click below raise its own clear timeout error
        self.view_cart_modal_link.click()
        return registry.cart_page(self.page, self.base_url)

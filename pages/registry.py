"""Central, single point of lazy resolution for Page Object classes.

Every Page Object needs to construct *sibling* Page Objects -- e.g. to
return the next page after a click that navigates somewhere. Navigation on
this site goes in both directions between almost every pair of pages (Home
<-> Signup/Login <-> Signup <-> Account Created <-> Home, etc.), so having
each of the ~12 page modules `import` each other directly at module level
would create an unavoidable circular-import cycle.

Rather than scattering a local `from pages.x import X` inside every single
navigation method (which used to be the case here), that lazy resolution is
centralized in this one module instead. This file itself never imports a
concrete page module at its own top level -- only inside each small factory
function -- so nothing importing `pages.registry` at module level can ever
form a cycle through it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page

    from pages.account_created_page import AccountCreatedPage
    from pages.account_deleted_page import AccountDeletedPage
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage
    from pages.contact_us_page import ContactUsPage
    from pages.home_page import HomePage
    from pages.payment_page import PaymentPage
    from pages.product_detail_page import ProductDetailPage
    from pages.products_page import ProductsPage
    from pages.signup_login_page import SignupLoginPage
    from pages.signup_page import SignupPage


def home_page(page: "Page", base_url: str) -> "HomePage":
    from pages.home_page import HomePage

    return HomePage(page, base_url)


def signup_login_page(page: "Page", base_url: str) -> "SignupLoginPage":
    from pages.signup_login_page import SignupLoginPage

    return SignupLoginPage(page, base_url)


def signup_page(page: "Page", base_url: str) -> "SignupPage":
    from pages.signup_page import SignupPage

    return SignupPage(page, base_url)


def account_created_page(page: "Page", base_url: str) -> "AccountCreatedPage":
    from pages.account_created_page import AccountCreatedPage

    return AccountCreatedPage(page, base_url)


def account_deleted_page(page: "Page", base_url: str) -> "AccountDeletedPage":
    from pages.account_deleted_page import AccountDeletedPage

    return AccountDeletedPage(page, base_url)


def products_page(page: "Page", base_url: str) -> "ProductsPage":
    from pages.products_page import ProductsPage

    return ProductsPage(page, base_url)


def product_detail_page(page: "Page", base_url: str) -> "ProductDetailPage":
    from pages.product_detail_page import ProductDetailPage

    return ProductDetailPage(page, base_url)


def cart_page(page: "Page", base_url: str) -> "CartPage":
    from pages.cart_page import CartPage

    return CartPage(page, base_url)


def checkout_page(page: "Page", base_url: str) -> "CheckoutPage":
    from pages.checkout_page import CheckoutPage

    return CheckoutPage(page, base_url)


def payment_page(page: "Page", base_url: str) -> "PaymentPage":
    from pages.payment_page import PaymentPage

    return PaymentPage(page, base_url)


def contact_us_page(page: "Page", base_url: str) -> "ContactUsPage":
    from pages.contact_us_page import ContactUsPage

    return ContactUsPage(page, base_url)

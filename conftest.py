import re

import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from utils import verifications
from utils.test_data import unique_user_data


_AD_DOMAINS = (
    "googlesyndication.com",
    "doubleclick.net",
    "google.com/pagead",
    "googleadservices.com",
    "adservice.google.com",
)


@pytest.fixture
def home_page(page: Page, base_url: str) -> HomePage:
    # Block ad iframes/vignettes: the live site serves interstitial Google ads
    # that can overlay nav/sidebar links and intercept clicks mid-test.
    page.route(
        re.compile("|".join(re.escape(domain) for domain in _AD_DOMAINS)),
        lambda route: route.abort(),
    )

    home = HomePage(page, base_url)
    home.goto()
    return home


@pytest.fixture
def registered_user(home_page: HomePage) -> dict:
    """Registers a new account, logs out, and returns the user's credentials.

    Reuses SignupPage.complete_registration so the field-filling sequence has
    a single source of truth shared with the registration test.

    Teardown deletes the account if the test itself hasn't already deleted it,
    so accounts created for a test don't leak beyond it.
    """
    user = unique_user_data()

    signup_login_page = home_page.click_signup_login()
    signup_page = signup_login_page.signup(user["name"], user["email"])
    account_created_page = signup_page.complete_registration(user)
    home_page_after_signup = account_created_page.click_continue()
    home_page_after_signup.click_logout()

    yield user

    _delete_account_if_exists(home_page, user)


def _delete_account_if_exists(home_page: HomePage, user: dict) -> None:
    """Logs in as `user` and deletes the account, unless the test already deleted it."""
    home_page.goto()
    signup_login_page = home_page.click_signup_login()
    home_page_after_login = signup_login_page.login(user["email"], user["password"])

    try:
        verifications.assert_logged_in_as(home_page_after_login, user["name"])
    except AssertionError:
        return  # login failed -> account no longer exists, nothing to clean up

    home_page_after_login.click_delete_account()

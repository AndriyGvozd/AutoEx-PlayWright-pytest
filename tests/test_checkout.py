"""Checkout/Payment test suite for automationexercise.com.

Covers the Checkout/Payment-related test cases published at
https://www.automationexercise.com/test_cases (Test Case 14, 15, 16, 23, 24).
"""

import tempfile
from pathlib import Path

import allure

from pages.home_page import HomePage
from utils.allure_steps import step
from utils.test_data import unique_user_data

_CARD = {
    "name_on_card": "Test User",
    "card_number": "4111111111111111",
    "cvc": "123",
    "expiry_month": "12",
    "expiry_year": "2030",
}

_COMMENT = "Please handle this order with care."


def _add_first_product_to_cart(home_page: HomePage):
    page = home_page.page
    with step(page, "4. Add products to cart"):
        products_page = home_page.click_products()
        products_page.verify_all_products_page_visible()
        products_page.add_product_to_cart_by_index(0)
        products_page.click_continue_shopping()


@allure.feature("Checkout")
@allure.title("Test Case 14: Place Order: Register while Checkout")
def test_place_order_register_while_checkout(home_page: HomePage):
    """Test Case 14: Place Order: Register while Checkout."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    _add_first_product_to_cart(home_page)

    with step(page, "5-6. Click 'Cart' button, verify that cart page is displayed"):
        cart_page = home_page.click_cart()
        cart_page.verify_cart_page_visible()

    with step(page, "7. Click Proceed To Checkout -> not logged in, shows Register/Login modal"):
        cart_page.click_proceed_to_checkout()

    with step(page, "8. Click 'Register / Login' button"):
        signup_login_page = cart_page.click_register_login_from_checkout_modal()
        signup_login_page.verify_new_user_signup_visible()

    user = unique_user_data()
    with step(page, f"9. Fill all details in Signup (name='{user['name']}', email='{user['email']}') and create account"):
        signup_page = signup_login_page.signup(user["name"], user["email"])
        account_created_page = signup_page.complete_registration(user)

    with step(page, "10. Verify 'ACCOUNT CREATED!' and click 'Continue' button"):
        account_created_page.verify_account_created()
        home_page_after_signup = account_created_page.click_continue()

    with step(page, f"11. Verify 'Logged in as {user['name']}' at top"):
        home_page_after_signup.verify_logged_in_as(user["name"])

    with step(page, "12. Click 'Cart' button"):
        cart_page = home_page_after_signup.click_cart()

    with step(page, "13. Click 'Proceed To Checkout' button"):
        checkout_page = cart_page.click_proceed_to_checkout()

    with step(page, "14. Verify Address Details and Review Your Order"):
        checkout_page.verify_checkout_page_visible()

    with step(page, f"15. Enter description '{_COMMENT}' in comment text area and click 'Place Order'"):
        checkout_page.enter_comment(_COMMENT)
        payment_page = checkout_page.click_place_order()

    with step(page, "16-17. Enter payment details and click 'Pay and Confirm Order' button"):
        payment_page.pay(**_CARD)

    with step(page, "18. Verify success message"):
        payment_page.verify_order_placed_success()

    with step(page, "19. Click 'Delete Account' button"):
        account_deleted_page = payment_page.click_delete_account()

    with step(page, "20. Verify 'ACCOUNT DELETED!' and click 'Continue' button"):
        account_deleted_page.verify_account_deleted()
        account_deleted_page.click_continue()


@allure.feature("Checkout")
@allure.title("Test Case 15: Place Order: Register before Checkout")
def test_place_order_register_before_checkout(home_page: HomePage):
    """Test Case 15: Place Order: Register before Checkout."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click 'Signup / Login' button"):
        signup_login_page = home_page.click_signup_login()
        signup_login_page.verify_new_user_signup_visible()

    user = unique_user_data()
    with step(page, f"5. Fill all details in Signup (name='{user['name']}', email='{user['email']}') and create account"):
        signup_page = signup_login_page.signup(user["name"], user["email"])
        account_created_page = signup_page.complete_registration(user)

    with step(page, "6. Verify 'ACCOUNT CREATED!' and click 'Continue' button"):
        account_created_page.verify_account_created()
        home_page_after_signup = account_created_page.click_continue()

    with step(page, f"7. Verify 'Logged in as {user['name']}' at top"):
        home_page_after_signup.verify_logged_in_as(user["name"])

    _add_first_product_to_cart(home_page_after_signup)

    with step(page, "9-10. Click 'Cart' button, verify that cart page is displayed"):
        cart_page = home_page_after_signup.click_cart()
        cart_page.verify_cart_page_visible()

    with step(page, "11. Click Proceed To Checkout"):
        checkout_page = cart_page.click_proceed_to_checkout()

    with step(page, "12. Verify Address Details and Review Your Order"):
        checkout_page.verify_checkout_page_visible()

    with step(page, f"13. Enter description '{_COMMENT}' in comment text area and click 'Place Order'"):
        checkout_page.enter_comment(_COMMENT)
        payment_page = checkout_page.click_place_order()

    with step(page, "14-15. Enter payment details and click 'Pay and Confirm Order' button"):
        payment_page.pay(**_CARD)

    with step(page, "16. Verify success message"):
        payment_page.verify_order_placed_success()

    with step(page, "17. Click 'Delete Account' button"):
        account_deleted_page = payment_page.click_delete_account()

    with step(page, "18. Verify 'ACCOUNT DELETED!' and click 'Continue' button"):
        account_deleted_page.verify_account_deleted()
        account_deleted_page.click_continue()


@allure.feature("Checkout")
@allure.title("Test Case 16: Place Order: Login before Checkout")
def test_place_order_login_before_checkout(home_page: HomePage, registered_user: dict):
    """Test Case 16: Place Order: Login before Checkout."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click 'Signup / Login' button"):
        signup_login_page = home_page.click_signup_login()

    with step(page, f"5. Fill email '{registered_user['email']}', password and click 'Login' button"):
        home_page_after_login = signup_login_page.login(registered_user["email"], registered_user["password"])

    with step(page, f"6. Verify 'Logged in as {registered_user['name']}' at top"):
        home_page_after_login.verify_logged_in_as(registered_user["name"])

    _add_first_product_to_cart(home_page_after_login)

    with step(page, "8-9. Click 'Cart' button, verify that cart page is displayed"):
        cart_page = home_page_after_login.click_cart()
        cart_page.verify_cart_page_visible()

    with step(page, "10. Click Proceed To Checkout"):
        checkout_page = cart_page.click_proceed_to_checkout()

    with step(page, "11. Verify Address Details and Review Your Order"):
        checkout_page.verify_checkout_page_visible()

    with step(page, f"12. Enter description '{_COMMENT}' in comment text area and click 'Place Order'"):
        checkout_page.enter_comment(_COMMENT)
        payment_page = checkout_page.click_place_order()

    with step(page, "13-14. Enter payment details and click 'Pay and Confirm Order' button"):
        payment_page.pay(**_CARD)

    with step(page, "15. Verify success message"):
        payment_page.verify_order_placed_success()

    with step(page, "16. Click 'Delete Account' button"):
        account_deleted_page = payment_page.click_delete_account()

    with step(page, "17. Verify 'ACCOUNT DELETED!' and click 'Continue' button"):
        account_deleted_page.verify_account_deleted()
        account_deleted_page.click_continue()


@allure.feature("Checkout")
@allure.title("Test Case 23: Verify address details in checkout page")
def test_verify_address_details_in_checkout_page(home_page: HomePage):
    """Test Case 23: Verify address details in checkout page."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click 'Signup / Login' button"):
        signup_login_page = home_page.click_signup_login()
        signup_login_page.verify_new_user_signup_visible()

    user = unique_user_data()
    with step(page, f"5. Fill all details in Signup (name='{user['name']}', email='{user['email']}') and create account"):
        signup_page = signup_login_page.signup(user["name"], user["email"])
        account_created_page = signup_page.complete_registration(user)

    with step(page, "6. Verify 'ACCOUNT CREATED!' and click 'Continue' button"):
        account_created_page.verify_account_created()
        home_page_after_signup = account_created_page.click_continue()

    with step(page, f"7. Verify 'Logged in as {user['name']}' at top"):
        home_page_after_signup.verify_logged_in_as(user["name"])

    _add_first_product_to_cart(home_page_after_signup)

    with step(page, "9-10. Click 'Cart' button, verify that cart page is displayed"):
        cart_page = home_page_after_signup.click_cart()
        cart_page.verify_cart_page_visible()

    with step(page, "11. Click Proceed To Checkout"):
        checkout_page = cart_page.click_proceed_to_checkout()
        checkout_page.verify_checkout_page_visible()

    with step(
        page,
        f"12-13. Verify that the delivery address and billing address match address filled at "
        f"registration (name='{user['first_name']} {user['last_name']}', address='{user['address1']}')",
    ):
        checkout_page.verify_address_matches_user(user)

    # 14. Click 'Delete Account' button
    # (the header nav, including 'Delete Account', is shared across pages, so
    # the original `home_page` object's locator still resolves here)
    with step(page, "14. Click 'Delete Account' button"):
        account_deleted_page = home_page.click_delete_account()

    with step(page, "15. Verify 'ACCOUNT DELETED!' and click 'Continue' button"):
        account_deleted_page.verify_account_deleted()
        account_deleted_page.click_continue()


@allure.feature("Checkout")
@allure.title("Test Case 24: Download Invoice after purchase order")
def test_download_invoice_after_purchase_order(home_page: HomePage):
    """Test Case 24: Download Invoice after purchase order."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    _add_first_product_to_cart(home_page)

    with step(page, "5-6. Click 'Cart' button, verify that cart page is displayed"):
        cart_page = home_page.click_cart()
        cart_page.verify_cart_page_visible()

    with step(page, "7. Click Proceed To Checkout -> not logged in, shows Register/Login modal"):
        cart_page.click_proceed_to_checkout()

    with step(page, "8. Click 'Register / Login' button"):
        signup_login_page = cart_page.click_register_login_from_checkout_modal()

    user = unique_user_data()
    with step(page, f"9. Fill all details in Signup (name='{user['name']}', email='{user['email']}') and create account"):
        signup_page = signup_login_page.signup(user["name"], user["email"])
        account_created_page = signup_page.complete_registration(user)

    with step(page, "10. Verify 'ACCOUNT CREATED!' and click 'Continue' button"):
        account_created_page.verify_account_created()
        home_page_after_signup = account_created_page.click_continue()

    with step(page, f"11. Verify 'Logged in as {user['name']}' at top"):
        home_page_after_signup.verify_logged_in_as(user["name"])

    with step(page, "12. Click 'Cart' button"):
        cart_page = home_page_after_signup.click_cart()

    with step(page, "13. Click 'Proceed To Checkout' button"):
        checkout_page = cart_page.click_proceed_to_checkout()

    with step(page, "14. Verify Address Details and Review Your Order"):
        checkout_page.verify_checkout_page_visible()

    with step(page, f"15. Enter description '{_COMMENT}' in comment text area and click 'Place Order'"):
        checkout_page.enter_comment(_COMMENT)
        payment_page = checkout_page.click_place_order()

    with step(page, "16-17. Enter payment details and click 'Pay and Confirm Order' button"):
        payment_page.pay(**_CARD)

    with step(page, "18. Verify success message"):
        payment_page.verify_order_placed_success()

    with tempfile.TemporaryDirectory() as tmp_dir:
        destination = Path(tmp_dir) / "invoice.txt"
        with step(page, "19. Click 'Download Invoice' button and verify invoice is downloaded successfully"):
            saved_path = payment_page.download_invoice(destination)
            assert saved_path.exists(), "Downloaded invoice file was not saved"
            assert saved_path.stat().st_size > 0, "Downloaded invoice file is empty"

    with step(page, "20. Click 'Continue' button"):
        home_page_after_order = payment_page.click_continue()

    with step(page, "21. Click 'Delete Account' button"):
        account_deleted_page = home_page_after_order.click_delete_account()

    with step(page, "22. Verify 'ACCOUNT DELETED!' and click 'Continue' button"):
        account_deleted_page.verify_account_deleted()
        account_deleted_page.click_continue()

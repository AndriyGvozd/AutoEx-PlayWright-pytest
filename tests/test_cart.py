"""Cart test suite for automationexercise.com.

Covers the Cart-related test cases published at
https://www.automationexercise.com/test_cases (Test Case 11, 12, 13, 17, 20, 22).
"""

import allure

from pages.home_page import HomePage
from utils import verifications
from utils.allure_steps import step


@allure.feature("Cart")
@allure.title("Test Case 11: Verify Subscription in Cart page")
def test_verify_subscription_in_cart_page(home_page: HomePage):
    """Test Case 11: Verify Subscription in Cart page."""
    page = home_page.page
    email = "qa_subscribe_check@example.com"

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click 'Cart' button"):
        cart_page = home_page.click_cart()
        verifications.assert_cart_page_visible(cart_page)

    with step(page, "5. Scroll down to footer"):
        cart_page.scroll_to_subscription()

    with step(page, "6. Verify text 'SUBSCRIPTION'"):
        verifications.assert_subscription_heading_visible(cart_page)

    with step(page, f"7. Enter email address '{email}' in input and click arrow button"):
        cart_page.subscribe(email)

    with step(page, "8. Verify success message 'You have been successfully subscribed!' is visible"):
        verifications.assert_subscription_success(cart_page)


@allure.feature("Cart")
@allure.title("Test Case 12: Add Products in Cart")
def test_add_products_in_cart(home_page: HomePage):
    """Test Case 12: Add Products in Cart."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click 'Products' button"):
        products_page = home_page.click_products()
        verifications.assert_all_products_page_visible(products_page)

    first_name = products_page.get_product_name(0)
    first_price = products_page.get_product_price(0)
    second_name = products_page.get_product_name(1)
    second_price = products_page.get_product_price(1)

    with step(page, f"5. Hover over first product '{first_name}' and click 'Add to cart'"):
        products_page.add_product_to_cart_by_index(0)

    with step(page, "6. Click 'Continue Shopping' button"):
        products_page.click_continue_shopping()

    with step(page, f"7. Hover over second product '{second_name}' and click 'Add to cart'"):
        products_page.add_product_to_cart_by_index(1)

    with step(page, "8. Click 'View Cart' button"):
        cart_page = products_page.click_view_cart_from_modal()
        verifications.assert_cart_page_visible(cart_page)

    with step(page, f"9. Verify both products '{first_name}' and '{second_name}' are added to Cart"):
        verifications.assert_product_in_cart(cart_page, first_name)
        verifications.assert_product_in_cart(cart_page, second_name)

    with step(page, "10. Verify their prices, quantity and total price"):
        assert cart_page.get_product_price(first_name) == first_price
        assert cart_page.get_product_price(second_name) == second_price
        verifications.assert_product_quantity_in_cart(cart_page, first_name, "1")
        verifications.assert_product_quantity_in_cart(cart_page, second_name, "1")
        assert cart_page.get_product_total(first_name) == first_price
        assert cart_page.get_product_total(second_name) == second_price


@allure.feature("Cart")
@allure.title("Test Case 13: Verify Product quantity in Cart")
def test_verify_product_quantity_in_cart(home_page: HomePage):
    """Test Case 13: Verify Product quantity in Cart."""
    page = home_page.page
    quantity = 4

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click 'View Product' for any product"):
        products_page = home_page.click_products()
        product_detail_page = products_page.click_view_product(0)

    with step(page, "5. Verify product detail is opened"):
        verifications.assert_product_detail_visible(product_detail_page)
        product_name = product_detail_page.product_name.inner_text()

    with step(page, f"6. Increase quantity to {quantity}"):
        product_detail_page.set_quantity(quantity)

    with step(page, "7. Click 'Add to cart' button"):
        product_detail_page.add_to_cart()

    with step(page, "8. Click 'View Cart' button"):
        cart_page = product_detail_page.click_view_cart()
        verifications.assert_cart_page_visible(cart_page)

    with step(page, f"9. Verify that product '{product_name}' is displayed in cart page with exact quantity {quantity}"):
        verifications.assert_product_in_cart(cart_page, product_name)
        verifications.assert_product_quantity_in_cart(cart_page, product_name, str(quantity))


@allure.feature("Cart")
@allure.title("Test Case 17: Remove Products From Cart")
def test_remove_products_from_cart(home_page: HomePage):
    """Test Case 17: Remove Products From Cart."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Add products to cart"):
        products_page = home_page.click_products()
        verifications.assert_all_products_page_visible(products_page)

        first_name = products_page.get_product_name(0)
        second_name = products_page.get_product_name(1)

        products_page.add_product_to_cart_by_index(0)
        products_page.click_continue_shopping()
        products_page.add_product_to_cart_by_index(1)

    with step(page, "5. Click 'Cart' button"):
        cart_page = products_page.click_view_cart_from_modal()

    with step(page, "6. Verify that cart page is displayed"):
        verifications.assert_cart_page_visible(cart_page)
        verifications.assert_product_in_cart(cart_page, first_name)
        verifications.assert_product_in_cart(cart_page, second_name)

    with step(page, f"7. Click 'X' button corresponding to particular product '{first_name}'"):
        cart_page.remove_product(first_name)

    with step(page, f"8. Verify that product '{first_name}' is removed from the cart"):
        verifications.assert_product_not_in_cart(cart_page, first_name)
        verifications.assert_product_in_cart(cart_page, second_name)


@allure.feature("Cart")
@allure.title("Test Case 20: Search Products and Verify Cart After Login")
def test_search_products_and_verify_cart_after_login(home_page: HomePage, registered_user: dict):
    """Test Case 20: Search Products and Verify Cart After Login."""
    page = home_page.page
    search_term = "Top"

    with step(page, "3. Click on 'Products' button"):
        products_page = home_page.click_products()

    with step(page, "4. Verify user is navigated to ALL PRODUCTS page successfully"):
        verifications.assert_all_products_page_visible(products_page)

    with step(page, f"5. Enter product name '{search_term}' in search input and click search button"):
        products_page.search_product(search_term)

    with step(page, "6. Verify 'SEARCHED PRODUCTS' is visible"):
        verifications.assert_searched_products_visible(products_page, search_term)

    with step(page, "7. Verify all the products related to search are visible"):
        verifications.assert_search_results_visible(products_page)

    searched_name = products_page.get_product_name(0)

    with step(page, f"8. Add those products '{searched_name}' to cart"):
        products_page.add_product_to_cart_by_index(0)
        products_page.click_continue_shopping()

    with step(page, "9. Click 'Cart' button and verify that products are visible in cart"):
        cart_page = home_page.click_cart()
        verifications.assert_cart_page_visible(cart_page)
        verifications.assert_product_in_cart(cart_page, searched_name)

    with step(page, f"10. Click 'Signup / Login' button and submit login details for '{registered_user['email']}'"):
        signup_login_page = home_page.click_signup_login()
        home_page_after_login = signup_login_page.login(registered_user["email"], registered_user["password"])
        verifications.assert_logged_in_as(home_page_after_login, registered_user["name"])

    with step(page, "11. Again, go to Cart page"):
        cart_page = home_page_after_login.click_cart()
        verifications.assert_cart_page_visible(cart_page)

    with step(page, f"12. Verify that those products '{searched_name}' are visible in cart after login as well"):
        verifications.assert_product_in_cart(cart_page, searched_name)

    # Clean up: this test logs in, so leave the app in a logged-in state
    # consistent with the registered_user fixture's teardown expectations.
    home_page_after_login.click_logout()


@allure.feature("Cart")
@allure.title("Test Case 22: Add to cart from Recommended items")
def test_add_to_cart_from_recommended_items(home_page: HomePage):
    """Test Case 22: Add to cart from Recommended items."""
    page = home_page.page

    with step(page, "3. Scroll to bottom of page"):
        home_page.scroll_to_bottom()

    with step(page, "4. Verify 'RECOMMENDED ITEMS' are visible"):
        verifications.assert_recommended_items_visible(home_page)

    recommended_name = home_page.get_recommended_product_name(0)

    with step(page, f"5. Click on 'Add To Cart' on Recommended product '{recommended_name}'"):
        home_page.add_recommended_product_to_cart(0)

    with step(page, "6. Click on 'View Cart' button"):
        cart_page = home_page.click_view_cart_from_modal()

    with step(page, f"7. Verify that product '{recommended_name}' is displayed in cart page"):
        verifications.assert_cart_page_visible(cart_page)
        verifications.assert_product_in_cart(cart_page, recommended_name)

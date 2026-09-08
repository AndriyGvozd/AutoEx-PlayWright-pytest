"""Cart test suite for automationexercise.com.

Covers the Cart-related test cases published at
https://www.automationexercise.com/test_cases (Test Case 11, 12, 13, 17, 20, 22).
"""

import allure

from pages.home_page import HomePage
from utils.allure_steps import step


@allure.feature("Cart")
@allure.title("Test Case 11: Verify Subscription in Cart page")
def test_verify_subscription_in_cart_page(home_page: HomePage):
    """Test Case 11: Verify Subscription in Cart page."""
    page = home_page.page
    email = "qa_subscribe_check@example.com"

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click 'Cart' button"):
        cart_page = home_page.click_cart()
        cart_page.verify_cart_page_visible()

    with step(page, "5. Scroll down to footer"):
        cart_page.scroll_to_subscription()

    with step(page, "6. Verify text 'SUBSCRIPTION'"):
        cart_page.verify_subscription_heading_visible()

    with step(page, f"7. Enter email address '{email}' in input and click arrow button"):
        cart_page.subscribe(email)

    with step(page, "8. Verify success message 'You have been successfully subscribed!' is visible"):
        cart_page.verify_subscription_success()


@allure.feature("Cart")
@allure.title("Test Case 12: Add Products in Cart")
def test_add_products_in_cart(home_page: HomePage):
    """Test Case 12: Add Products in Cart."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click 'Products' button"):
        products_page = home_page.click_products()
        products_page.verify_all_products_page_visible()

    first_name = products_page.products_list.nth(0).locator(".productinfo p").inner_text()
    first_price = products_page.products_list.nth(0).locator(".productinfo h2").inner_text()
    second_name = products_page.products_list.nth(1).locator(".productinfo p").inner_text()
    second_price = products_page.products_list.nth(1).locator(".productinfo h2").inner_text()

    with step(page, f"5. Hover over first product '{first_name}' and click 'Add to cart'"):
        products_page.add_product_to_cart_by_index(0)

    with step(page, "6. Click 'Continue Shopping' button"):
        products_page.click_continue_shopping()

    with step(page, f"7. Hover over second product '{second_name}' and click 'Add to cart'"):
        products_page.add_product_to_cart_by_index(1)

    with step(page, "8. Click 'View Cart' button"):
        cart_page = products_page.click_view_cart_from_modal()
        cart_page.verify_cart_page_visible()

    with step(page, f"9. Verify both products '{first_name}' and '{second_name}' are added to Cart"):
        cart_page.verify_product_in_cart(first_name)
        cart_page.verify_product_in_cart(second_name)

    with step(page, "10. Verify their prices, quantity and total price"):
        assert cart_page.get_product_price(first_name) == first_price
        assert cart_page.get_product_price(second_name) == second_price
        cart_page.verify_product_quantity(first_name, "1")
        cart_page.verify_product_quantity(second_name, "1")
        assert cart_page.get_product_total(first_name) == first_price
        assert cart_page.get_product_total(second_name) == second_price


@allure.feature("Cart")
@allure.title("Test Case 13: Verify Product quantity in Cart")
def test_verify_product_quantity_in_cart(home_page: HomePage):
    """Test Case 13: Verify Product quantity in Cart."""
    page = home_page.page
    quantity = 4

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click 'View Product' for any product"):
        products_page = home_page.click_products()
        product_detail_page = products_page.click_view_product(0)

    with step(page, "5. Verify product detail is opened"):
        product_detail_page.verify_product_detail_visible()
        product_name = product_detail_page.product_name.inner_text()

    with step(page, f"6. Increase quantity to {quantity}"):
        product_detail_page.set_quantity(quantity)

    with step(page, "7. Click 'Add to cart' button"):
        product_detail_page.add_to_cart()

    with step(page, "8. Click 'View Cart' button"):
        cart_page = product_detail_page.click_view_cart()
        cart_page.verify_cart_page_visible()

    with step(page, f"9. Verify that product '{product_name}' is displayed in cart page with exact quantity {quantity}"):
        cart_page.verify_product_in_cart(product_name)
        cart_page.verify_product_quantity(product_name, str(quantity))


@allure.feature("Cart")
@allure.title("Test Case 17: Remove Products From Cart")
def test_remove_products_from_cart(home_page: HomePage):
    """Test Case 17: Remove Products From Cart."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Add products to cart"):
        products_page = home_page.click_products()
        products_page.verify_all_products_page_visible()

        first_name = products_page.products_list.nth(0).locator(".productinfo p").inner_text()
        second_name = products_page.products_list.nth(1).locator(".productinfo p").inner_text()

        products_page.add_product_to_cart_by_index(0)
        products_page.click_continue_shopping()
        products_page.add_product_to_cart_by_index(1)

    with step(page, "5. Click 'Cart' button"):
        cart_page = products_page.click_view_cart_from_modal()

    with step(page, "6. Verify that cart page is displayed"):
        cart_page.verify_cart_page_visible()
        cart_page.verify_product_in_cart(first_name)
        cart_page.verify_product_in_cart(second_name)

    with step(page, f"7. Click 'X' button corresponding to particular product '{first_name}'"):
        cart_page.remove_product(first_name)

    with step(page, f"8. Verify that product '{first_name}' is removed from the cart"):
        cart_page.verify_product_not_in_cart(first_name)
        cart_page.verify_product_in_cart(second_name)


@allure.feature("Cart")
@allure.title("Test Case 20: Search Products and Verify Cart After Login")
def test_search_products_and_verify_cart_after_login(home_page: HomePage, registered_user: dict):
    """Test Case 20: Search Products and Verify Cart After Login."""
    page = home_page.page
    search_term = "Top"

    with step(page, "3. Click on 'Products' button"):
        products_page = home_page.click_products()

    with step(page, "4. Verify user is navigated to ALL PRODUCTS page successfully"):
        products_page.verify_all_products_page_visible()

    with step(page, f"5. Enter product name '{search_term}' in search input and click search button"):
        products_page.search_product(search_term)

    with step(page, "6. Verify 'SEARCHED PRODUCTS' is visible"):
        products_page.verify_searched_products_visible(search_term)

    with step(page, "7. Verify all the products related to search are visible"):
        products_page.verify_search_results_visible()

    searched_name = products_page.products_list.nth(0).locator(".productinfo p").inner_text()

    with step(page, f"8. Add those products '{searched_name}' to cart"):
        products_page.add_product_to_cart_by_index(0)
        products_page.click_continue_shopping()

    with step(page, "9. Click 'Cart' button and verify that products are visible in cart"):
        cart_page = home_page.click_cart()
        cart_page.verify_cart_page_visible()
        cart_page.verify_product_in_cart(searched_name)

    with step(page, f"10. Click 'Signup / Login' button and submit login details for '{registered_user['email']}'"):
        signup_login_page = home_page.click_signup_login()
        home_page_after_login = signup_login_page.login(registered_user["email"], registered_user["password"])
        home_page_after_login.verify_logged_in_as(registered_user["name"])

    with step(page, "11. Again, go to Cart page"):
        cart_page = home_page_after_login.click_cart()
        cart_page.verify_cart_page_visible()

    with step(page, f"12. Verify that those products '{searched_name}' are visible in cart after login as well"):
        cart_page.verify_product_in_cart(searched_name)

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
        home_page.verify_recommended_items_visible()

    recommended_name = home_page.recommended_items.nth(0).locator("p").inner_text()

    with step(page, f"5. Click on 'Add To Cart' on Recommended product '{recommended_name}'"):
        home_page.add_recommended_product_to_cart(0)

    with step(page, "6. Click on 'View Cart' button"):
        cart_page = home_page.click_view_cart_from_modal()

    with step(page, f"7. Verify that product '{recommended_name}' is displayed in cart page"):
        cart_page.verify_cart_page_visible()
        cart_page.verify_product_in_cart(recommended_name)

"""Products test suite for automationexercise.com.

Covers the Products-related test cases published at
https://www.automationexercise.com/test_cases (Test Case 7, 8, 9, 18, 19, 21).
"""

import allure

from pages.home_page import HomePage
from utils import verifications
from utils.allure_steps import step
from utils.test_data import unique_user_data


@allure.feature("Products")
@allure.title("Test Case 7: Verify Test Cases Page")
def test_verify_test_cases_page(home_page: HomePage):
    """Test Case 7: Verify Test Cases Page."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Test Cases' button"):
        home_page.click_test_cases()

    with step(page, "5. Verify user is navigated to test cases page successfully"):
        verifications.assert_navigated_to_test_cases_page(home_page)


@allure.feature("Products")
@allure.title("Test Case 8: Verify All Products and product detail page")
def test_verify_all_products_and_product_detail_page(home_page: HomePage):
    """Test Case 8: Verify All Products and product detail page."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Products' button"):
        products_page = home_page.click_products()

    with step(page, "5. Verify user is navigated to ALL PRODUCTS page successfully"):
        verifications.assert_all_products_page_visible(products_page)

    with step(page, "6. Click on 'View Product' of any product"):
        product_detail_page = products_page.click_view_product(0)

    with step(page, "7. Verify that user is landed to product detail page"):
        verifications.assert_product_detail_visible(product_detail_page)


@allure.feature("Products")
@allure.title("Test Case 9: Search Product")
def test_search_product(home_page: HomePage):
    """Test Case 9: Search Product."""
    page = home_page.page
    search_term = "Top"

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Products' button"):
        products_page = home_page.click_products()

    with step(page, "5. Verify user is navigated to ALL PRODUCTS page successfully"):
        verifications.assert_all_products_page_visible(products_page)

    with step(page, f"6-7. Enter product name '{search_term}' in search input and click search button"):
        products_page.search_product(search_term)

    with step(page, "8. Verify 'SEARCHED PRODUCTS' is visible"):
        verifications.assert_searched_products_visible(products_page, search_term)

    with step(page, "9. Verify all the products related to search are visible"):
        verifications.assert_search_results_visible(products_page)


@allure.feature("Products")
@allure.title("Test Case 18: View Category Products")
def test_view_category_products(home_page: HomePage):
    """Test Case 18: View Category Products."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Verify categories are visible on left side bar"):
        products_page = home_page.click_products()
        verifications.assert_category_visible(products_page)

    with step(page, "5-6. Click on 'Women' category, click on any category link, e.g. 'Tops'"):
        products_page.click_category("Women", "Tops")

    # Note: the live site renders this heading as "Women - Tops Products" (mixed case),
    # not the all-caps text used in the official test case description.
    with step(page, "7. Verify that category page is displayed and confirm text 'WOMEN - TOPS PRODUCTS' is visible"):
        verifications.assert_category_products_title(products_page, "Women - Tops Products")


@allure.feature("Products")
@allure.title("Test Case 19: View & Cart Brand Products")
def test_view_and_cart_brand_products(home_page: HomePage):
    """Test Case 19: View & Cart Brand Products."""
    page = home_page.page
    brand_name = "Polo"

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Verify categories are visible on left side bar"):
        products_page = home_page.click_products()
        verifications.assert_brands_visible(products_page)

    with step(page, "5. Verify brands are visible on left side bar"):
        verifications.assert_brand_link_visible(products_page, brand_name)

    with step(page, f"6. Click on any brand name, e.g. '{brand_name}'"):
        products_page.click_brand(brand_name)

    with step(page, "7. Verify that user is navigated to brand page and brand products are displayed"):
        verifications.assert_brand_products_title(products_page, f"Brand - {brand_name} Products")

    with step(page, "Add the first brand product to cart and verify it in the cart"):
        product_name = products_page.get_product_name(0)
        products_page.add_product_to_cart_by_index(0)
        cart_page = products_page.click_view_cart_from_modal()
        verifications.assert_cart_page_visible(cart_page)
        verifications.assert_product_in_cart(cart_page, product_name)


@allure.feature("Products")
@allure.title("Test Case 21: Add review on product")
def test_add_review_on_product(home_page: HomePage):
    """Test Case 21: Add review on product."""
    user = unique_user_data()
    page = home_page.page
    review_text = "Great product, exactly as described!"

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Products' button"):
        products_page = home_page.click_products()

    with step(page, "5. Click on 'View Product' button for any product on products page"):
        product_detail_page = products_page.click_view_product(0)

    with step(page, "6. Verify 'Write Your Review' is visible"):
        verifications.assert_write_review_link_visible(product_detail_page)

    with step(
        page,
        f"7-8. Enter name '{user['name']}', email '{user['email']}' and review '{review_text}', "
        "click 'Submit' button",
    ):
        product_detail_page.write_review(user["name"], user["email"], review_text)

    with step(page, "9. Verify success message 'Thank you for your review.' is visible"):
        verifications.assert_review_success_visible(product_detail_page)

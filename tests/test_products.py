"""Products test suite for automationexercise.com.

Covers the Products-related test cases published at
https://www.automationexercise.com/test_cases (Test Case 7, 8, 9, 18, 19, 21).
"""

import allure
from playwright.sync_api import expect

from pages.home_page import HomePage
from utils.allure_steps import step
from utils.test_data import unique_user_data


@allure.feature("Products")
@allure.title("Test Case 7: Verify Test Cases Page")
def test_verify_test_cases_page(home_page: HomePage):
    """Test Case 7: Verify Test Cases Page."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click on 'Test Cases' button"):
        home_page.click_test_cases()


@allure.feature("Products")
@allure.title("Test Case 8: Verify All Products and product detail page")
def test_verify_all_products_and_product_detail_page(home_page: HomePage):
    """Test Case 8: Verify All Products and product detail page."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click on 'Products' button"):
        products_page = home_page.click_products()

    with step(page, "5. Verify user is navigated to ALL PRODUCTS page successfully"):
        products_page.verify_all_products_page_visible()
        expect(products_page.products_list.first).to_be_visible()

    with step(page, "6. Click on 'View Product' of any product"):
        product_detail_page = products_page.click_view_product(0)

    with step(page, "7. Verify that user is landed to product detail page"):
        product_detail_page.verify_product_detail_visible()


@allure.feature("Products")
@allure.title("Test Case 9: Search Product")
def test_search_product(home_page: HomePage):
    """Test Case 9: Search Product."""
    page = home_page.page
    search_term = "Top"

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click on 'Products' button"):
        products_page = home_page.click_products()

    with step(page, "5. Verify user is navigated to ALL PRODUCTS page successfully"):
        products_page.verify_all_products_page_visible()

    with step(page, f"6-7. Enter product name '{search_term}' in search input and click search button"):
        products_page.search_product(search_term)

    with step(page, "8. Verify 'SEARCHED PRODUCTS' is visible"):
        products_page.verify_searched_products_visible(search_term)

    with step(page, "9. Verify all the products related to search are visible"):
        products_page.verify_search_results_visible()


@allure.feature("Products")
@allure.title("Test Case 18: View Category Products")
def test_view_category_products(home_page: HomePage):
    """Test Case 18: View Category Products."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Verify categories are visible on left side bar"):
        products_page = home_page.click_products()
        expect(products_page.page.locator("h2", has_text="Category")).to_be_visible()

    with step(page, "5-6. Click on 'Women' category, click on any category link, e.g. 'Tops'"):
        products_page.click_category("Women", "Tops")

    # Note: the live site renders this heading as "Women - Tops Products" (mixed case),
    # not the all-caps text used in the official test case description.
    with step(page, "7. Verify that category page is displayed and confirm text 'WOMEN - TOPS PRODUCTS' is visible"):
        products_page.verify_category_products_title("Women - Tops Products")


@allure.feature("Products")
@allure.title("Test Case 19: View & Cart Brand Products")
def test_view_and_cart_brand_products(home_page: HomePage):
    """Test Case 19: View & Cart Brand Products."""
    page = home_page.page
    brand_name = "Polo"

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Verify categories are visible on left side bar"):
        products_page = home_page.click_products()
        expect(products_page.page.locator("h2", has_text="Brands")).to_be_visible()

    with step(page, "5. Verify brands are visible on left side bar"):
        expect(products_page.page.locator(f"a[href='/brand_products/{brand_name}']")).to_be_visible()

    with step(page, f"6. Click on any brand name, e.g. '{brand_name}'"):
        products_page.click_brand(brand_name)

    with step(page, "7. Verify that user is navigated to brand page and brand products are displayed"):
        products_page.verify_brand_products_title(f"Brand - {brand_name} Products")

    with step(page, "Add the first brand product to cart and verify it in the cart"):
        product_name = products_page.products_list.first.locator(".productinfo p").inner_text()
        products_page.add_product_to_cart_by_index(0)
        cart_page = products_page.click_view_cart_from_modal()
        cart_page.verify_cart_page_visible()
        cart_page.verify_product_in_cart(product_name)


@allure.feature("Products")
@allure.title("Test Case 21: Add review on product")
def test_add_review_on_product(home_page: HomePage):
    """Test Case 21: Add review on product."""
    user = unique_user_data()
    page = home_page.page
    review_text = "Great product, exactly as described!"

    with step(page, "3. Verify that home page is visible successfully"):
        home_page.verify_home_page_visible()

    with step(page, "4. Click on 'Products' button"):
        products_page = home_page.click_products()

    with step(page, "5. Click on 'View Product' button for any product on products page"):
        product_detail_page = products_page.click_view_product(0)

    with step(page, "6. Verify 'Write Your Review' is visible"):
        expect(product_detail_page.page.locator("a", has_text="Write Your Review")).to_be_visible()

    with step(
        page,
        f"7-8. Enter name '{user['name']}', email '{user['email']}' and review '{review_text}', "
        "click 'Submit' button",
    ):
        product_detail_page.write_review(user["name"], user["email"], review_text)

    with step(page, "9. Verify success message 'Thank you for your review.' is visible"):
        product_detail_page.verify_review_success_visible()

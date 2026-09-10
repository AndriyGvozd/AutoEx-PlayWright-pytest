"""Authorization flow test suite for automationexercise.com.

Covers the registration/login/logout test cases published at
https://www.automationexercise.com/test_cases (Test Case 1-5).
"""

import allure

from pages.home_page import HomePage
from utils import verifications
from utils.allure_steps import step
from utils.test_data import unique_user_data


@allure.feature("Authorization")
@allure.title("Test Case 1: Register User")
def test_register_user(home_page: HomePage):
    """Test Case 1: Register User."""
    user = unique_user_data()
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Signup / Login' button"):
        signup_login_page = home_page.click_signup_login()

    with step(page, "5. Verify 'New User Signup!' is visible"):
        verifications.assert_new_user_signup_visible(signup_login_page)

    with step(page, f"6-7. Enter name '{user['name']}' and email '{user['email']}', click 'Signup' button"):
        signup_page = signup_login_page.signup(user["name"], user["email"])

    with step(page, "8. Verify that 'ENTER ACCOUNT INFORMATION' is visible"):
        verifications.assert_account_info_visible(signup_page)

    with step(
        page,
        f"9-13. Fill account details (title='{user['title']}', password, date of birth) and "
        f"address details (name='{user['first_name']} {user['last_name']}', company='{user['company']}', "
        f"address='{user['address1']}', country='{user['country']}', state='{user['state']}', "
        f"city='{user['city']}', zipcode='{user['zipcode']}', mobile='{user['mobile_number']}'), "
        "select newsletter/offers checkboxes, click 'Create Account' button",
    ):
        account_created_page = signup_page.complete_registration(user)

    with step(page, "14. Verify that 'ACCOUNT CREATED!' is visible"):
        verifications.assert_account_created(account_created_page)

    with step(page, "15. Click 'Continue' button"):
        home_page_after_signup = account_created_page.click_continue()

    with step(page, f"16. Verify that 'Logged in as {user['name']}' is visible"):
        verifications.assert_logged_in_as(home_page_after_signup, user["name"])

    with step(page, "17. Click 'Delete Account' button"):
        account_deleted_page = home_page_after_signup.click_delete_account()

    with step(page, "18. Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button"):
        verifications.assert_account_deleted(account_deleted_page)
        account_deleted_page.click_continue()


@allure.feature("Authorization")
@allure.title("Test Case 2: Login User with correct email and password")
def test_login_with_correct_credentials(home_page: HomePage, registered_user: dict):
    """Test Case 2: Login User with correct email and password."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Signup / Login' button"):
        signup_login_page = home_page.click_signup_login()

    with step(page, "5. Verify 'Login to your account' is visible"):
        verifications.assert_login_to_account_visible(signup_login_page)

    with step(page, f"6-7. Enter correct email '{registered_user['email']}' and password, click 'login' button"):
        home_page_after_login = signup_login_page.login(registered_user["email"], registered_user["password"])

    with step(page, f"8. Verify that 'Logged in as {registered_user['name']}' is visible"):
        verifications.assert_logged_in_as(home_page_after_login, registered_user["name"])

    with step(page, "9. Click 'Delete Account' button"):
        account_deleted_page = home_page_after_login.click_delete_account()

    with step(page, "10. Verify that 'ACCOUNT DELETED!' is visible"):
        verifications.assert_account_deleted(account_deleted_page)


@allure.feature("Authorization")
@allure.title("Test Case 3: Login User with incorrect email and password")
def test_login_with_incorrect_credentials(home_page: HomePage):
    """Test Case 3: Login User with incorrect email and password."""
    page = home_page.page
    incorrect_email = "incorrect_email@example.com"

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Signup / Login' button"):
        signup_login_page = home_page.click_signup_login()

    with step(page, "5. Verify 'Login to your account' is visible"):
        verifications.assert_login_to_account_visible(signup_login_page)

    with step(page, f"6-7. Enter incorrect email '{incorrect_email}' and password, click 'login' button"):
        signup_login_page.login(incorrect_email, "wrong_password")

    with step(page, "8. Verify error 'Your email or password is incorrect!' is visible"):
        verifications.assert_login_error_visible(signup_login_page)


@allure.feature("Authorization")
@allure.title("Test Case 4: Logout User")
def test_logout_user(home_page: HomePage, registered_user: dict):
    """Test Case 4: Logout User."""
    page = home_page.page

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Signup / Login' button"):
        signup_login_page = home_page.click_signup_login()

    with step(page, "5. Verify 'Login to your account' is visible"):
        verifications.assert_login_to_account_visible(signup_login_page)

    with step(page, f"6-7. Enter correct email '{registered_user['email']}' and password, click 'login' button"):
        home_page_after_login = signup_login_page.login(registered_user["email"], registered_user["password"])

    with step(page, f"8. Verify that 'Logged in as {registered_user['name']}' is visible"):
        verifications.assert_logged_in_as(home_page_after_login, registered_user["name"])

    with step(page, "9. Click 'Logout' button"):
        login_page_after_logout = home_page_after_login.click_logout()

    with step(page, "10. Verify that user is navigated to login page"):
        verifications.assert_login_to_account_visible(login_page_after_logout)


@allure.feature("Authorization")
@allure.title("Test Case 5: Register User with existing email")
def test_register_user_with_existing_email(home_page: HomePage, registered_user: dict):
    """Test Case 5: Register User with existing email."""
    page = home_page.page
    new_name = unique_user_data()["name"]

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Signup / Login' button"):
        signup_login_page = home_page.click_signup_login()

    with step(page, "5. Verify 'New User Signup!' is visible"):
        verifications.assert_new_user_signup_visible(signup_login_page)

    with step(
        page,
        f"6-7. Enter name '{new_name}' and already registered email "
        f"'{registered_user['email']}', click 'Signup' button",
    ):
        signup_login_page.signup(new_name, registered_user["email"])

    with step(page, "8. Verify error 'Email Address already exist!' is visible"):
        verifications.assert_signup_error_visible(signup_login_page)

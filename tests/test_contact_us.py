"""Contact Us test suite for automationexercise.com.

Covers Test Case 6 published at https://www.automationexercise.com/test_cases.
"""

import os

import allure

from pages.home_page import HomePage
from utils import verifications
from utils.allure_steps import step
from utils.test_data import unique_user_data

_UPLOAD_FILE = os.path.join(os.path.dirname(__file__), "fixtures", "sample_upload.txt")


@allure.feature("Contact Us")
@allure.title("Test Case 6: Contact Us Form")
def test_contact_us_form(home_page: HomePage):
    """Test Case 6: Contact Us Form."""
    user = unique_user_data()
    page = home_page.page
    subject = "Test Case 6 subject"
    message = "Test Case 6 message body."

    with step(page, "3. Verify that home page is visible successfully"):
        verifications.assert_home_page_visible(home_page)

    with step(page, "4. Click on 'Contact Us' button"):
        contact_us_page = home_page.click_contact_us()

    with step(page, "5. Verify 'GET IN TOUCH' is visible"):
        verifications.assert_get_in_touch_visible(contact_us_page)

    with step(
        page,
        f"6. Enter name '{user['name']}', email '{user['email']}', subject '{subject}' and message '{message}'",
    ):
        contact_us_page.fill_contact_form(
            name=user["name"],
            email=user["email"],
            subject=subject,
            message=message,
        )

    with step(page, f"7. Upload file '{_UPLOAD_FILE}'"):
        contact_us_page.upload_file(_UPLOAD_FILE)

    with step(page, "8-9. Click 'Submit' button, click OK button on the confirm dialog"):
        contact_us_page.submit()

    with step(page, "10. Verify success message is visible"):
        verifications.assert_contact_us_success_visible(contact_us_page)

    with step(page, "11. Click 'Home' button and verify that landed to home page successfully"):
        home_page_after_submit = contact_us_page.click_home()
        verifications.assert_home_page_visible(home_page_after_submit)

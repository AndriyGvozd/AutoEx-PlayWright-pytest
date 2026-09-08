from contextlib import contextmanager

import allure
from playwright.sync_api import Page


@contextmanager
def step(page: Page, description: str):
    """Wraps a test step for Allure reporting.

    Records `description` as an Allure step (pass an f-string to parametrize
    it with the actual data used, e.g. f"Enter email '{email}'") and attaches
    a full-page screenshot of the resulting state once the step's actions
    complete, so every reported step carries its own visual evidence.
    """
    with allure.step(description):
        yield
        allure.attach(
            page.screenshot(full_page=True),
            name=description,
            attachment_type=allure.attachment_type.PNG,
        )

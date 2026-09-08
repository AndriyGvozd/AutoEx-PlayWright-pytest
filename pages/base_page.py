from playwright.sync_api import Page


class BasePage:
    URL = "https://automationexercise.com"

    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto(self.URL)

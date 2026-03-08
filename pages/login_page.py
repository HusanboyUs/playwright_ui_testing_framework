from .basepage import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):

    def __init__(self, page:Page):
        super().__init__(page=page)

    @property
    def login_error_message(self):
        return self.page.locator("xpath=.//h3[@data-test='error']")

    @property
    def login_button(self):
        return self.page.get_by_role(role="button", name="Login")

    def navigate(self):
        return super().navigate("")

    def login(self, username:str, password:str):
        self.page.get_by_placeholder(text="Username").fill(value=username)
        self.page.get_by_placeholder(text="Password").fill(value=password)
        self.login_button.click()
        

from playwright.sync_api import Page, expect
import pytest

from pages import LoginPage

from conftest import browser_firefox

@pytest.fixture(scope="session", autouse=True)
def browser_firefox(playwright:Playwright):
    browser = playwright.firefox.launch(headless=False)
    yield browser
    browser.close()



@pytest.mark.usefixtures(browser_firefox)
class TestLoginPage:

    @classmethod
    def setup(cls, browser_firefox):
        page = browser_firefox.new

    def test_login_page_with_incorrect_username_and_correct_password(self, login_page):
        
        expect(self.loginpage.page).not_to_have_title("Swag Labs")
        expect(self.loginpage.login_error_message).to_be_visible()
        expect(self.loginpage.login_error_message).to_have_text("Epic sadface: Username and password do not match any user in this service")


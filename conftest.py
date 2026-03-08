from playwright.sync_api import Page, Playwright
import pytest


@pytest.fixture(scope="session", autouse=True)
def browser_firefox(playwright:Playwright):
    browser = playwright.firefox.launch(headless=False)
    yield browser
    browser.close()


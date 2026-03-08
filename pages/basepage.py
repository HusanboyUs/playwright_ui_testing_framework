from playwright.sync_api import Page

class BasePage:

    def __init__(self, page):
        self.page:Page = page
        self.base_url = "https://www.saucedemo.com/"

    def navigate(self, path:str = ""):
        return self.page.goto(url=self.base_url + path)
    
    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")
    
    @property
    def get_page_title(self):
        return self.page.title()

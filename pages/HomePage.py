from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class HomePage(BasePage):
    URL = "https://insiderone.com/"

    #Locators
    HEADER = (By.CSS_SELECTOR, "header")
    FOOTER = (By.CSS_SELECTOR, "footer")
    BODY = (By.CSS_SELECTOR, "body")

    def load(self):
        self.open(self.URL)
        self.accept_cookies()

    def get_current_url(self) -> str:
        return self.driver.current_url

    def is_header_visible(self) -> bool:
        return self.is_visible(self.HEADER)

    def is_footer_visible(self) -> bool:
        return self.is_visible(self.FOOTER)

    def is_body_visible(self) -> bool:
        return self.is_visible(self.BODY)

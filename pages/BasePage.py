from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    TimeoutException,
)


class BasePage:
    def __init__(self, driver):
        self.driver = driver

        self.wait = WebDriverWait(driver, 30)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_visible(self, locator) -> bool:
        try:
            return self.driver.find_element(*locator).is_displayed()
        except Exception:
            return False

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def scroll_to(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def click_body(self):
        self.driver.find_element(By.CSS_SELECTOR, "body").click()

    def wait_until_text_contains(self, locator, expected_text: str):


        def condition(driver):
            try:
                text = driver.find_element(*locator).text or ""
                return expected_text.lower() in text.lower()
            except (StaleElementReferenceException, NoSuchElementException):
                return False

        self.wait.until(condition)

    def wait_until_all_contain(self, elements_locator, child_locator, expected_text: str):
        def condition(driver):
            elements = driver.find_elements(*elements_locator)
            if not elements:
                return False

            for el in elements:
                try:
                    text = el.find_element(*child_locator).text
                except StaleElementReferenceException:
                    return False
                if expected_text not in text:
                    return False

            return True

        self.wait.until(condition)

    def accept_cookies(self):
        cookie_btn = (By.CSS_SELECTOR, "#wt-cli-accept-all-btn")
        try:
            if self.driver.find_element(*cookie_btn).is_displayed():
                self.click(cookie_btn)
        except Exception:
            pass

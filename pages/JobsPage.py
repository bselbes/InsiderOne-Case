from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException

from pages.BasePage import BasePage


class JobsPage(BasePage):
    URL = "https://insiderone.com/careers/quality-assurance/"

    # Locators
    SEE_ALL_JOBS = (By.XPATH, "//a[normalize-space()='See all QA jobs']")
    DEPARTMENT_SELECTED = (By.CSS_SELECTOR, "#filter-by-department")
    FILTER_LOCATION = (By.CSS_SELECTOR, "#filter-by-location")
    JOB_CARD = (By.CSS_SELECTOR, "div.position-list-item")
    POSITION = (By.CSS_SELECTOR, "p.position-title")
    DEPARTMENT = (By.CSS_SELECTOR, ".position-department")
    LOCATION = (By.CSS_SELECTOR, ".position-location")
    VIEW_ROLE_IN_CARD = (By.XPATH, ".//a[contains(text(),'View Role')]")

    def load(self):
        self.open(self.URL)
        self.accept_cookies()

    def click_see_all_jobs(self):
        self.click(self.SEE_ALL_JOBS)
        self.wait.until(lambda d: "careers/open-positions" in d.current_url.lower())


    def get_selected_department(self) -> str:
        el = self.driver.find_element(*self.DEPARTMENT_SELECTED)
        return Select(el).first_selected_option.text.strip()

    def wait_until_job_cards_visible(self):
        self.wait.until(lambda d: len(d.find_elements(*self.JOB_CARD)) > 0)

    def wait_until_department_selected(self, expected_text: str):
        def condition(driver):
            try:
                el = driver.find_element(*self.DEPARTMENT_SELECTED)
                selected = Select(el).first_selected_option.text or ""
                return expected_text.lower() in selected.lower()
            except StaleElementReferenceException:
                return False

        self.wait.until(condition)


    def get_department_dropdown_text(self):
        return self.find(self.DEPARTMENT_SELECTED).text.strip()

    def get_jobs(self):
        return self.find_all(self.JOB_CARD)

    def get_job_details(self):
        jobs = self.get_jobs()
        details = []

        for job in jobs:
            details.append(
                {
                    "position": job.find_element(*self.POSITION).text.strip(),
                    "department": job.find_element(*self.DEPARTMENT).text.strip(),
                    "location": job.find_element(*self.LOCATION).text.strip(),
                }
            )

        return details

    def select_location(self, option_text, expected_location):
        option_locator = (
            By.XPATH,
            f"//select[@id='filter-by-location']/option[contains(text(),'{option_text}')]",
        )

        self.click(self.FILTER_LOCATION)
        self.scroll_to(option_locator)
        self.click(option_locator)
        self.click_body()

        self.wait_until_all_contain(self.JOB_CARD, self.LOCATION, expected_location)

    def open_first_job(self):
        first_job = self.get_jobs()[0]
        first_job.find_element(*self.VIEW_ROLE_IN_CARD).click()

    def switch_to_lever_page(self):
        self.wait.until(lambda d: len(d.window_handles) > 1 or "lever.co" in d.current_url.lower())

        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])

    def get_current_url(self):
        return self.driver.current_url

    def get_lever_job_details(self):
        title = self.driver.find_element(
            "css selector", "h2"
        ).text

        location = self.driver.find_element(
            "css selector", ".posting-categories .location"
        ).text

        department = self.driver.find_element(
            "css selector", ".posting-categories .department"
        ).text

        return {
            "title": title,
            "location": location,
            "department": department
        }
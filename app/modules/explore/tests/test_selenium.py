# Generated by Selenium IDE
from selenium.webdriver.common.by import By
from core.selenium.common import initialize_driver


class TestSeleniumverdadero():
    def setup_method(self):
        self.driver = initialize_driver()
        self.vars = {}
    def teardown_method(self, method):
        self.driver.quit()
    def test_seleniumverdadero(self):
        self.driver.get("http://localhost:5000/")
        self.driver.set_window_size(1850, 1053)
        self.driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)").click()
        self.driver.find_element(By.ID, "query").click()
        self.driver.find_element(By.ID, "query").send_keys("Cats")
        self.driver.find_element(By.ID, "search-button").click()

# Generated by Selenium IDE
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from core.selenium.common import initialize_driver, close_driver

class TestTestmaxminsizefilterUI():
  def setup_method(self, method):
    self.driver = initialize_driver()
    self.vars = {}

  def teardown_method(self, method):
    close_driver(self.driver)

  def test_testmaxminsizefilterUI(self):
    self.driver.get("http://127.0.0.1:5000/")
    self.driver.set_window_size(1920, 1048)
    self.driver.find_element(By.LINK_TEXT, "Team").click()
    self.driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)").click()
    self.driver.find_element(By.ID, "max_size").click()
    self.driver.find_element(By.ID, "max_size").send_keys("300")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.find_element(By.ID, "max_size").click()
    self.driver.find_element(By.ID, "max_size").send_keys("800")
    self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(7) > .col-12").click()
    self.driver.find_element(By.ID, "search-button").click()
    element = self.driver.find_element(By.ID, "search-button")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.ID, "max_size").click()
    self.driver.find_element(By.ID, "max_size").send_keys("1000")
    self.driver.find_element(By.ID, "search-button").click()
    element = self.driver.find_element(By.ID, "search-button")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, "body")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.ID, "min_size")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.ID, "min_size")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.ID, "min_size")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    self.driver.find_element(By.CSS_SELECTOR, ".col-12 > .row:nth-child(4)").click()
    self.driver.find_element(By.ID, "max_size").send_keys("100000")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.find_element(By.ID, "min_size").click()
    self.driver.find_element(By.ID, "min_size").send_keys("900")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.close()
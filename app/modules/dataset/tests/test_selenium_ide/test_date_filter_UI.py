# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestTestdatefilterUI():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()

  def test_testdatefilterUI(self):
    self.driver.get("http://127.0.0.1:5000/")
    self.driver.set_window_size(1920, 1048)
    self.driver.find_element(By.LINK_TEXT, "Explore").click()
    self.driver.find_element(By.ID, "end_date").click()
    self.driver.find_element(By.ID, "end_date").click()
    self.driver.find_element(By.ID, "end_date").send_keys("2022-05-09")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.find_element(By.ID, "start_date").click()
    self.driver.find_element(By.ID, "start_date").send_keys("2022-01-09")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.find_element(By.ID, "end_date").click()
    self.driver.find_element(By.ID, "end_date").send_keys("2023-12-09")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.close()
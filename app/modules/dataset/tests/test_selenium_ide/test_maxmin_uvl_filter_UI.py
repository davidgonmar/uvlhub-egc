# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestTestmaxminuvlfilterUI():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()

  def test_testmaxminuvlfilterUI(self):
    self.driver.get("http://127.0.0.1:5000/")
    self.driver.set_window_size(1761, 962)
    self.driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)").click()
    self.driver.find_element(By.ID, "min_uvl").click()
    self.driver.find_element(By.ID, "min_uvl").send_keys("1")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.find_element(By.ID, "min_uvl").click()
    self.driver.find_element(By.ID, "min_uvl").send_keys("10")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.find_element(By.ID, "min_uvl").click()
    self.driver.find_element(By.ID, "min_uvl").send_keys("3")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.find_element(By.ID, "max_uvl").click()
    self.driver.find_element(By.ID, "max_uvl").send_keys("10")
    self.driver.find_element(By.ID, "search-button").click()
    self.driver.find_element(By.ID, "max_uvl").click()
    self.driver.find_element(By.ID, "filters").click()
    self.driver.close()
# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestChatbotsuccesful():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()

  def test_chatbotsuccesful(self):
    self.driver.get("http://127.0.0.1:5000/chatbot")
    self.driver.set_window_size(1920, 1048)
    self.driver.find_element(By.ID, "chatInput").click()
    self.driver.find_element(By.ID, "chatInput").send_keys("Hola Romeo como estas?")
    self.driver.find_element(By.ID, "chatInput").send_keys(Keys.ENTER)
# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from core.selenium.common import initialize_driver, close_driver


class TestUI:
    def setup_method(self, method):
        self.driver = initialize_driver()
        self.vars = {}

    def teardown_method(self, method):
        close_driver(self.driver)

    def test_UI(self):
        # Test name: test_UI
        # Step # | name | target | value
        # 1 | open | /doi/10.1234/dataset4/ |
        self.driver.get("http://localhost:5000/doi/10.1234/dataset4/")
        # 2 | setWindowSize | 1536x816 |
        self.driver.set_window_size(1536, 816)
        # 3 | click | id=btnGroupDrop80 |
        self.driver.find_element(By.ID, "btnGroupDrop80").click()
        # 4 | click | linkText=Syntax check |
        self.driver.find_element(By.LINK_TEXT, "Syntax check").click()
        # 5 | click | id=btnGroupDropExport80 |
        self.driver.find_element(By.ID, "btnGroupDropExport80").click()
        # 6 | click | id=btnGroupDropExport80 |
        self.driver.find_element(By.ID, "btnGroupDropExport80").click()
        # 7 | click | css=.doi_text |
        self.driver.find_element(By.CSS_SELECTOR, ".doi_text").click()
        # 8 | click | css=.list-group-item:nth-child(2) .col-12 > .btn |
        self.driver.find_element(
            By.CSS_SELECTOR, ".list-group-item:nth-child(2) .col-12 > .btn"
        ).click()
        # 9 | close |  |
        self.driver.close()

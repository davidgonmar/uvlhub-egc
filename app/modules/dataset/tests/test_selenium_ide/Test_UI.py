import time
import os
from selenium.webdriver.common.by import By
from core.selenium.common import initialize_driver, close_driver


def get_downloads_folder():
    return os.path.join(os.path.expanduser('~'), 'Descargas')


class TestUi:
    def setup_method(self, method):
        self.driver = initialize_driver()
        self.downloads_dir = get_downloads_folder()
        self.vars = {}

    def teardown_method(self, method):
        close_driver(self.driver)

    def test_ui(self):
        self.driver.get("http://localhost:5000/")
        self.driver.set_window_size(1536, 816)
        # Navegar a la página del dataset
        self.driver.find_element(By.LINK_TEXT, "Tigers").click()
        # Descargar el archivo
        self.driver.find_element(By.ID, "btnGroupDropExport3").click()
        download_link = self.driver.find_element(By.LINK_TEXT, "UVL")
        download_link.click()
        time.sleep(1)  # Esperar a que la descarga se complete
        # Ejecutar el Syntax Check
        self.driver.find_element(By.ID, "btnGroupDrop1").click()
        self.driver.find_element(By.XPATH, "//a[text()='Syntax check']").click()

        # Abrir y cerrar el modal
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item:nth-child(4) .col-12 > .btn").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/div[2]/div[1]/div[2]/div/div/div[3]/div/div/div[1]/div/a").click()
        self.driver.find_element(By.CSS_SELECTOR, "#fileViewerModal > div > div > div.modal-header > div > button.btn-close").click()
        time.sleep(1)

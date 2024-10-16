from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Configurar Selenium para usar Chromium
options = webdriver.ChromeOptions()

# Quita '--headless' para ejecutar el navegador de manera visible
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Iniciar el driver de Chromium usando webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. Abrir Google
    driver.get("https://www.google.com")

    # 2. Esperar hasta que aparezca la ventana de cookies y hacer clic en "Rechazar todo"
    reject_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Rechazar todo')]"))
    )
    reject_cookies_button.click()

    # 3. Esperar hasta que el campo de búsqueda sea visible
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "q"))
    )

    # 4. Escribir "Selenium" en la barra de búsqueda y enviar el formulario
    search_box.send_keys("Selenium")
    search_box.send_keys(Keys.RETURN)

    # 5. Esperar a que el título cambie y contenga "Selenium"
    WebDriverWait(driver, 10).until(EC.title_contains("Selenium"))
    print("¡Selenium está funcionando correctamente con Chromium!")

except Exception as e:
    print(f"Error: {e}")
    driver.save_screenshot("error_screenshot.png")
    print("Captura de pantalla guardada como 'error_screenshot.png'")

finally:
    # Cerrar el navegador
    driver.quit()
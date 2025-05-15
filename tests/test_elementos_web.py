import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    # Setup
    ##driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    ##driver.maximize_window()
    ##yield driver
    # Teardown
    ##driver.quit()
    options = Options()
    options.add_argument("--headless")  # modo headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")  # en lugar de maximize_window()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_interaccion_con_elementos_web(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://the-internet.herokuapp.com/")

    # 1. Inputs
    driver.find_element(By.LINK_TEXT, "Inputs").click()
    input_field = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    input_field.send_keys("123")
    driver.back()

    # 2. Checkboxes
    driver.find_element(By.LINK_TEXT, "Checkboxes").click()
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()
        assert checkbox.is_selected()  # ✅ Asegura que esté marcado
    driver.back()

    # 3. Dropdown
    driver.find_element(By.LINK_TEXT, "Dropdown").click()
    dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "dropdown"))))
    dropdown.select_by_visible_text("Option 2")
    assert dropdown.first_selected_option.text == "Option 2"
    driver.back()

    # 4. Alert
    driver.find_element(By.LINK_TEXT, "JavaScript Alerts").click()
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
    wait.until(EC.alert_is_present()).accept()
    driver.back()

    # 5. Elemento dinámico
    driver.find_element(By.LINK_TEXT, "Dynamic Loading").click()
    driver.find_element(By.LINK_TEXT, "Example 1: Element on page that is hidden").click()
    driver.find_element(By.TAG_NAME, "button").click()
    mensaje = wait.until(EC.visibility_of_element_located((By.ID, "finish"))).text
    assert "Hello World!" in mensaje  # ✅ Verifica el mensaje cargado

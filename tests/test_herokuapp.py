import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_checkboxes(driver):
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    assert len(checkboxes) == 2
    # Marcar el primero si no está marcado
    if not checkboxes[0].is_selected():
        checkboxes[0].click()
    assert checkboxes[0].is_selected()

def test_dropdown(driver):
    driver.get("https://the-internet.herokuapp.com/dropdown")
    select = Select(driver.find_element(By.ID, "dropdown"))
    select.select_by_visible_text("Option 2")
    selected = select.first_selected_option
    assert selected.text == "Option 2"

def test_login_exitoso(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    mensaje = driver.find_element(By.ID, "flash").text
    assert "You logged into a secure area!" in mensaje

def test_login_fallido(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("usuario")
    driver.find_element(By.ID, "password").send_keys("clave_incorrecta")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    mensaje = driver.find_element(By.ID, "flash").text
    assert "Your username is invalid!" in mensaje

def test_inputs(driver):
    driver.get("https://the-internet.herokuapp.com/inputs")
    input_field = driver.find_element(By.TAG_NAME, "input")
    input_field.send_keys("12345")
    value = input_field.get_attribute("value")
    assert value == "12345"

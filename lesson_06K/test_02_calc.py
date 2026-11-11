from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_calc():
    driver = webdriver.Chrome()

    # 1. Открываем страницу в Google Chrome
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
    )

    # 2. В поле #delay вводим значение 45
    delay = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#delay"))
    )
    delay.clear()
    delay.send_keys("45")

    # 3. Нажимаем на кнопки 7, +, 8, =
    for button in ["7", "+", "8", "="]:
        driver.find_element(
            By.XPATH, f"//span[text()='{button}']"
        ).click()

    # 4. Ждём результат 15 (задержка 45 секунд) и проверяем его
    screen = (By.CSS_SELECTOR, ".screen")
    WebDriverWait(driver, 50).until(
        EC.text_to_be_present_in_element(screen, "15")
    )
    result = driver.find_element(*screen).text
    assert result == "15", f"Ожидался результат 15, получен: {result}"

    driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_dynamic_loading():
    driver = webdriver.Chrome()

    # 1. Откройте страницу https://the-internet.herokuapp.com/dynamic_loading/2
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")

    # 2. Найдите и нажмите на кнопку "Start"
    driver.find_element(By.CSS_SELECTOR, "#start button").click()

    # 3. Дождитесь появления текста "Hello World!"
    WebDriverWait(driver, 30).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#finish h4"), "Hello World!"
        )
    )

    # 4. Сделайте скриншот страницы
    driver.save_screenshot("lesson06_task1.png")

    # 5. Проверьте, что появившийся текст равен "Hello World!"
    result = driver.find_element(By.CSS_SELECTOR, "#finish h4")
    assert result.text == "Hello World!", (
        f"Ожидался текст 'Hello World!', получен: '{result.text}'"
    )

    driver.quit()
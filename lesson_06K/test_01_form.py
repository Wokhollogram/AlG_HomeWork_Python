from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form():
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10)

    # 1. Открывается страница в браузере Edge
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
    )

    # 2. Заполняется форма (поле Zip code оставляем пустым)
    data = {
        "first-name": "Иван",
        "last-name": "Петров",
        "address": "Ленина, 55-3",
        "e-mail": "test@skypro.com",
        "phone": "+7985899998787",
        "city": "Москва",
        "country": "Россия",
        "job-position": "QA",
        "company": "SkyPro",
    }
    for name, value in data.items():
        field = wait.until(EC.visibility_of_element_located((By.NAME, name)))
        field.send_keys(value)

    # 3. Нажимаем кнопку Submit
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # 4. Проверяем, что поле Zip code подсвечено красным
    zip_code = wait.until(
        EC.visibility_of_element_located((By.ID, "zip-code"))
    )
    assert "alert-danger" in zip_code.get_attribute("class")

    # 5. Проверяем, что остальные поля подсвечены зелёным
    for name in data:
        field = driver.find_element(By.ID, name)
        assert "alert-success" in field.get_attribute("class"), (
            f"Поле {name} не подсвечено зелёным"
        )

    driver.quit()
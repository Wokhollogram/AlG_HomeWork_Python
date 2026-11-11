from selenium import webdriver
from selenium.webdriver.common.by import By


def test_form_submission():
    driver = webdriver.Chrome()
    form_url = "https://httpbin.qa-territory.online/forms/post"
    driver.get(form_url)

    # 2-3. Находим поле custname и вводим имя
    name_input = driver.find_element(By.NAME, "custname")
    name_input.send_keys("Ivan")

    # 4. Находим кнопку Submit и нажимаем на неё
    driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()

    # 5. Проверяем, что URL изменился
    assert driver.current_url != form_url, (
        f"URL не изменился после отправки формы: {driver.current_url}"
    )

    driver.quit()
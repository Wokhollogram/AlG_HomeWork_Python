from selenium import webdriver
from selenium.webdriver.common.by import By


def test_navigation():
    driver = webdriver.Chrome()

    # 1. Открываем главную страницу
    base_url = "https://httpbin.qa-territory.online"
    driver.get(base_url)
    initial_url = driver.current_url

    # 2. Находим и кликаем на ссылку "HTML Form"
    driver.find_element(By.LINK_TEXT, "HTML Form").click()

    # 3. Проверяем, что URL изменился на /forms/post
    assert driver.current_url.endswith("/forms/post"), (
        f"Ожидался URL, оканчивающийся на /forms/post, "
        f"но получен: {driver.current_url}"
    )

    # 4. Возвращаемся назад на главную страницу
    driver.back()

    # 5. Проверяем, что вернулись на исходный URL
    assert driver.current_url == initial_url, (
        f"Ожидался URL {initial_url}, но получен: {driver.current_url}"
    )

    driver.quit()
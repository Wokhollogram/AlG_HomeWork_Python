from selenium import webdriver
from selenium.webdriver.common.by import By


def test_multiple_elements():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.qa-territory.online/links/10")

    # 2. Находим все ссылки на странице
    links = driver.find_elements(By.TAG_NAME, "a")

    # 3. Проверяем количество ссылок
    assert len(links) == 9, f"Ожидалось 9 ссылок, найдено: {len(links)}"

    # 4. Проверяем, что все ссылки отображаются
    for link in links:
        assert link.is_displayed(), f"Ссылка не отображается: {link.text}"

    # 5. Проверяем, что текст первой ссылки содержит "1"
    assert "1" in links[0].text, f"Текст первой ссылки: {links[0].text}"

    driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_session_storage_auth():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # Данные реальных аккаунтов (не коммитьте их в репозиторий!)
    user1_login = "sosiskakiller777"
    user1_session = "Y2ZjMDRjNjAtOTViZS00M2Q4LThlNTQtM2VhOGJkN2IwYzc5"
    user1_csrf = "3ee21233-b20e-4e52-8500-ce4e9f533751"
    user2_login = "kapusta07"
    user2_session = "NmRjZDkwZGEtZTk0NC00YWYyLTlhYjYtY2M2MDY2NmRhODlk"
    user2_csrf = "ed6addc2-d502-4c83-9c91-4e807c5771d8"

    # 1. Откройте страницу https://gitflic.ru/
    driver.get("https://gitflic.ru/")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 2. Установите cookie пользователя 1
    driver.add_cookie({"name": "SESSION", "value": user1_session})
    driver.add_cookie({"name": "X-CSRF-TOKEN", "value": user1_csrf})

    # 3. Обновите страницу
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 4. Перейдите на страницу пользователя 1
    driver.get(f"https://gitflic.ru/user/{user1_login}")
    wait.until(EC.url_contains(user1_login))

    # 5. Сохраните текущий URL
    user1_url = driver.current_url

    # 6. Разлогиньтесь (очистите куки)
    driver.delete_all_cookies()

    # 7. Установите cookie пользователя 2
    driver.add_cookie({"name": "SESSION", "value": user2_session})
    driver.add_cookie({"name": "X-CSRF-TOKEN", "value": user2_csrf})

    # 8. Обновите страницу
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 9. Перейдите на страницу пользователя 2
    driver.get(f"https://gitflic.ru/user/{user2_login}")
    wait.until(EC.url_contains(user2_login))

    # 10. Сохраните текущий URL
    user2_url = driver.current_url

    # 11. Проверьте, что URL пользователей различаются
    assert user1_url != user2_url, (
        f"URL совпадают: {user1_url} и {user2_url}"
    )

    driver.quit()
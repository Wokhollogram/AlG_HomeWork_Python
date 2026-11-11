from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_shop():
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)

    # 1. Открываем сайт магазина в Firefox
    driver.get("https://www.saucedemo.com/")

    # 2. Авторизуемся как standard_user
    wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # 3. Добавляем товары в корзину
    items = [
        "add-to-cart-sauce-labs-backpack",
        "add-to-cart-sauce-labs-bolt-t-shirt",
        "add-to-cart-sauce-labs-onesie",
    ]
    for item in items:
        wait.until(EC.element_to_be_clickable((By.ID, item))).click()

    # 4. Переходим в корзину
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # 5. Нажимаем Checkout
    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # 6. Заполняем форму своими данными
    wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    ).send_keys("Иван")
    driver.find_element(By.ID, "last-name").send_keys("Петров")
    driver.find_element(By.ID, "postal-code").send_keys("101000")

    # 7. Нажимаем кнопку Continue
    driver.find_element(By.ID, "continue").click()

    # 8. Читаем итоговую стоимость (Total)
    total_text = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".summary_total_label")
        )
    ).text

    # 9. Закрываем браузер
    driver.quit()

    # 10. Проверяем, что итоговая сумма равна $58.29
    assert total_text == "Total: $58.29", (
        f"Ожидалась сумма $58.29, получено: {total_text}"
    )
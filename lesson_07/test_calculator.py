import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    """Page Object страницы Slow calculator."""

    URL = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"

    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    SCREEN = (By.CSS_SELECTOR, ".screen")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Открывает страницу калькулятора."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.DELAY_INPUT))

    def set_delay(self, seconds):
        """Вводит значение в поле задержки."""
        delay_input = self.wait.until(
            EC.visibility_of_element_located(self.DELAY_INPUT)
        )
        delay_input.clear()
        delay_input.send_keys(str(seconds))

    def click_button(self, label):
        """Нажимает кнопку калькулятора (цифра, оператор или =)."""
        button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[text()='{label}']")
            )
        )
        button.click()

    def press(self, *labels):
        """Последовательно нажимает несколько кнопок."""
        for label in labels:
            self.click_button(label)

    def wait_for_result(self, expected, timeout):
        """Ждёт, пока на экране появится ожидаемый результат."""
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(self.SCREEN, expected)
        )

    def get_result(self):
        """Возвращает текст с экрана калькулятора."""
        return self.driver.find_element(*self.SCREEN).text


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_slow_calculator(driver):
    calculator = CalculatorPage(driver)

    # Открываем страницу калькулятора
    calculator.open()

    # Вводим значение 45 в поле задержки
    calculator.set_delay(45)

    # Нажимаем кнопки: 7, +, 8, =
    calculator.press("7", "+", "8", "=")

    # Проверяем, что результат 15 отобразится через 45 секунд
    calculator.wait_for_result("15", timeout=50)
    assert calculator.get_result() == "15"
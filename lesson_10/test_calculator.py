from collections.abc import Generator

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    """Page Object страницы Slow calculator."""

    URL: str = (
        "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
    )

    DELAY_INPUT: tuple[str, str] = (By.CSS_SELECTOR, "#delay")
    SCREEN: tuple[str, str] = (By.CSS_SELECTOR, ".screen")

    def __init__(self, driver: WebDriver) -> None:
        """Создаёт страницу.

        Args:
            driver (WebDriver): драйвер браузера.

        Returns:
            None
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self) -> None:
        """Открывает страницу калькулятора и ждёт поле задержки.

        Returns:
            None
        """
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.DELAY_INPUT))

    def set_delay(self, seconds: int) -> None:
        """Вводит значение в поле задержки.

        Args:
            seconds (int): задержка вычисления в секундах.

        Returns:
            None
        """
        delay_input = self.wait.until(
            EC.visibility_of_element_located(self.DELAY_INPUT)
        )
        delay_input.clear()
        delay_input.send_keys(str(seconds))

    def click_button(self, label: str) -> None:
        """Нажимает кнопку калькулятора (цифра, оператор или =).

        Args:
            label (str): текст на кнопке, например "7", "+" или "=".

        Returns:
            None
        """
        button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[text()='{label}']")
            )
        )
        button.click()

    def press(self, *labels: str) -> None:
        """Последовательно нажимает несколько кнопок.

        Args:
            *labels (str): тексты кнопок в порядке нажатия.

        Returns:
            None
        """
        for label in labels:
            self.click_button(label)

    def wait_for_result(self, expected: str, timeout: int) -> None:
        """Ждёт, пока на экране появится ожидаемый результат.

        Args:
            expected (str): текст, который должен появиться на экране.
            timeout (int): максимальное время ожидания в секундах.

        Returns:
            None
        """
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(self.SCREEN, expected)
        )

    def get_result(self) -> str:
        """Возвращает текст с экрана калькулятора.

        Returns:
            str: текущий текст на экране.
        """
        return self.driver.find_element(*self.SCREEN).text


@pytest.fixture
def driver() -> Generator[WebDriver, None, None]:
    """Запускает Chrome и закрывает его после теста.

    Yields:
        WebDriver: драйвер браузера Google Chrome.
    """
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@allure.feature("Калькулятор")
@allure.title("Сложение 7 + 8 с задержкой 45 секунд")
@allure.description(
    "Открываем медленный калькулятор, задаём задержку 45 секунд, "
    "вводим 7 + 8 и проверяем, что через 45 секунд результат равен 15."
)
@allure.severity(allure.severity_level.NORMAL)
def test_slow_calculator(driver: WebDriver) -> None:
    """Проверяет сложение на странице Slow calculator."""
    calculator = CalculatorPage(driver)

    with allure.step("Открыть страницу калькулятора"):
        calculator.open()

    with allure.step("Ввести значение 45 в поле задержки"):
        calculator.set_delay(45)

    with allure.step("Нажать кнопки: 7, +, 8, ="):
        calculator.press("7", "+", "8", "=")

    with allure.step("Дождаться результата (до 50 секунд)"):
        calculator.wait_for_result("15", timeout=50)

    with allure.step("Проверить, что на экране отображается результат 15"):
        assert calculator.get_result() == "15"

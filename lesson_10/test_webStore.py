import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PRODUCTS: list[str] = [
    "Sauce Labs Backpack",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Onesie",
]


class LoginPage:
    """Страница авторизации."""

    URL: str = "https://www.saucedemo.com/"

    USERNAME: tuple[str, str] = (By.ID, "user-name")
    PASSWORD: tuple[str, str] = (By.ID, "password")
    LOGIN_BUTTON: tuple[str, str] = (By.ID, "login-button")

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
        """Открывает страницу авторизации и ждёт поле логина.

        Returns:
            None
        """
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))

    def enter_username(self, username: str) -> None:
        """Вводит логин.

        Args:
            username (str): имя пользователя.

        Returns:
            None
        """
        self.driver.find_element(*self.USERNAME).send_keys(username)

    def enter_password(self, password: str) -> None:
        """Вводит пароль.

        Args:
            password (str): пароль пользователя.

        Returns:
            None
        """
        self.driver.find_element(*self.PASSWORD).send_keys(password)

    def click_login(self) -> None:
        """Нажимает кнопку входа.

        Returns:
            None
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login(self, username: str, password: str) -> None:
        """Вводит логин и пароль и нажимает кнопку входа.

        Args:
            username (str): имя пользователя.
            password (str): пароль пользователя.

        Returns:
            None
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()


class MainPage:
    """Главная страница магазина (список товаров)."""

    CART_LINK: tuple[str, str] = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver: WebDriver) -> None:
        """Создаёт страницу.

        Args:
            driver (WebDriver): драйвер браузера.

        Returns:
            None
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @staticmethod
    def _add_button_locator(product_name: str) -> tuple[str, str]:
        """Формирует локатор кнопки добавления товара в корзину.

        Например, "Sauce Labs Backpack" превращается в
        "add-to-cart-sauce-labs-backpack".

        Args:
            product_name (str): название товара.

        Returns:
            tuple[str, str]: пара (способ поиска, значение локатора).
        """
        slug = product_name.lower().replace(" ", "-")
        return (By.ID, f"add-to-cart-{slug}")

    def add_to_cart(self, product_name: str) -> None:
        """Добавляет товар в корзину по его названию.

        Args:
            product_name (str): название товара.

        Returns:
            None
        """
        button = self.wait.until(
            EC.element_to_be_clickable(self._add_button_locator(product_name))
        )
        button.click()

    def add_products(self, *product_names: str) -> None:
        """Добавляет в корзину несколько товаров.

        Args:
            *product_names (str): названия товаров.

        Returns:
            None
        """
        for name in product_names:
            self.add_to_cart(name)

    def go_to_cart(self) -> None:
        """Переходит в корзину.

        Returns:
            None
        """
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()


class CartPage:
    """Страница корзины."""

    ITEM_NAMES: tuple[str, str] = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON: tuple[str, str] = (By.ID, "checkout")

    def __init__(self, driver: WebDriver) -> None:
        """Создаёт страницу.

        Args:
            driver (WebDriver): драйвер браузера.

        Returns:
            None
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_item_names(self) -> list[str]:
        """Возвращает названия товаров, лежащих в корзине.

        Returns:
            list[str]: список названий товаров.
        """
        items = self.wait.until(
            EC.visibility_of_all_elements_located(self.ITEM_NAMES)
        )
        return [item.text for item in items]

    def has_items(self, *product_names: str) -> bool:
        """Проверяет, что в корзине ровно указанные товары.

        Args:
            *product_names (str): ожидаемые названия товаров.

        Returns:
            bool: True, если состав корзины совпадает с ожидаемым.
        """
        return sorted(self.get_item_names()) == sorted(product_names)

    def click_checkout(self) -> None:
        """Нажимает кнопку Checkout.

        Returns:
            None
        """
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()


class CheckoutPage:
    """Страницы оформления заказа (данные покупателя и итог)."""

    FIRST_NAME: tuple[str, str] = (By.ID, "first-name")
    LAST_NAME: tuple[str, str] = (By.ID, "last-name")
    POSTAL_CODE: tuple[str, str] = (By.ID, "postal-code")
    CONTINUE_BUTTON: tuple[str, str] = (By.ID, "continue")
    TOTAL_LABEL: tuple[str, str] = (By.CSS_SELECTOR, ".summary_total_label")

    def __init__(self, driver: WebDriver) -> None:
        """Создаёт страницу.

        Args:
            driver (WebDriver): драйвер браузера.

        Returns:
            None
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_form(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        """Заполняет форму данными покупателя.

        Args:
            first_name (str): имя.
            last_name (str): фамилия.
            postal_code (str): почтовый индекс.

        Returns:
            None
        """
        self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME)
        ).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal_code)

    def click_continue(self) -> None:
        """Нажимает кнопку Continue.

        Returns:
            None
        """
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def get_total(self) -> str:
        """Возвращает итоговую стоимость, например '$58.29'.

        Returns:
            str: итоговая сумма заказа без префикса "Total: ".
        """
        label = self.wait.until(
            EC.visibility_of_element_located(self.TOTAL_LABEL)
        )
        return label.text.replace("Total: ", "")


@allure.feature("Интернет-магазин")
@allure.title("Покупка трёх товаров в магазине Sauce Demo")
@allure.description(
    "Авторизуемся как standard_user, добавляем в корзину рюкзак, футболку "
    "и боди, оформляем заказ и проверяем, что итоговая сумма равна $58.29."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_shop() -> None:
    """Проверяет оформление заказа в магазине Sauce Demo."""
    driver = webdriver.Firefox()

    with allure.step("Открыть сайт магазина и авторизоваться"):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

    with allure.step("Добавить товары в корзину и перейти в корзину"):
        main_page = MainPage(driver)
        main_page.add_products(*PRODUCTS)
        main_page.go_to_cart()

    with allure.step("Проверить содержимое корзины"):
        cart_page = CartPage(driver)
        assert cart_page.has_items(*PRODUCTS)

    with allure.step("Нажать Checkout"):
        cart_page.click_checkout()

    with allure.step("Заполнить форму данными покупателя и продолжить"):
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_form("Иван", "Петров", "101000")
        checkout_page.click_continue()

    with allure.step("Прочитать итоговую стоимость (Total)"):
        total = checkout_page.get_total()

    with allure.step("Закрыть браузер"):
        driver.quit()

    with allure.step("Проверить, что итоговая сумма равна $58.29"):
        assert total == "$58.29", (
            f"Ожидалась сумма $58.29, получено: {total}"
        )

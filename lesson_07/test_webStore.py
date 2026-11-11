from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Onesie",
]


class LoginPage:
    """Страница авторизации."""

    URL = "https://www.saucedemo.com/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))

    def enter_username(self, username):
        self.driver.find_element(*self.USERNAME).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()


class MainPage:
    """Главная страница магазина (список товаров)."""

    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @staticmethod
    def _add_button_locator(product_name):
        # "Sauce Labs Backpack" -> "add-to-cart-sauce-labs-backpack"
        slug = product_name.lower().replace(" ", "-")
        return (By.ID, f"add-to-cart-{slug}")

    def add_to_cart(self, product_name):
        """Добавляет товар в корзину по его названию."""
        button = self.wait.until(
            EC.element_to_be_clickable(self._add_button_locator(product_name))
        )
        button.click()

    def add_products(self, *product_names):
        for name in product_names:
            self.add_to_cart(name)

    def go_to_cart(self):
        """Переходит в корзину."""
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()


class CartPage:
    """Страница корзины."""

    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_item_names(self):
        """Возвращает названия товаров, лежащих в корзине."""
        items = self.wait.until(
            EC.visibility_of_all_elements_located(self.ITEM_NAMES)
        )
        return [item.text for item in items]

    def has_items(self, *product_names):
        """Проверяет, что в корзине ровно указанные товары."""
        return sorted(self.get_item_names()) == sorted(product_names)

    def click_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()


class CheckoutPage:
    """Страницы оформления заказа (данные покупателя и итог)."""

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_total_label")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_form(self, first_name, last_name, postal_code):
        """Заполняет форму данными покупателя."""
        self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME)
        ).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal_code)

    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def get_total(self):
        """Возвращает итоговую стоимость, например '$58.29'."""
        label = self.wait.until(
            EC.visibility_of_element_located(self.TOTAL_LABEL)
        )
        return label.text.replace("Total: ", "")


def test_shop():
    driver = webdriver.Firefox()

    # Открываем сайт магазина и авторизуемся как standard_user
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    # Добавляем товары в корзину и переходим в корзину
    main_page = MainPage(driver)
    main_page.add_products(*PRODUCTS)
    main_page.go_to_cart()

    # Проверяем содержимое корзины и нажимаем Checkout
    cart_page = CartPage(driver)
    assert cart_page.has_items(*PRODUCTS)
    cart_page.click_checkout()

    # Заполняем форму своими данными и читаем итоговую стоимость
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_form("Иван", "Петров", "101000")
    checkout_page.click_continue()
    total = checkout_page.get_total()

    # Закрываем браузер
    driver.quit()

    # Проверяем, что итоговая сумма равна $58.29
    assert total == "$58.29", f"Ожидалась сумма $58.29, получено: {total}"
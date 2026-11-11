import pytest
from string_utils import StringUtils


class TestStringUtils:
    """
    Тесты для класса StringUtils.

    Используется фикстура autouse=True, которая создаёт свежий
    экземпляр класса перед каждым тестом — это гарантирует изоляцию
    тестов друг от друга.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.string_utils = StringUtils()

    # ==================================================================
    # capitalize
    # ==================================================================

    @pytest.mark.positive
    @pytest.mark.parametrize("input_str, expected", [
        ("skypro", "Skypro"),           # пример из документации
        ("hello world", "Hello world"),  # фраза с пробелом
        ("python", "Python"),
        ("a", "A"),                      # граничное: строка из 1 символа
    ])
    def test_capitalize_positive(self, input_str, expected):
        assert self.string_utils.capitalize(input_str) == expected

    @pytest.mark.negative
    @pytest.mark.parametrize("input_str, expected", [
        ("123abc", "123abc"),            # начинается с цифры
        ("", ""),                        # граничное: пустая строка
        ("   ", "   "),                  # только пробелы
        ("!hello", "!hello"),            # начинается со знака
        ("HELLO", "Hello"),              # регистр остальных букв понижается
    ])
    def test_capitalize_negative(self, input_str, expected):
        assert self.string_utils.capitalize(input_str) == expected

    @pytest.mark.negative
    def test_capitalize_none_raises(self):
        """None — не строка, ожидаем AttributeError."""
        with pytest.raises(AttributeError):
            self.string_utils.capitalize(None)

    # ==================================================================
    # trim
    # ==================================================================

    @pytest.mark.positive
    @pytest.mark.parametrize("input_str, expected", [
        ("   skypro", "skypro"),             # пример из документации
        ("skypro", "skypro"),                # пробелов нет
        (" skypro", "skypro"),               # один пробел
        ("     skypro", "skypro"),           # много пробелов
        ("   skypro   ", "skypro   "),       # пробелы в конце сохраняются
        ("   hello world", "hello world"),   # пробел внутри сохраняется
    ])
    def test_trim_positive(self, input_str, expected):
        assert self.string_utils.trim(input_str) == expected

    @pytest.mark.negative
    @pytest.mark.parametrize("input_str, expected", [
        ("", ""),                            # граничное: пустая строка
        ("   ", ""),                         # только пробелы
        ("\tskypro", "\tskypro"),            # таб не удаляется
        ("\nskypro", "\nskypro"),            # перевод строки не удаляется
    ])
    def test_trim_negative(self, input_str, expected):
        assert self.string_utils.trim(input_str) == expected

    @pytest.mark.negative
    def test_trim_none_raises(self):
        """None — не строка, ожидаем AttributeError."""
        with pytest.raises(AttributeError):
            self.string_utils.trim(None)

    # ==================================================================
    # contains
    # ==================================================================

    @pytest.mark.positive
    @pytest.mark.parametrize("string, symbol, expected", [
        ("SkyPro", "S", True),               # пример 1 из документации
        ("SkyPro", "k", True),               # символ в середине
        ("SkyPro", "o", True),               # символ в конце
        ("SkyPro", "Sky", True),             # подстрока в начале
        ("SkyPro", "Pro", True),             # подстрока в конце
        ("SkyPro", "SkyPro", True),          # вся строка целиком
    ])
    def test_contains_positive(self, string, symbol, expected):
        assert self.string_utils.contains(string, symbol) is expected

    @pytest.mark.negative
    @pytest.mark.parametrize("string, symbol, expected", [
        ("SkyPro", "U", False),              # пример 2 из документации
        ("SkyPro", "s", False),              # регистрозависимость
        ("SkyPro", "x", False),              # символа нет
        ("SkyPro", "SkyPro!", False),        # подстрока длиннее строки
    ])
    def test_contains_negative(self, string, symbol, expected):
        assert self.string_utils.contains(string, symbol) is expected

    @pytest.mark.negative
    @pytest.mark.parametrize("string, symbol, expected", [
        ("", "", True),                      # пустая строка содержит пустую подстроку
        ("SkyPro", "", True),                # пустая подстрока всегда находится
        ("", "S", False),                    # в пустой строке нечего искать
    ])
    def test_contains_edge_cases(self, string, symbol, expected):
        """Граничные случаи — ожидаемое поведение зафиксировано как есть."""
        assert self.string_utils.contains(string, symbol) is expected

    # ==================================================================
    # delete_symbol
    # ==================================================================

    @pytest.mark.positive
    @pytest.mark.parametrize("string, symbol, expected", [
        ("SkyPro", "k", "SyPro"),            # пример 1 из документации
        ("SkyPro", "Pro", "Sky"),            # пример 2 из документации
        ("aaa", "a", ""),                    # удаляются все вхождения
        ("banana", "na", "ba"),              # повторяющаяся подстрока
        ("SkyPro", "SkyPro", ""),            # удаляется вся строка
    ])
    def test_delete_symbol_positive(self, string, symbol, expected):
        assert self.string_utils.delete_symbol(string, symbol) == expected

    @pytest.mark.negative
    @pytest.mark.parametrize("string, symbol, expected", [
        ("SkyPro", "U", "SkyPro"),           # символа нет — строка не меняется
        ("SkyPro", "s", "SkyPro"),           # регистрозависимость
        ("", "a", ""),                       # граничное: пустая строка
        ("SkyPro", "", "SkyPro"),            # пустая подстрока — строка не меняется
    ])
    def test_delete_symbol_negative(self, string, symbol, expected):
        assert self.string_utils.delete_symbol(string, symbol) == expected

    @pytest.mark.negative
    def test_delete_symbol_none_raises(self):
        """None — не строка, ожидаем AttributeError."""
        with pytest.raises(AttributeError):
            self.string_utils.delete_symbol(None, "a")
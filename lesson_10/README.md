# Автотесты UI с Allure

Проект содержит два UI-автотеста на Selenium и pytest. Тесты оформлены по паттерну **Page Object**, а результаты формируются в виде отчёта **Allure**.

## Тесты

| Файл | Что проверяет | Браузер |
|------|---------------|---------|
| `test_calculator.py` | Медленный калькулятор: `7 + 8 = 15` при задержке 45 секунд | Google Chrome |
| `test_webStore.py` | Магазин Sauce Demo: покупка трёх товаров, итоговая сумма `$58.29` | Mozilla Firefox |

> Тест калькулятора идёт больше 45 секунд, это нормально: так задумано заданием.

## Что нужно для работы

- Python 3.12 или новее
- Браузеры **Google Chrome** и **Mozilla Firefox**
- Java (нужна для командной строки Allure)
- Allure Commandline

## Установка

1. Склонируйте репозиторий и перейдите в папку проекта.
2. Установите зависимости:

   ```
   pip install -r requirements.txt
   ```

   В файле перечислены `pytest`, `selenium` и `allure-pytest`. Драйверы браузеров Selenium скачивает сам.

3. Установите Allure Commandline одним из способов:

   - через Scoop (Windows): `scoop install allure`;
   - через npm: `npm install -g allure-commandline`;
   - вручную: скачайте архив с [страницы релизов Allure](https://github.com/allure-framework/allure2/releases), распакуйте и добавьте папку `bin` в переменную `PATH`.

   Проверить установку можно командой `allure --version`.

## Запуск тестов и формирование результатов

Из корня проекта выполните:

```
pytest --alluredir=allure-results
```

Результаты прогона сохранятся в папке `allure-results`. Чтобы перед запуском очистить старые результаты, добавьте ключ `--clean-alluredir`:

```
pytest --alluredir=allure-results --clean-alluredir
```

Запустить только один тест можно так:

```
pytest test_calculator.py --alluredir=allure-results
```

## Как посмотреть отчёт

**Вариант 1. Быстрый просмотр.** Команда сама соберёт отчёт во временную папку и откроет его в браузере:

```
allure serve allure-results
```

**Вариант 2. Сохранить отчёт в папку.** Соберите отчёт в `allure-report` и откройте его:

```
allure generate allure-results -o allure-report --clean
allure open allure-report
```

> Файл `allure-report/index.html` не стоит открывать двойным щелчком: в браузере он не загрузит данные. Используйте `allure open` или `allure serve`.

## Структура проекта

```
.
├── allure-report/        # собранный отчёт (в git только пустая папка)
├── allure-results/       # результаты прогона (в git только пустая папка)
├── test_calculator.py    # Page Object и тест калькулятора
├── test_webStore.py      # Page Object и тест интернет-магазина
├── requirements.txt      # зависимости
├── .gitignore
└── README.md
```

Папки `allure-results` и `allure-report` добавлены в `.gitignore`, их содержимое в репозиторий не попадает.

## Разметка Allure

- Шаги и проверки в тестах размечены через `with allure.step("...")`.
- Каждый тест имеет декораторы `@allure.title`, `@allure.description`, `@allure.feature` и `@allure.severity`.
- Методы Page-классов описаны в docstring с указанием типов параметров и возвращаемых значений.

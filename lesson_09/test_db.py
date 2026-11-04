import os
import uuid

import pytest
from sqlalchemy import MetaData, Table, create_engine, delete, insert
from sqlalchemy import select, update

# Строка подключения. Впишите свои данные вместо myuser, mypassword,
# mydatabase (или задайте переменную окружения DATABASE_URL).
# Драйвер psycopg2 указан явно (postgresql+psycopg2), так как новые
# версии SQLAlchemy по умолчанию могут искать драйвер psycopg 3.
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydatabase",
)

# Таблица и столбцы, с которыми работают тесты.
TABLE_NAME = "subject"
ID_COLUMN = "subject_id"
TITLE_COLUMN = "subject_title"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(DB_URL)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def table(engine):
    """Описание таблицы, считанное из БД."""
    return Table(TABLE_NAME, MetaData(), autoload_with=engine)


@pytest.fixture
def created_ids(engine, table):
    """Список id созданных в тесте строк.

    После теста все они удаляются из БД, даже если тест упал.
    """
    ids = []
    yield ids
    with engine.begin() as conn:
        for row_id in ids:
            conn.execute(delete(table).where(table.c[ID_COLUMN] == row_id))


def unique_title():
    """Уникальное значение, чтобы повторные запуски не конфликтовали."""
    return f"autotest-{uuid.uuid4()}"


def add_row(engine, table, created_ids, title):
    """Добавляет строку и возвращает её id."""
    with engine.begin() as conn:
        result = conn.execute(
            insert(table)
            .values({TITLE_COLUMN: title})
            .returning(table.c[ID_COLUMN])
        )
        row_id = result.scalar_one()
    created_ids.append(row_id)
    return row_id


def get_row(engine, table, row_id):
    """Возвращает строку по id или None, если её нет."""
    with engine.connect() as conn:
        return conn.execute(
            select(table).where(table.c[ID_COLUMN] == row_id)
        ).mappings().first()


def test_add_subject(engine, table, created_ids):
    title = unique_title()

    row_id = add_row(engine, table, created_ids, title)

    row = get_row(engine, table, row_id)
    assert row is not None
    assert row[TITLE_COLUMN] == title


def test_update_subject(engine, table, created_ids):
    row_id = add_row(engine, table, created_ids, unique_title())
    new_title = unique_title()

    with engine.begin() as conn:
        conn.execute(
            update(table)
            .where(table.c[ID_COLUMN] == row_id)
            .values({TITLE_COLUMN: new_title})
        )

    row = get_row(engine, table, row_id)
    assert row[TITLE_COLUMN] == new_title


def test_delete_subject(engine, table, created_ids):
    row_id = add_row(engine, table, created_ids, unique_title())

    with engine.begin() as conn:
        conn.execute(delete(table).where(table.c[ID_COLUMN] == row_id))

    assert get_row(engine, table, row_id) is None
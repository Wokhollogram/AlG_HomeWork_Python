import os
import uuid

import pytest
import requests

# Данные для авторизации берутся из переменных окружения,
# в коде токена нет.
BASE_URL = os.getenv("YOUGILE_BASE_URL", "https://yougile.com/api-v2")
API_KEY = os.getenv("YOUGILE_API_KEY")
TIMEOUT = 10


class ProjectsApi:
    """Обёртка над методами проектов Yougile (/api-v2/projects)."""

    def __init__(self, base_url, api_key):
        self.url = f"{base_url}/projects"
        self.api_key = api_key

    def _headers(self, api_key=None):
        token = self.api_key if api_key is None else api_key
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def create(self, payload, api_key=None):
        """[POST] /projects"""
        return requests.post(
            self.url,
            json=payload,
            headers=self._headers(api_key),
            timeout=TIMEOUT,
        )

    def update(self, project_id, payload):
        """[PUT] /projects/{id}"""
        return requests.put(
            f"{self.url}/{project_id}",
            json=payload,
            headers=self._headers(),
            timeout=TIMEOUT,
        )

    def get(self, project_id):
        """[GET] /projects/{id}"""
        return requests.get(
            f"{self.url}/{project_id}",
            headers=self._headers(),
            timeout=TIMEOUT,
        )


def unique_title():
    """Уникальное название, чтобы повторные запуски не конфликтовали."""
    return f"autotest-{uuid.uuid4()}"


@pytest.fixture(scope="session")
def api():
    if not API_KEY:
        pytest.fail(
            "Не задана переменная окружения YOUGILE_API_KEY "
            "(API-ключ Yougile)"
        )
    return ProjectsApi(BASE_URL, API_KEY)


@pytest.fixture
def created_projects(api):
    """Список id созданных в тесте проектов.

    Проекты в Yougile нельзя удалить методом DELETE, поэтому после
    теста они помечаются как удалённые (PUT с deleted=true).
    """
    ids = []
    yield ids
    for project_id in ids:
        api.update(project_id, {"deleted": True})


@pytest.fixture
def project(api, created_projects):
    """Готовый проект для тестов PUT и GET."""
    title = unique_title()
    response = api.create({"title": title})
    assert response.status_code == 201
    project_id = response.json()["id"]
    created_projects.append(project_id)
    return {"id": project_id, "title": title}


# ---------- [POST] /projects ----------
def test_create_project_positive(api, created_projects):
    title = unique_title()

    response = api.create({"title": title})

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    created_projects.append(body["id"])


def test_create_project_without_title_negative(api):
    # title - обязательное поле
    response = api.create({})

    assert response.status_code == 400


def test_create_project_invalid_token_negative(api):
    response = api.create({"title": unique_title()}, api_key="invalid-key")

    assert response.status_code == 401


# ---------- [PUT] /projects/{id} ----------
def test_update_project_positive(api, project):
    new_title = unique_title()

    response = api.update(project["id"], {"title": new_title})

    assert response.status_code == 200
    assert response.json()["id"] == project["id"]
    # Убеждаемся, что название действительно изменилось
    assert api.get(project["id"]).json()["title"] == new_title


def test_update_project_not_found_negative(api):
    unknown_id = str(uuid.uuid4())

    response = api.update(unknown_id, {"title": unique_title()})

    assert response.status_code == 404


# ---------- [GET] /projects/{id} ----------
def test_get_project_positive(api, project):
    response = api.get(project["id"])

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == project["id"]
    assert body["title"] == project["title"]


def test_get_project_not_found_negative(api):
    unknown_id = str(uuid.uuid4())

    response = api.get(unknown_id)

    assert response.status_code == 404
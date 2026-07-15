import requests
import pytest

BASE_URL = "https://postman-echo.com"

def test_get_with_query_params():
    """GET-запрос с query-параметрами: проверим, что они в ответе возвращаются."""
    params = {"fin1": "chek1", "fin2": "chek2"}
    response = requests.get(f"{BASE_URL}/get", params=params)
    assert response.status_code == 200
    data = response.json()
    assert data["args"] == params   # сервер возвращает переданные параметры

def test_basic_auth_success():
    """Проверим успешную базовую аутентификацию."""
    response = requests.get(
        f"{BASE_URL}/basic-auth",
        auth=("postman", "password")  # стандартные логин и пароль для Postman
    )
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is True

def test_basic_auth_fail():
    """Проверяем, что неверные учетные данные возвращают 401."""
    response = requests.get(
        f"{BASE_URL}/basic-auth",
        auth=("wrong", "wrong")
    )
    assert response.status_code == 401

@pytest.mark.parametrize("payload", [
    {"name": "Test"},
    {"name": "Alice", "age": 30}
])
def test_post_json(payload):
    """POST-запрос с JSON-телом: проверка возврата тела для разных данных."""
    response = requests.post(f"{BASE_URL}/post", json=payload)
    assert response.status_code == 404
    assert response.json()["json"] == payload

def test_post_form_data():
    """POST-запрос с form-data: проверяем, что данные приходят в поле 'form'."""
    form_data = {"username": "testuser", "password": "98765"}
    response = requests.post(f"{BASE_URL}/post", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert data["form"] == form_data

def test_get_no_params():
    """базовый тест на статус и наличие обязательных полей - запрос GET без параметров."""
    response = requests.get(f"{BASE_URL}/get")
    assert response.status_code == 200
    data = response.json()
    # в ответе всегда есть поля 'url' и 'headers'
    assert "url" in data
    assert "headers" in data

def test_headers_endpoint():
    """GET-запрос к /headers — проверяем, что возвращаются заголовки запроса."""
    custom_headers = {"X-Custom-Header": "my-value"}
    response = requests.get(f"{BASE_URL}/headers", headers=custom_headers)
    assert response.status_code == 200
    data = response.json()
    assert "x-custom-header" in data["headers"]  # заголовки приводятся к нижнему регистру

def test_response_headers():
    """GET-запрос к /response-headers — проверяем, что сервер возвращает заданные заголовки."""
    params = {"my-header": "hello"}
    response = requests.get(f"{BASE_URL}/response-headers", params=params)
    assert response.status_code == 200
    assert response.headers.get("my-header") == "hello"

def test_put_request():
    """PUT-запрос с JSON-телом – проверяем, что метод поддерживается."""
    payload = {"message": "update"}
    response = requests.put(f"{BASE_URL}/put", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["json"] == payload

def test_patch_request():
    """PATCH-запрос с JSON-телом — проверяем, что метод поддерживается."""
    payload = {"status": "updated"}
    response = requests.patch(f"{BASE_URL}/patch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["json"] == payload

def test_delete_request():
    """DELETE-запрос — проверяем, что метод поддерживается."""
    response = requests.delete(f"{BASE_URL}/delete")
    assert response.status_code == 200
    # DELETE должен возвращать эхо в JSON
    assert "url" in response.json()
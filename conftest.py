import pytest
import requests
from data import Url
from generators import generate_user_data


@pytest.fixture
def create_user():
    """Создаёт нового пользователя перед тестом и удаляет после теста"""
    user_data = generate_user_data()

    # Регистрируем пользователя
    create_response = requests.post(f"{Url.BASE_URL}{Url.USER_CREATE}", json=user_data)
    access_token = create_response.json().get("accessToken")

    # Возвращаем данные в тест
    yield {
        "user_data": user_data,
        "access_token": access_token
    }

    # Удаляем пользователя после теста (если токен получен)
    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(f"{Url.BASE_URL}{Url.USER_DELETE}", headers=headers)
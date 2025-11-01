import pytest
import requests
from data import Url, UserEndpoints
from generators import generate_user_data


@pytest.fixture
def create_user():
    """Создаёт нового пользователя перед тестом и удаляет после теста"""
    user_data = generate_user_data()
    create_response = requests.post(f"{Url.BASE_URL}{UserEndpoints.USER_CREATE}", json=user_data)
    access_token = create_response.json().get("accessToken")

    yield {"user_data": user_data, "access_token": access_token}

    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(f"{Url.BASE_URL}{UserEndpoints.USER_DELETE}", headers=headers)
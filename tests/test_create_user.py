import requests
import pytest
import allure
from data import Url, ResponseMessages
from generators import generate_user_data, generate_incomplete_user_data


@allure.epic("Пользователи")
@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self, create_user):
        """
        Проверяет, что можно создать нового пользователя.
        Фикстура create_user создаёт пользователя и удаляет его после теста.
        """
        response = requests.post(f"{Url.BASE_URL}{Url.USER_LOGIN}", json={
            "email": create_user["user_data"]["email"],
            "password": create_user["user_data"]["password"]
        })

        assert response.status_code == 200, f"Неверный статус-код: {response.status_code}"
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert body["user"]["email"] == create_user["user_data"]["email"]

    @allure.title("Ошибка при создании пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, create_user):
        """
        Проверяет, что нельзя зарегистрировать уже существующего пользователя.
        """
        existing_user = create_user["user_data"]
        duplicate = requests.post(f"{Url.BASE_URL}{Url.USER_CREATE}", json=existing_user)

        assert duplicate.status_code == 403
        body = duplicate.json()
        assert body["success"] is False
        assert body["message"] == ResponseMessages.USER_ALREADY_EXISTS

    @allure.title("Ошибка при создании пользователя без обязательных полей")
    @pytest.mark.parametrize("payload", generate_incomplete_user_data())
    def test_create_user_missing_required_fields(self, payload):
        """
        Проверяет, что при отсутствии одного из обязательных полей
        возвращается ошибка 403 с корректным сообщением.
        """
        response = requests.post(f"{Url.BASE_URL}{Url.USER_CREATE}", json=payload)

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ResponseMessages.USER_CREATION_NOT_ENOUGH_DATA
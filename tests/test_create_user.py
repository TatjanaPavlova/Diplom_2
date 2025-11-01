import pytest
import requests
import allure
from data import Url, UserEndpoints, ResponseMessages
from generators import generate_incomplete_user_data


@allure.epic("Пользователи")
@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self, create_user):
        user_data = create_user["user_data"]
        with allure.step("Логинимся под новым пользователем"):
            response = requests.post(f"{Url.BASE_URL}{UserEndpoints.USER_LOGIN}", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "accessToken" in body
            assert body["user"]["email"] == user_data["email"]

    @allure.title("Ошибка при создании пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, create_user):
        existing_user = create_user["user_data"]
        with allure.step("Пробуем создать пользователя, который уже существует"):
            duplicate = requests.post(f"{Url.BASE_URL}{UserEndpoints.USER_CREATE}", json=existing_user)
            assert duplicate.status_code == 403
            body = duplicate.json()
            assert body["success"] is False
            assert body["message"] == ResponseMessages.USER_ALREADY_EXISTS

    @allure.title("Ошибка при создании пользователя без обязательных полей")
    @pytest.mark.parametrize("payload", generate_incomplete_user_data())
    def test_create_user_missing_required_fields(self, payload):
        with allure.step(f"Пробуем создать пользователя с неполными данными: {payload}"):
            response = requests.post(f"{Url.BASE_URL}{UserEndpoints.USER_CREATE}", json=payload)
            assert response.status_code == 403
            body = response.json()
            assert body["success"] is False
            assert body["message"] == ResponseMessages.USER_CREATION_NOT_ENOUGH_DATA

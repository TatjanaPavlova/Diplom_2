import requests
import allure
from data import Url, ResponseMessages
from generators import generate_user_data


@allure.epic("Пользователи")
@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Успешная авторизация существующего пользователя")
    def test_login_existing_user(self, create_user):
        user = create_user["user_data"]
        response = requests.post(f"{Url.BASE_URL}{Url.USER_LOGIN}", json=user)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert body["user"]["email"] == user["email"]

    @allure.title("Ошибка при авторизации с неверным логином или паролем")
    def test_login_with_invalid_credentials(self):
        invalid_user = generate_user_data()
        invalid_user["password"] = "wrongpassword123"
        response = requests.post(f"{Url.BASE_URL}{Url.USER_LOGIN}", json=invalid_user)

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ResponseMessages.USER_LOGIN_INVALID_CREDENTIALS

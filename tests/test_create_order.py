import requests
import allure
from data import Url, OrderEndpoints, ResponseMessages


@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_and_valid_ingredients(self, create_user):
        token = create_user["access_token"]
        headers = {"Authorization": token}

        with allure.step("Получаем список ингредиентов"):
            ingredients_response = requests.get(f"{Url.BASE_URL}{OrderEndpoints.INGREDIENTS}")
            ingredients_data = ingredients_response.json()["data"]
            ingredients = [i["_id"] for i in ingredients_data[:2]]

        payload = {"ingredients": ingredients}
        with allure.step("Создаём заказ с авторизацией и валидными ингредиентами"):
            response = requests.post(f"{Url.BASE_URL}{OrderEndpoints.ORDER_CREATE}", json=payload, headers=headers)
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "order" in body
            assert "number" in body["order"]

    @allure.title("Ошибка при создании заказа без авторизации")
    def test_create_order_without_auth(self):
        with allure.step("Получаем список ингредиентов"):
            ingredients_response = requests.get(f"{Url.BASE_URL}{OrderEndpoints.INGREDIENTS}")
            ingredients = [i["_id"] for i in ingredients_response.json()["data"][:2]]

        payload = {"ingredients": ingredients}
        with allure.step("Создаём заказ без авторизации"):
            response = requests.post(f"{Url.BASE_URL}{OrderEndpoints.ORDER_CREATE}", json=payload)
            assert response.status_code == 401
            body = response.json()
            assert body["success"] is False
            assert body["message"] == ResponseMessages.USER_UNAUTHORIZED

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_user):
        token = create_user["access_token"]
        headers = {"Authorization": token}

        with allure.step("Создаём заказ с пустым списком ингредиентов"):
            response = requests.post(
                f"{Url.BASE_URL}{OrderEndpoints.ORDER_CREATE}", json={"ingredients": []}, headers=headers
            )
            assert response.status_code == 400
            body = response.json()
            assert body["success"] is False
            assert body["message"] == ResponseMessages.ORDER_NO_INGREDIENTS

    @allure.title("Создание заказа с невалидным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, create_user):
        token = create_user["access_token"]
        headers = {"Authorization": token}

        payload = {"ingredients": ["invalid_hash_123"]}
        with allure.step("Создаём заказ с невалидным хешем ингредиентов"):
            response = requests.post(f"{Url.BASE_URL}{OrderEndpoints.ORDER_CREATE}", json=payload, headers=headers)
            assert response.status_code == 500


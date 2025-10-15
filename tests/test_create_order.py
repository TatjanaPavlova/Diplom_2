import requests
import allure
from data import Url, ResponseMessages


@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_and_valid_ingredients(self, create_user):
        token = create_user["access_token"]
        headers = {"Authorization": token}

        ingredients_response = requests.get(f"{Url.BASE_URL}{Url.INGREDIENTS}")
        ingredients_data = ingredients_response.json()["data"]
        ingredients = [i["_id"] for i in ingredients_data[:2]]

        payload = {"ingredients": ingredients}
        response = requests.post(f"{Url.BASE_URL}{Url.ORDER_CREATE}", json=payload, headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Ошибка при создании заказа без авторизации")
    def test_create_order_without_auth(self):
        ingredients_response = requests.get(f"{Url.BASE_URL}{Url.INGREDIENTS}")
        ingredients = [i["_id"] for i in ingredients_response.json()["data"][:2]]
        payload = {"ingredients": ingredients}

        response = requests.post(f"{Url.BASE_URL}{Url.ORDER_CREATE}", json=payload)
        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ResponseMessages.USER_UNAUTHORIZED

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_user):
        token = create_user["access_token"]
        headers = {"Authorization": token}

        response = requests.post(f"{Url.BASE_URL}{Url.ORDER_CREATE}", json={"ingredients": []}, headers=headers)
        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ResponseMessages.ORDER_NO_INGREDIENTS

    @allure.title("Создание заказа с невалидным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, create_user):
        token = create_user["access_token"]
        headers = {"Authorization": token}

        payload = {"ingredients": ["invalid_hash_123"]}
        response = requests.post(f"{Url.BASE_URL}{Url.ORDER_CREATE}", json=payload, headers=headers)
        assert response.status_code == 500


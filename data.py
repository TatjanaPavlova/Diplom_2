

class Url:
    BASE_URL = 'https://stellarburgers.education-services.ru' # главная страница Stellar Burgers

    # пользователи
    USER_CREATE = '/api/auth/register' # создание пользователя
    USER_LOGIN = '/api/auth/login' # логин пользователя
    USER_DELETE = '/api/auth/user' # удаление пользователя

    # заказы
    ORDER_CREATE = '/api/orders' # создание заказа
    INGREDIENTS = '/api/ingredients' # получение данных об ингредиентах


class ResponseMessages:
    USER_ALREADY_EXISTS = 'User already exists'
    USER_CREATION_NOT_ENOUGH_DATA = 'Email, password and name are required fields'
    USER_LOGIN_INVALID_CREDENTIALS = 'email or password are incorrect'
    USER_UNAUTHORIZED = 'You should be authorised'
    ORDER_NO_INGREDIENTS = 'Ingredient ids must be provided'
    

class TestUsers:
    INVALID_LOGIN = "wrong@example.com"
    INVALID_PASSWORD = "wrongpassword123"
    # Можно добавить существующего пользователя для тестов
    EXISTING_USER_EMAIL = "existing@example.com"
    EXISTING_USER_PASSWORD = "correctpass"
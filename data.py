

class Url:
    BASE_URL = 'https://stellarburgers.education-services.ru' # главная страница Stellar Burgers
    USER_CREATE = '/api/auth/register' # создание пользователя
    USER_LOGIN = '/api/auth/login' # логин пользователя
    USER_DELETE = '/api/auth/user' #удаление пользователя
    ORDER_CREATE = '/api/orders' # создание заказа


class ResponseMessages:
    USER_ALREADY_EXISTS = 'User already exists'
    USER_CREATION_NOT_ENOUGH_DATA = 'Email, password and name are required fields'
    USER_LOGIN_NOT_ENOUGH_DATA = 'email or password are incorrect'
    ORDER_NO_INGREDIENTS = 'Ingredient ids must be provided'
    
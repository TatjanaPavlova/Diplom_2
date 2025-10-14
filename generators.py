from faker import Faker

fake = Faker()


# Создаёт валидные данные для регистрации нового пользователя
def generate_user_data():
    return {
        "email": fake.email(),
        "password": fake.password(length=10),
        "name": fake.first_name()
    }


# Возвращает список неполных данных для проверки обязательных полей
def generate_incomplete_user_data():
    return [
        {"password": fake.password(length=10), "name": fake.first_name()},   # без email
        {"email": fake.email(), "name": fake.first_name()},                  # без password
        {"email": fake.email(), "password": fake.password(length=10)}        # без name
    ]
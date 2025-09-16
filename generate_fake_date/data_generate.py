from faker import Faker

class FakeDateGen:
    def __init__(self):
        self.fake = Faker('ru_RU')

    """Генерируем имя"""
    def generate_name(self):
        return self.fake.first_name()

    """Генерируем почту"""
    def generate_email(self):
        return self.fake.email()

    """Генерируем пароль"""
    def generate_password(self, length=5):
        return self.fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

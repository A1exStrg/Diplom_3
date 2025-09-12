from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.base_page import BasePage
from generate_fake_date.data_generate import FakeDateGen
from locators import Locators

class LoginPage(BasePage):
    """
    Page Object для формы логина/регистрации/восстановления.
    Здесь — вводы, переключение 'eye', ожидания подтверждений.
    """
    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver, timeout=timeout)
        self.locators = Locators()
        self.data_generator = FakeDateGen()

    """Нажать ссылку 'Восстановить пароль'"""
    def click_recover_password(self):
        self.click_and_wait_element(self.locators.RECOVER_PASS_BUTTON)

    """Нажать поле e-mail"""
    def click_email_field(self):
        self.click_and_wait_element(self.locators.EMAIL_FIELD)

    """Нажать поле пароля"""
    def click_password_field(self):
        self.click_and_wait_element(self.locators.PASSWORD_FIELD)

    """Ввести сгенерированный e-mail в {locator}"""
    def send_email_to_input(self, locator):
        email = self.data_generator.generate_email()
        el = self.driver.find_element(*locator)
        el.clear()
        el.send_keys(email)

    """Ввести e-mail: {email}"""
    def send_email_to_input2(self, email):
        el = self.driver.find_element(*self.locators.EMAIL_FIELD)
        el.clear()
        el.send_keys(email)

    """Ввести сгенерированный пароль в {locator}"""
    def send_password_to_input(self, locator):
        pwd = self.data_generator.generate_password()
        el = self.driver.find_element(*locator)
        el.clear()
        el.send_keys(pwd)

    """Ввести пароль: {password}"""
    def send_password_to_input2(self, password):
        el = self.driver.find_element(*self.locators.PASSWORD_FIELD)
        el.clear()
        el.send_keys(password)

    """Нажать кнопку 'Восстановить'"""
    def click_recover_button(self):
        self.click_and_wait_element(self.locators.RECOVER_BUTTON)

    """Проверить, что пользователь залогинен"""
    def is_logged_in(self) -> bool:
        """Возвращает True, если видна кнопка выхода из аккаунта."""
        try:
            return WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.locators.EXIT_BUTTON)
            ).is_displayed()
        except TimeoutException:
            return False

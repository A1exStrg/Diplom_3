import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.base_page import BasePage
from locators import Locators

class Stellar_burger_page(BasePage):
    """
    Page Object для главной страницы.
    Личный кабинет, конструктор, лента заказов и т.д.
    """
    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver, timeout=timeout)
        self.locators = Locators()

    @allure.step("Клик по кнопке 'Личный кабинет'")
    def click_on_personal_cabinet(self):
        try:
            personal_cabinet_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.locators.PERS_CABINET_BUTTON))
            browser = self.driver.capabilities.get('browserName', '').lower()
            if browser == 'firefox':
                self.driver.execute_script("arguments[0].click();", personal_cabinet_button)
            else:
                personal_cabinet_button.click()
        except TimeoutException:
            pass

    @allure.step("Клик по разделу 'История заказов'")
    def open_order_history(self):
        try:
            history_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.locators.ZAKAZ_HISTORY_BUTTON))
            current_browser = self.driver.capabilities.get('browserName', '').lower()
            if current_browser == 'firefox':
                self.driver.execute_script("arguments[0].click();", history_link)
            else:
                history_link.click()
        except TimeoutException:
            pass

    """Клик по ссылке 'Зарегистрироваться'"""
    def open_register_link(self):
        self.click_and_wait_element(self.locators.REGISTER_LINK)

    """Клик по кнопке 'Зарегистрироваться'"""
    def click_register_button(self):
        try:
            self.driver.find_element(*self.locators.REGISTER_BUTTON).click()
        except Exception:
            print("Кнопка регистрации не найдена")

    """Клик по кнопке 'Войти'"""
    def click_login_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.locators.LOGIN_BUTTON)).click()

    """Клик по разделу 'Лента заказов'"""
    def click_order_lenta(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located((self.locators.MODAL_OVERLAY))
            )
            order_feed_link = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.locators.ORDER_LENTA_BUTTON))
            order_feed_link.click()
        except TimeoutException:
            pass

    """Клик по заказу в ленте"""
    def click_order(self):
            try:
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.locators.ORDER_LINK)).click()
            except TimeoutException:
                print("Заказ не кликабелен")

    """Список заказа не пустой"""
    def test_order_not_empty(self):
        try:
            ul_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.locators.DETAILS_ORDER))
            items = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(self.locators.ELEMENT_ORDER))
            return ul_element.is_displayed() and len(items) > 0
        except TimeoutException:
            return False

    """Клик по разделу 'Конструктор'"""
    def click_constructor(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.locators.CONSTRUCT_BUTTON)).click()

    """Проверка, открыто ли модальное окно заказа"""
    def order_modal_window_is_visible(self):
        return self.driver.find_element(*self.locators.DETAILS_ORDERS).is_displayed()


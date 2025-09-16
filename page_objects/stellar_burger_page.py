import allure
from selenium.common import TimeoutException
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
            # ждём кнопку через универсальный метод
            button = self.wait_for_condition(
                lambda d: EC.element_to_be_clickable(self.locators.PERS_CABINET_BUTTON)(d),
                timeout=10
            )
            # проверяем браузер через BasePage
            if self.get_browser_name() == 'firefox':
                self.js_click(button)
            else:
                button.click()
        except TimeoutException:
            pass

    @allure.step("Клик по разделу 'История заказов'")
    def open_order_history(self):
        try:
            history_link = self.wait_for_condition(
                lambda d: EC.element_to_be_clickable(self.locators.ZAKAZ_HISTORY_BUTTON)(d),
                timeout=10
            )
            if self.get_browser_name() == 'firefox':
                self.js_click(history_link)
            else:
                history_link.click()
        except TimeoutException:
            pass

    @allure.title('Клик по кнопке "Войти"')
    def click_login_button(self):
        try:
            self.click_and_wait_element(self.locators.LOGIN_BUTTON)
        except Exception:
            print("Кнопка 'Войти' не найдена")

    @allure.title('Клик по разделу "Лента заказов"')
    def click_order_lenta(self):
        try:
            self.wait_for_invisibility(self.locators.MODAL_OVERLAY)
            self.click_and_wait_element(self.locators.ORDER_LENTA_BUTTON)
        except TimeoutException:
            pass

    @allure.title('Клик по заказу в ленте')
    def click_order(self):
        try:
            self.click_and_wait_element(self.locators.ORDER_LINK)
        except TimeoutException:
            print("Заказ не кликабелен")

    @allure.title('Список заказа не пустой')
    def test_order_not_empty(self):
        try:
            ul_element = self.wait_for_visible(self.locators.DETAILS_ORDER)
            items = self.find_all(self.locators.ELEMENT_ORDER)
            return ul_element.is_displayed() and len(items) > 0
        except TimeoutException:
            return False

    @allure.title('Клик по разделу "Конструктор"')
    def click_constructor(self):
        try:
            self.click_and_wait_element(self.locators.CONSTRUCT_BUTTON)
        except TimeoutException:
            print("Кнопка 'Конструктор' не кликабельна")

    @allure.title('Проверка, открыто ли модальное окно заказа')
    def order_modal_window_is_visible(self):
        try:
            # ждём появления окна в DOM
            self.wait_for_condition(
                lambda d: d.find_element(*self.locators.MODAL_ORDER_NUMBER),
                timeout=10
            )
            return True
        except TimeoutException:
            return False


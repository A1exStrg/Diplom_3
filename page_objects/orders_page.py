from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from page_objects.base_page import BasePage
from locators import Locators
import allure

class OrdersPage(BasePage):
    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver, timeout=timeout)
        self.locators = Locators()

    @allure.title('Получить элементы истории заказов')
    def get_history_order_items(self):
        def _collect():
            try:
                elems = self.wait_for_condition(
                    lambda d: d.find_elements(*self.locators.ORDER_HISTORY_ITEMS),
                    timeout=10
                )
                return [el.text for el in elems]
            except StaleElementReferenceException:
                return _collect()
        return _collect()

    @allure.title('Получить список заказов на странице')
    def get_order_list(self):
        def _collect():
            try:
                elems = self.wait_for_condition(
                    lambda d: d.find_elements(*self.locators.ORDER_ITEMS),
                    timeout=10
                )
                return [el.text for el in elems]
            except StaleElementReferenceException:
                return _collect()
        return _collect()

    @allure.title('Получить номер текущего заказа')
    def get_current_order_number(self):
        try:
            el = self.wait_for_condition(
                lambda d: d.find_element(*self.locators.MODAL_ORDER_NUMBER),
                timeout=10
            )
            num = el.text.strip()
            if num.isdigit() and int(num) != 9999:
                return num
            return ""
        except TimeoutException:
            return ""

    @allure.title('Закрыть окно деталей заказа')
    def close_modal_window(self):
        try:
            close_button = self.wait_for_condition(
                lambda d: EC.element_to_be_clickable(self.locators.CLOSE_MODAL_WINDOW_OF_ORDER)(d),
                timeout=10
            )
            try:
                close_button.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", close_button)
        except TimeoutException:
            pass

    @allure.title('Получить общее число выполненных заказов (за всё время)')
    def get_completed_orders_all_time(self):
        try:
            element = self.wait_for_condition(
                lambda d: EC.visibility_of_element_located(self.locators.COMPLETED_ALL_TIME_TEXT)(d),
                timeout=10
            )
            text_value = element.text.strip()
            return int(text_value.replace(" ", "")) if text_value.isdigit() or text_value.replace(" ",
                                                                                                  "").isdigit() else None
        except TimeoutException:
            print("[ERROR] Элемент 'Выполнено за все время' не найден")
            return None

    @allure.title('Получить число выполненных заказов за сегодня')
    def get_complete_orders_today(self):
        try:
            element = self.wait_for_condition(
                lambda d: d.find_element(*self.locators.COMPLETED_TODAY_TEXT),
                timeout=10
            )
            return int(element.text.strip())
        except Exception as e:
            print("Счётчик 'Выполнено за сегодня' не найден:", e)
            return 0

    @allure.title('Получить количество заказов "в работе"')
    def get_orders_in_work(self):
        try:
            # Ждём исчезновения текста "В работе"
            self.wait_for_condition(
                lambda d: EC.invisibility_of_element_located(self.locators.WORK_IN_PROGRESS_TEXT)(d),
                timeout=10
            )
            # Ждём появления номеров заказов
            self.wait_for_condition(
                lambda d: d.find_elements(*self.locators.WORK_IN_PROGRESS_ORDER_NUMBER),
                timeout=10
            )
            orders = self.find_all(self.locators.WORK_IN_PROGRESS_ORDER_NUMBER)
            nums = [o.text.strip().zfill(7) for o in orders if o.text.strip().isdigit()]
            return len(set(nums))
        except TimeoutException:
            return 0

from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.base_page import BasePage
from locators import Locators

class OrdersPage(BasePage):
    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver, timeout=timeout)
        self.locators = Locators()

    """"Получить элементы истории заказов"""""
    def get_history_order_items(self):
        wait_driver = WebDriverWait(self.driver, 10)
        def _collect():
            try:
                elems = wait_driver.until(EC.presence_of_all_elements_located(self.locators.ORDER_HISTORY_ITEMS))
                return [el.text for el in elems]
            except StaleElementReferenceException:
                return _collect()
        return _collect()

    """Получить список заказов на странице"""
    def get_order_list(self):
        wait = WebDriverWait(self.driver, 10)
        def _collect():
            try:
                elems = wait.until(EC.presence_of_all_elements_located(self.locators.ORDER_ITEMS))
                return [el.text for el in elems]
            except StaleElementReferenceException:
                return _collect()
        return _collect()

    """Получить номер текущего заказа"""
    def get_current_order_number(self):
        try:
            el = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.locators.MODAL_ORDER_NUMBER))
            num = el.text.strip()
            if num.isdigit() and int(num) != 9999:
                return num
            return ""
        except TimeoutException:
            return ""

    """Закрыть окно деталей заказа"""""
    def close_modal_window(self):
        try:
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.locators.CLOSE_MODAL_WINDOW_OF_ORDER))
            try:
                close_button.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", close_button)
        except TimeoutException:
            pass

    """Получить общее число выполненных заказов (за всё время)"""
    def get_completed_orders_all_time(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.locators.COMPLETED_ALL_TIME_TEXT)
            )
            text_value = element.text.strip()
            print(f"[DEBUG] Completed all time raw text: {text_value}")  # для отладки
            return int(text_value.replace(" ", "")) if text_value.isdigit() or text_value.replace(" ",
                                                                                                  "").isdigit() else None
        except TimeoutException:
            print("[ERROR] Элемент 'Выполнено за все время' не найден")
            return None

    """Получить число выполненных заказов за сегодня"""
    def get_complete_orders_today(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.locators.COMPLETED_TODAY_TEXT))
            return int(element.text.strip())
        except Exception as e:
            print("Счётчик 'Выполнено за сегодня' не найден:", e)
            return 0

    """Получить количество заказов 'в работе'"""
    def get_orders_in_work(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.locators.WORK_IN_PROGRESS_TEXT))
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.locators.WORK_IN_PROGRESS_ORDER_NUMBER))
            orders = self.driver.find_elements(*self.locators.WORK_IN_PROGRESS_ORDER_NUMBER)
            nums = [o.text.strip().zfill(7) for o in orders if o.text.strip().isdigit()]
            return len(set(nums))
        except TimeoutException:
            return 0

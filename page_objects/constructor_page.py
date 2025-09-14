# import allure
# from selenium.common import NoSuchElementException, TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from page_objects.base_page import BasePage
# from locators import Locators
#
# class ConstructorPage(BasePage):
#     def __init__(self, driver, timeout: int = 10):
#         super().__init__(driver, timeout=timeout)
#         self.locators = Locators()
#
#     @allure.title('Клик по ингредиенту')
#     def click_on_ingredient(self):
#         try:
#             ing = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.locators.INGREDIENT))
#             ing.click()
#         except TimeoutException:
#             print("Ингредиент не кликабелен")
#
#     @allure.title('Проверить, что модальное окно ингредиента видно')
#     def ingredient_modal_window_is_visible(self):
#         try:
#             return self.driver.find_element(*self.locators.DETAIL_WINDOW_IS_OPEN).is_displayed()
#         except NoSuchElementException:
#             return False
#
#     @allure.title('Закрыть модальное окно (крестик)')
#     def close_modal_window_cross(self):
#         try:
#             cross_button = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable(self.locators.CLOSE_DETAIL_WINDOW_BUTTON))
#             try:
#                 cross_button.click()
#             except Exception:
#                 self.driver.execute_script("arguments[0].click();", cross_button)
#         except TimeoutException:
#             print("Кнопка 'Крестик' закрытия модалки не кликабельна")
#
#     @allure.title('Проверить, что модалка ингредиента закрыта')
#     def ingredient_modal_window_is_close(self):
#         try:
#             return not self.driver.find_element(*self.locators.DETAIL_WINDOW_IS_CLOSE).is_displayed()
#         except NoSuchElementException:
#             return True
#
#     @allure.title('Получить значение счётчика ингредиента {counter_locator}')
#     def get_ingredient_counter_value(self, counter_locator):
#         try:
#             el = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(counter_locator))
#             return el.text.strip()
#         except TimeoutException:
#             print(f"Не найден счётчик {counter_locator}")
#             return None
#         except NoSuchElementException:
#             return None
#
#     @allure.title('Перетащить ингредиент {ingredient_locator} в {target_locator}')
#     def move_ingredient(self, ingredient_locator, target_locator):
#         try:
#             ingredient = self.driver.find_element(*ingredient_locator)
#             order = self.driver.find_element(*target_locator)
#             WebDriverWait(self.driver, 10).until(EC.visibility_of(ingredient))
#             WebDriverWait(self.driver, 10).until(EC.visibility_of(order))
#             self.driver.execute_script("""
#                 var dataTransfer = { data: {} };
#                 var dragStartEvent = new MouseEvent('dragstart', {bubbles:true, cancelable:true});
#                 var dropEvent = new MouseEvent('drop', {bubbles:true, cancelable:true});
#                 var dragEndEvent = new MouseEvent('dragend', {bubbles:true, cancelable:true});
#                 arguments[0].dispatchEvent(dragStartEvent);
#                 arguments[1].dispatchEvent(dropEvent);
#                 arguments[0].dispatchEvent(dragEndEvent);
#             """, ingredient, order)
#         except Exception:
#             print("Не удалось перетащить ингредиент")
#
#     @allure.title('Ожидать обновления счётчика {counter_locator} от {initial_count} до +1')
#     def wait_for_counter_update(self, counter_locator, initial_count):
#         try:
#             new_count = str(int(initial_count) + 1)
#             WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(counter_locator, new_count))
#         except Exception:
#             print("Счётчик не обновился")
#
#     @allure.title('Клик по кнопке "Оформить заказ"')
#     def click_place_an_order_button(self):
#         try:
#             order_button = self.driver.find_element(*self.locators.ORDER_BUTTON)
#             if self.driver.capabilities.get('browserName', '').lower() == 'firefox':
#                 self.driver.execute_script("arguments[0].click();", order_button)
#             else:
#                 order_button.click()
#         except Exception:
#             print("Кнопка заказа не нажалась")


import allure
from selenium.common import NoSuchElementException
from page_objects.base_page import BasePage
from locators import Locators


class ConstructorPage(BasePage):
    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver, timeout=timeout)
        self.locators = Locators()

    @allure.title('Клик по ингредиенту')
    def click_on_ingredient(self):
        self.click(self.locators.INGREDIENT)

    @allure.title('Проверить, что модальное окно ингредиента видно')
    def ingredient_modal_window_is_visible(self):
        return self.is_visible(self.locators.DETAIL_WINDOW_IS_OPEN)

    @allure.title('Закрыть модальное окно (крестик)')
    def close_modal_window_cross(self):
        self.click(self.locators.CLOSE_DETAIL_WINDOW_BUTTON)

    @allure.title('Проверить, что модалка ингредиента закрыта')
    def ingredient_modal_window_is_close(self):
        return self.is_not_visible(self.locators.DETAIL_WINDOW_IS_CLOSE)

    @allure.title('Получить значение счётчика ингредиента {counter_locator}')
    def get_ingredient_counter_value(self, counter_locator):
        try:
            el = self.wait_for_visible(counter_locator)
            return el.text.strip()
        except Exception:
            print(f"Не найден счётчик {counter_locator}")
            return None

    @allure.title('Перетащить ингредиент {ingredient_locator} в {target_locator}')
    def move_ingredient(self, ingredient_locator, target_locator):
        try:
            ingredient = self.find(ingredient_locator)
            order = self.find(target_locator)
            # ждём видимости
            self.wait_for_visible(ingredient_locator)
            self.wait_for_visible(target_locator)
            # эмуляция drag-n-drop
            self.driver.execute_script("""
                var dataTransfer = { data: {} };
                var dragStartEvent = new MouseEvent('dragstart', {bubbles:true, cancelable:true});
                var dropEvent = new MouseEvent('drop', {bubbles:true, cancelable:true});
                var dragEndEvent = new MouseEvent('dragend', {bubbles:true, cancelable:true});
                arguments[0].dispatchEvent(dragStartEvent);
                arguments[1].dispatchEvent(dropEvent);
                arguments[0].dispatchEvent(dragEndEvent);
            """, ingredient, order)
        except Exception:
            print("Не удалось перетащить ингредиент")

    @allure.title('Ожидать обновления счётчика {counter_locator} от {initial_count} до +1')
    def wait_for_counter_update(self, counter_locator, initial_count):
        new_count = str(int(initial_count) + 1)
        return self.wait_for_text(counter_locator, new_count)

    @allure.title('Клик по кнопке "Оформить заказ"')
    def click_place_an_order_button(self):
        try:
            order_button = self.find(self.locators.ORDER_BUTTON)
            if self.driver.capabilities.get('browserName', '').lower() == 'firefox':
                self.driver.execute_script("arguments[0].click();", order_button)
            else:
                order_button.click()
        except Exception:
            print("Кнопка заказа не нажалась")

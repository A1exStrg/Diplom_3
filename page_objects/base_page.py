from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    """находим и кликаем по элементу"""
    def click_and_wait_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except Exception:
            print("Не удалось кликнуть по элементу")

    """Ввод значения"""
    def send_keys(self,locator, text):
        try:
            field = self.wait.until(EC.visibility_of_element_located(locator))
            field.clear()
            field.send_keys(text)
        except Exception:
            print("Ошибка при вводе значения")

    # """Получение текста элемента"""
    # def get_text(self, locator):
    #     try:
    #         return self.wait.until(EC.visibility_of_element_located(locator)).text
    #     except Exception:
    #         return None


    # """Наличие элемента на странице"""
    # def is_element_present(self, locator, wait=False):
    #     try:
    #         if wait:
    #             self.wait.until(EC.presence_of_element_located(locator))
    #         else:
    #             self.driver.find_element(*locator)
    #         return True
    #     except (NoSuchElementException, TimeoutException):
    #         return False

    # """Общий метод для ожидания и клика по элементу"""
    # def click_element(self, locator, timeout=10):
    #     try:
    #         WebDriverWait(self.driver, timeout).until(
    #             EC.visibility_of_element_located(locator)
    #         )
    #         element = self.driver.find_element(*locator)
    #         element.click()
    #     except Exception as e:
    #         print(f"Не удалось кликнуть по элементу: {e}")

    """Ожидание загрузки"""
    def wait_for_url_contains(self, substring, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: substring in d.current_url
            )
            return True
        except TimeoutException:
            print(f"URL не содержит '{substring}' в течение {timeout} сек. "
                  f"Текущий: {self.driver.current_url}")
            return False

    # def get_text_safe(self, locator, timeout=7):
    #     wait = WebDriverWait(self.driver, timeout)
    #
    #     def _get(d):
    #         el = d.find_element(*locator)
    #         return el.text
    #
    #     return wait.until(lambda d: _get(d))
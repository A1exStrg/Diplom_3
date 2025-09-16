from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element

    def is_visible(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except:
            return False

    def is_not_visible(self, locator):
        try:
            WebDriverWait(self.driver, self.timeout).until_not(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def wait_for_visible(self, locator):
        """Ждать появления элемента и вернуть его"""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_text(self, locator, text):
        """Ждать появления текста внутри элемента"""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def click_and_wait_element(self, locator):
        """Кликнуть и дождаться кликабельности элемента"""
        return self.click(locator)

    def wait_for_url_contains(self, url_part: str):
        """Ждать, пока URL будет содержать часть строки"""
        WebDriverWait(self.driver, self.timeout).until(
            EC.url_contains(url_part)
        )
        return self.driver.current_url

    def wait_for_condition(self, condition, timeout=5):
        return WebDriverWait(self.driver, timeout).until(condition)


    """Добавлено новое"""

    def wait_for_invisibility(self, locator):
        """Ждать исчезновения элемента"""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def get_browser_name(self):
        """Возвращает имя браузера (chrome, firefox и т.д.)"""
        return self.driver.capabilities.get('browserName', '').lower()

    def js_click(self, element):
        """Клик по элементу через JavaScript"""
        self.driver.execute_script("arguments[0].click();", element)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

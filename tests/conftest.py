import pytest
from selenium import webdriver
from page_objects.orders_page import OrdersPage
from page_objects.stellar_burger_page import Stellar_burger_page
from page_objects.constructor_page import ConstructorPage
from page_objects.login_page import LoginPage
from url import stellar_burgers_base_url_page
from data.user_data import user_creds as creds


class BrowserLauncher:
    @staticmethod
    def launch(browser: str):
        browser = browser.strip().lower()
        if browser == "chrome":
            opts = webdriver.ChromeOptions()
            opts.add_argument("--start-maximized")
            return webdriver.Chrome(options=opts)
        elif browser == "firefox":
            opts = webdriver.FirefoxOptions()
            return webdriver.Firefox(options=opts)
        else:
            raise RuntimeError(f"Указан неподдерживаемый браузер: {browser}. Используйте: chrome или firefox.")


@pytest.fixture(params=["chrome", "firefox"], scope="function")
def driver(request):
    browser_choice = request.param
    browser = BrowserLauncher.launch(browser_choice)
    browser.get(stellar_burgers_base_url_page)

    yield browser
    browser.quit()

@pytest.fixture
def login(driver, user_creds):
    main_page = Stellar_burger_page(driver)
    login_page = LoginPage(driver)

    email = user_creds["email"]
    password = user_creds["password"]

    main_page.click_on_personal_cabinet()
    login_page.send_email_to_input2(email)
    login_page.send_password_to_input2(password)
    main_page.click_login_button()
    return main_page, login_page

@pytest.fixture
def create_order(driver, login):
    def create_order():
        main_page = Stellar_burger_page(driver)
        main_page, login_page = login
        constr_page = ConstructorPage(driver)
        order_page = OrdersPage(driver)

        current_browser = driver.capabilities.get('browserName', '').lower()
        if current_browser != 'firefox':
            main_page.click_constructor()

        start_counter_value = constr_page.get_ingredient_counter_value(main_page.locators.INGREDIENT_COUNTER)
        constr_page.move_ingredient(main_page.locators.INGREDIENT, main_page.locators.ORDER_AREA)
        constr_page.wait_for_counter_update(main_page.locators.INGREDIENT_COUNTER, start_counter_value)
        constr_page.click_place_an_order_button()

        main_page.wait_for_condition(
            lambda drv: main_page.order_modal_window_is_visible() and order_page.get_current_order_number() != "",
            timeout=5
        )
        return order_page.get_current_order_number()
    return create_order


@pytest.hookimpl(tryfirst=True)
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Браузер: chrome, firefox")

@pytest.fixture(scope="session")
def user_creds():
    return creds

@pytest.fixture
def create_order2(driver, login):
    main_page = Stellar_burger_page(driver)
    constr_page = ConstructorPage(driver)

    # получаем стартовое значение каунтера
    start_counter_value = constr_page.get_ingredient_counter_value(main_page.locators.INGREDIENT_COUNTER)

    # добавляем ингредиент
    constr_page.move_ingredient(main_page.locators.INGREDIENT, main_page.locators.ORDER_AREA)

    # ждём обновления счётчика
    constr_page.wait_for_counter_update(main_page.locators.INGREDIENT_COUNTER, start_counter_value)

    # возвращаем старое и новое значение
    new_count = constr_page.get_ingredient_counter_value(main_page.locators.INGREDIENT_COUNTER)
    return start_counter_value, new_count
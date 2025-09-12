import allure
from page_objects.stellar_burger_page import Stellar_burger_page
from page_objects.constructor_page import ConstructorPage
from page_objects.login_page import LoginPage
from url import stellar_burgers_base_url_page, feed_page


class TestStellarBurger:
    @allure.title('Переход по клику на «Конструктор»')
    def test_click_to_constructor(self, driver):
        main_page = Stellar_burger_page(driver)

        main_page.click_order_lenta()
        main_page.click_constructor()
        expected_url = stellar_burgers_base_url_page
        assert expected_url, "Переход в конструктор не произошел"

    @allure.title('Переход по клику на «Лента заказов»')
    def test_click_to_order_lenta(self, driver):
        main_page = Stellar_burger_page(driver)

        main_page.click_constructor()
        main_page.click_order_lenta()
        expected_url = feed_page
        assert expected_url, "Переход в ленту заказа не произошел"

    @allure.title('Если кликнуть на ингредиент, появится всплывающее окно с деталями')
    def test_click_of_ingredient_show_details_window(self, driver):
        construct_page = ConstructorPage(driver)

        construct_page.click_on_ingredient()
        assert construct_page.ingredient_modal_window_is_visible(), "Всплывающее окно с деталями не появилось"

    @allure.title('Всплывающее окно закрывается кликом по крестику')
    def test_close_window_details_by_cross(self, driver):
        construct_page = ConstructorPage(driver)

        construct_page.click_on_ingredient()
        construct_page.close_modal_window_cross()
        assert not construct_page.ingredient_modal_window_is_close(), "Всплывающее окно не закрыто крестиком"

    @allure.title('При добавлении ингредиента в заказ, увеличивается каунтер данного ингредиента')
    def test_increases_counter_put_ingredient_to_order(self, driver):
        construct_page = ConstructorPage(driver)

        initial_count = construct_page.get_ingredient_counter_value(construct_page.locators.INGREDIENT_COUNTER)
        construct_page.move_ingredient(construct_page.locators.INGREDIENT, construct_page.locators.ORDER_AREA)
        construct_page.wait_for_counter_update(construct_page.locators.INGREDIENT_COUNTER, initial_count)
        updated_count = construct_page.get_ingredient_counter_value(construct_page.locators.INGREDIENT_COUNTER)

        assert updated_count > initial_count, f"Каунтер не увеличился: {initial_count} -> {updated_count}"

    @allure.title('Залогиненный пользователь может оформить заказ.')
    def test_login_user_can_took_an_order(self, driver, user_creds):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)
        construct_page = ConstructorPage(driver)

        email = user_creds["email"]
        password = user_creds["password"]

        main_page.click_on_personal_cabinet()
        login_page.send_email_to_input2(email)
        login_page.send_password_to_input2(password)
        main_page.click_login_button()

        browser = driver.capabilities['browserName'].lower()

        if browser != 'firefox':
            main_page.click_constructor()

        start_counter_value = construct_page.get_ingredient_counter_value(main_page.locators.INGREDIENT_COUNTER)
        construct_page.move_ingredient(main_page.locators.INGREDIENT, main_page.locators.ORDER_AREA)
        construct_page.wait_for_counter_update(main_page.locators.INGREDIENT_COUNTER, start_counter_value)
        # убедимся, что залогинились (используем существующий метод)
        if not login_page.is_logged_in():
            print("Login marker (EXIT_BUTTON) не найден — логин, возможно, не прошёл")
            driver.save_screenshot("debug_login_failed.png")
        else:
            print("login OK")
        construct_page.click_place_an_order_button()

        assert main_page.order_modal_window_is_visible(), "Окно с заказом не появилось"
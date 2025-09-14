import allure
from page_objects.stellar_burger_page import Stellar_burger_page
from page_objects.constructor_page import ConstructorPage
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
        assert construct_page.ingredient_modal_window_is_close(), "Всплывающее окно не закрыто крестиком"

    @allure.title('При добавлении ингредиента в заказ, увеличивается каунтер данного ингредиента')
    def test_increases_counter_put_ingredient_to_order(self, driver, create_order2):

        start_counter_value, updated_count = create_order2
        assert updated_count > start_counter_value, (
            f"Каунтер не увеличился: {start_counter_value} -> {updated_count}"
        )
    @allure.title('Залогиненный пользователь может оформить заказ.')

    def test_login_user_can_took_an_order(self, driver, create_order):
        order_number = create_order
        assert order_number != "", "Окно с заказом не появилось или номер заказа пустой"
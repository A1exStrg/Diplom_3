import allure
from selenium.webdriver.support.wait import WebDriverWait
from page_objects.orders_page import OrdersPage
from page_objects.stellar_burger_page import Stellar_burger_page
from page_objects.constructor_page import ConstructorPage
from selenium.webdriver.support import expected_conditions as EC


class TestOrderLenta:
    @allure.title('Если кликнуть на заказ, откроется всплывающее окно с деталями')
    def test_details_order_after_click(self, driver):
        main_page = Stellar_burger_page(driver)

        main_page.click_order_lenta()
        main_page.click_order()
        main_page.order_modal_window_is_visible()

        assert main_page.order_modal_window_is_visible(), "Всплывающее окно не появилось"
        assert main_page.test_order_not_empty(),"Детали заказа не отобразились в окне"

    @allure.title('заказы пользователя из раздела «История заказов» отображаются на странице «Лента заказов')
    def test_user_orders_displaying_in_the_lenta_order(self, driver, create_order):
        main_page = Stellar_burger_page(driver)
        order_page = OrdersPage(driver)

        order_page.close_modal_window()
        main_page.click_on_personal_cabinet()
        main_page.open_order_history()
        history_orders = order_page.get_history_order_items()

        main_page.click_order_lenta()
        feed_orders = order_page.get_order_list()

        history_order_value = {order.split()[0] for order in history_orders}
        lenta_order_value = {order.split()[0] for order in feed_orders}

        assert history_order_value & lenta_order_value, "На странице ленты заказов нет заказов из раздела «История заказов»!"

    @allure.title('При создании нового заказа счётчик "Выполнено за всё время" увеличивается')
    def test_all_time_order_counter_is_increases(self, driver, login):
        main_page = Stellar_burger_page(driver)
        constr_page = ConstructorPage(driver)
        order_page = OrdersPage(driver)
        main_page, login_page = login

        main_page.click_order_lenta()
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((main_page.locators.MODAL_OVERLAY)))
        count_all_time_orders = order_page.get_completed_orders_all_time()
        assert isinstance(count_all_time_orders, int), "Не удалось прочитать initial_completed_today_count"

        main_page.click_constructor()

        start_counter_value = constr_page.get_ingredient_counter_value(main_page.locators.INGREDIENT_COUNTER)
        constr_page.move_ingredient(main_page.locators.INGREDIENT, main_page.locators.ORDER_AREA)
        constr_page.wait_for_counter_update(main_page.locators.INGREDIENT_COUNTER, start_counter_value)
        constr_page.click_place_an_order_button()

        WebDriverWait(main_page.driver, 10).until(
            lambda driver: main_page.order_modal_window_is_visible() and order_page.get_current_order_number() != "")

        order_page.close_modal_window()
        main_page.click_order_lenta()
        new_count_all_time_orders = order_page.get_completed_orders_all_time()

        assert int(new_count_all_time_orders) > int(count_all_time_orders), (
            f"Счётчик 'Выполнено за всё время' не увеличился "
            f"Начальное значение: {count_all_time_orders}, новое значение: {new_count_all_time_orders}"
        )

    @allure.title('При создании нового заказа счётчик "Выполнено за сегодня" увеличивается')
    def test_today_order_counter_is_increases(self, driver, login):
        main_page = Stellar_burger_page(driver)
        constr_page = ConstructorPage(driver)
        order_page = OrdersPage(driver)
        main_page, login_page = login

        main_page.click_order_lenta()
        today_count_orders = order_page.get_complete_orders_today()
        assert isinstance(today_count_orders, int), "Не удалось прочитать initial_completed_today_count"

        main_page.click_constructor()
        start_counter_value = constr_page.get_ingredient_counter_value(main_page.locators.INGREDIENT_COUNTER)
        constr_page.move_ingredient(main_page.locators.INGREDIENT, main_page.locators.ORDER_AREA)
        constr_page.wait_for_counter_update(main_page.locators.INGREDIENT_COUNTER, start_counter_value)
        constr_page.click_place_an_order_button()

        WebDriverWait(main_page.driver, 10).until(
            lambda driver: main_page.order_modal_window_is_visible() and order_page.get_current_order_number() != "")

        order_page.close_modal_window()
        main_page.click_order_lenta()
        new_count_today_orders = order_page.get_complete_orders_today()

        assert int(new_count_today_orders) > int(today_count_orders), (
            f"Счётчик 'Выполнено за сегодня' не увеличился"
            f"Начальное значение: {today_count_orders}, новое значение: {new_count_today_orders}"
        )

    @allure.title('После оформления заказа его номер появляется в разделе В работе.')
    def test_number_of_order_is_displaying_in_work(self, driver, login):
        main_page = Stellar_burger_page(driver)
        constr_page = ConstructorPage(driver)
        order_page = OrdersPage(driver)
        main_page, login_page = login

        main_page.click_order_lenta()
        orders_in_work = order_page.get_orders_in_work()

        main_page.click_constructor()
        start_counter_value = constr_page.get_ingredient_counter_value(main_page.locators.INGREDIENT_COUNTER)
        constr_page.move_ingredient(main_page.locators.INGREDIENT, main_page.locators.ORDER_AREA)
        constr_page.wait_for_counter_update(main_page.locators.INGREDIENT_COUNTER, start_counter_value)
        constr_page.click_place_an_order_button()

        WebDriverWait(main_page.driver, 10).until(
            lambda driver: main_page.order_modal_window_is_visible() and order_page.get_current_order_number() != "")
        order_page.close_modal_window()

        main_page.click_order_lenta()

        WebDriverWait(main_page.driver, 10).until(
            lambda driver: order_page.get_orders_in_work() > orders_in_work)

        orders_in_progress = order_page.get_orders_in_work()
        assert orders_in_progress > orders_in_work, (
            f"Количество заказов в работе не увеличилось. "
            f"Начальное значение: {orders_in_work}, "
            f"новое значение: {orders_in_progress}")
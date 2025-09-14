import allure
from page_objects.stellar_burger_page import Stellar_burger_page
from page_objects.login_page import LoginPage
from url import personal_profile_page, login_url_page



class TestPersonalCab:
    @allure.title('Переход в «Личный кабинет»')
    def test_go_to_personal_cabinet(self, driver, user_creds):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)

        email = user_creds["email"]
        password = user_creds["password"]

        with allure.step("Открываем личный кабинет и логинимся"):
            main_page.click_on_personal_cabinet()
            login_page.send_email_to_input2(email)
            login_page.send_password_to_input2(password)
            main_page.click_login_button()
            main_page.click_on_personal_cabinet()

        with allure.step("Проверяем URL личного кабинета"):
            main_page.wait_for_url_contains(personal_profile_page)
            assert personal_profile_page in driver.current_url, "Переход в личный кабинет не выполнен."

    @allure.title('Переход в раздел «История заказов»')
    def test_go_to_history_orders(self, driver, user_creds):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)

        email = user_creds["email"]
        password = user_creds["password"]

        with allure.step("Логинимся"):
            main_page.click_on_personal_cabinet()
            login_page.send_email_to_input2(email)
            login_page.send_password_to_input2(password)
            main_page.click_login_button()

        with allure.step("Открываем историю заказов"):
            main_page.click_on_personal_cabinet()
            main_page.open_order_history()

        with allure.step("Проверяем URL истории заказов"):
            assert "/account/order-history" in main_page.driver.current_url, "История заказов не открылась"

    @allure.title('Выход из аккаунта')
    def test_go_on_exit_button(self, driver, user_creds):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)

        email = user_creds["email"]
        password = user_creds["password"]

        with allure.step("Логинимся"):
            main_page.click_on_personal_cabinet()
            login_page.send_email_to_input2(email)
            login_page.send_password_to_input2(password)
            main_page.click_login_button()

        with allure.step("Проверяем, что перешли на страницу логина после выхода"):
            main_page.wait_for_url_contains(login_url_page)
            assert login_url_page in driver.current_url, "Не вышли из личного кабинета"

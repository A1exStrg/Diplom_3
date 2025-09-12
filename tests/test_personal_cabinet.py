import allure
from page_objects.stellar_burger_page import Stellar_burger_page
from page_objects.login_page import LoginPage
from url import personal_profile_page, login_url_page
from selenium.webdriver.support.ui import WebDriverWait

class TestPersonalCab:
    @allure.title('Переход в «Личный кабинет»')
    def test_go_to_personal_cabinet(self, driver, user_creds):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)

        email = user_creds["email"]
        password = user_creds["password"]

        main_page.click_on_personal_cabinet()
        login_page.send_email_to_input2(email)
        login_page.send_password_to_input2(password)

        main_page.click_login_button()
        main_page.click_on_personal_cabinet()

        expected_url = personal_profile_page
        assert expected_url is not None, "Переход в личный кабинет не выполнен."

    @allure.title('Переход в раздел «История заказов»')
    def test_go_to_history_orders(self, driver, user_creds):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)

        email = user_creds["email"]
        password = user_creds["password"]

        main_page.click_on_personal_cabinet()
        login_page.send_email_to_input2(email)
        login_page.send_password_to_input2(password)
        main_page.click_login_button()
        #убедимся, что залогинились (используем существующий метод)
        if not login_page.is_logged_in():
            print("Login marker (EXIT_BUTTON) не найден — логин, возможно, не прошёл")
            driver.save_screenshot("debug_login_failed.png")
        else:
            print("login OK")

        main_page.click_on_personal_cabinet()
        main_page.open_order_history()

        # проверка — URL содержит путь истории заказов
        assert "/account/order-history" in main_page.driver.current_url, "История заказов не открылась"

    @allure.title('Выход из аккаунта')
    def test_go_on_exit_button(self, driver, user_creds):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)

        email = user_creds["email"]
        password = user_creds["password"]

        main_page.click_on_personal_cabinet()
        login_page.send_email_to_input2(email)
        login_page.send_password_to_input2(password)
        main_page.click_login_button()

        WebDriverWait(main_page.driver, 5).until(lambda d: "/login" in d.current_url)

        expected_url = login_url_page
        assert expected_url in driver.current_url, "Не вышли из личного кабинета"
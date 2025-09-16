import allure
from page_objects.stellar_burger_page import Stellar_burger_page
from page_objects.login_page import LoginPage
from url import recover_password_page, reset_password_page


@allure.epic("Stellar Burgers — Восстановление пароля")
class TestRecoverPassword:
    @allure.title('Проверка перехода на страницу восстановления пароля по кнопке «Восстановить пароль»')
    def test_go_to_restore_password(self, driver):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)

        with allure.step("Открываем личный кабинет и кликаем 'Личный кабинет'"):
            main_page.click_on_personal_cabinet()

        with allure.step("Нажимаем ссылку 'Восстановить пароль'"):
            login_page.click_recover_password()

        with allure.step("Проверяем, что URL страницы содержит путь восстановления пароля"):
            main_page.wait_for_url_contains(recover_password_page)
            assert recover_password_page in driver.current_url

    @allure.title('Проверка ввода почты и клик по кнопке «Восстановить»')
    def test_restore_password_process(self, driver):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)

        with allure.step("Открываем страницу и переходим к восстановлению пароля"):
            main_page.click_on_personal_cabinet()
            login_page.click_recover_password()

        with allure.step("Вводим сгенерированный e-mail в поле и нажимаем 'Восстановить'"):
            login_page.send_email_to_input(login_page.locators.EMAIL_FIELD)
            login_page.click_recover_button()
            assert reset_password_page is not None

    @allure.title('Проверка клик по кнопке показать/скрыть пароль делает поле активным — подсвечивает его')
    def test_high_password(self, driver):
        main_page = Stellar_burger_page(driver)
        login_page = LoginPage(driver)

        main_page.click_on_personal_cabinet()
        login_page.click_recover_password()
        login_page.send_email_to_input(login_page.locators.EMAIL_FIELD)
        login_page.click_recover_button()

        login_page.click(login_page.locators.PASSWORD_FIELD)
        login_page.send_password_to_input(login_page.locators.PASSWORD_FIELD)

        login_page.click(login_page.locators.HIDE_GLASS)

        active_field = login_page.wait_for_visible(login_page.locators.HIDE_GLASS)

        assert active_field.get_attribute("class"), "Пароль не подсвечен"
        assert active_field.is_enabled(), "Пароль не активный"

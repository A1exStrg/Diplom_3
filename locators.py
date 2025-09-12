from selenium.webdriver.common.by import By


class Locators:
    # stellar_burger_page
    PERS_CABINET_BUTTON = (By.XPATH, "//p[@class='AppHeader_header__linkText__3q_va ml-2' and contains(., 'Личный Кабинет')]")
    RECOVER_PASS_BUTTON = (By.XPATH, "//a[text()='Восстановить пароль']")

    EMAIL_FIELD = (By.NAME, "name")
    RECOVER_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    RECOVER_PASS_TEXT = (By.XPATH, "//h2[text()='Восстановление пароля']")

    PASS_FIELD = (By.NAME, "Пароль")
    HIDE_GLASS = (By.XPATH, "//div[contains(@class, 'input__icon-action')]")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")



    PASS_VISIBLE = (By.XPATH, "//input[@type='text']")
    PASSWORD_FIELD = (By.XPATH, "//div[contains(@class, 'input_type_password')]/input[@type='password']")

    ZAKAZ_HISTORY_BUTTON = (By.XPATH, "//a[@href='/account/order-history']")
    REGISTER_LINK = (By.XPATH, "//a[text()='Зарегистрироваться']")

    NAME_FIELD = (By.XPATH, "//label[.='Имя']/..//input")
    REGISTER_BUTTON = (By.XPATH, "//button[text()='Зарегистрироваться']")
    EXIT_BUTTON = (By.XPATH, "//button[text()='Выход']")

    #лента заказов
    ORDER_LENTA_BUTTON = (By.XPATH, "//a[@href='/feed']//p[normalize-space(text())='Лента Заказов']")

    #первый заказ в ленте
    ORDER_LINK = (By.XPATH, "//a[contains(@href, '/feed/')]")
    DETAILS_ORDER = (By.CSS_SELECTOR, 'ul.Modal_list__2sHWc > li')

    #не загруз страницы
    DETAILS_ORDERS = (By.CSS_SELECTOR, '.Modal_modal_opened__3ISw4')
    ELEMENT_ORDER = (By.CSS_SELECTOR, '.Modal_listItem__3K1Kj')

    #кнопка конструктор
    CONSTRUCT_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    #первый ингридиент
    INGREDIENT = (By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6")
    #окно ингридиента открыто
    DETAIL_WINDOW_IS_OPEN = (By.CLASS_NAME, "Modal_modal_opened__3ISw4")
    # крестик закрыть окно ингридиента
    CLOSE_DETAIL_WINDOW_BUTTON = (By.CLASS_NAME, "Modal_modal__close__TnseK")
    # окно ингридиента закрыто
    DETAIL_WINDOW_IS_CLOSE = (By.CSS_SELECTOR, ".Modal_modal__P3_V5")

    INGREDIENT_COUNTER = (By.CSS_SELECTOR, ".BurgerConstructor_basket__totalContainer__2Z-ho p")
    #поле с добавленными ингридиентами
    ORDER_AREA = (By.CSS_SELECTOR, ".BurgerConstructor_basket__list__l9dp_")
    #кнопка оформить заказ
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")

    #надо найти после vpn
    ORDER_HISTORY_ITEMS = (By.CLASS_NAME, "OrderHistory_listItem__2x95r")
    ORDER_ITEMS = (By.CLASS_NAME, "OrderHistory_listItem__2x95r")

    #модальное окно идентификатора заказа
    MODAL_ORDER_NUMBER = (By.CSS_SELECTOR, "div.Modal_modal__container__Wo2l_ h2")
    # крестик закрыть окно заказа
    CLOSE_MODAL_WINDOW_OF_ORDER = (By.CSS_SELECTOR, "button.Modal_modal__close_modified__3V5XS")

    COMPLETED_ALL_TIME_TEXT = (
        By.XPATH,
        "//p[normalize-space(text())='Выполнено за все время:' or normalize-space(text())='Выполнено за всё время:']/following-sibling::p[1]")
    ORDER_FEED_TITLE = (By.XPATH, "//h1[normalize-space(text())='Лента заказов']")

    COMPLETED_TODAY_TEXT = (By.XPATH, "(//p[normalize-space(text())='Выполнено за сегодня:']/following::p[1])")

    WORK_IN_PROGRESS_TEXT = (By.XPATH, "//li[text()='Все текущие заказы готовы!']")
    WORK_IN_PROGRESS_ORDER_NUMBER = (By.XPATH, "//li[@class='text text_type_digits-default mb-2']")

    MODAL_OVERLAY = (By.CSS_SELECTOR, "div.Modal_modal_overlay__x2ZCr")



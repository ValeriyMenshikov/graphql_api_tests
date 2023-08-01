import allure

from generic.checkers.checkers import message_checker


@allure.suite("Тесты на проверку метода logout_all_account")
@allure.sub_suite("Позитивные проверки")
class TestLogoutAllAccountPositive:
    @allure.title("Проверка регистрации, авторизации и разлогина пользователя со всех устройств")
    def test_logout_all_account(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(login=login, email=email, password=password)
        access_token = logic.account_graphql.login_account(login=login, password=password).token
        logic.account_graphql.logout_all_account(access_token=access_token)


@allure.suite("Тесты на проверку метода logout_all_account")
@allure.sub_suite("Позитивные проверки")
class TestLogoutAllAccountNegative:
    @allure.title("Проверка регистрации, авторизации и разлогина пользователя со всех устройств c невалидным токеном")
    def test_logout_all_account_with_invalid_token(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(login=login, email=email, password=password)
        access_token = logic.account_graphql.login_account(login=login, password=password).token
        invalid_token = access_token + '1'
        with message_checker(error_message="Not authorized: ForgedToken"):
            logic.account_graphql.logout_all_account(access_token=invalid_token)

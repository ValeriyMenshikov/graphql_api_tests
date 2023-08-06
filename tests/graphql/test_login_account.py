import allure

from generic.checkers.checkers import message_checker


@allure.suite("Тесты на проверку метода login_account")
@allure.sub_suite("Позитивные проверки")
class TestLoginAccountPositive:
    @allure.title("Проверка регистрации и авторизации пользователя")
    def test_login_account(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(login=login, email=email, password=password)
        access_token = logic.provider.graphql.dm_api_account.login_account(login=login, password=password).token
        assert access_token, 'Пользователь смог авторизоваться'


@allure.suite("Тесты на проверку метода login_account")
@allure.sub_suite("Негативные проверки")
class TestLoginAccountNegative:
    @allure.title("Проверка регистрации и авторизации пользователя с невалидным паролем")
    def test_login_account_with_invalid_password(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(login=login, email=email, password=password)
        invalid_password = password + '1'
        with message_checker(error_message="The password is incorrect. Did you forget to switch the keyboard?"):
            logic.provider.graphql.dm_api_account.login_account(login=login, password=invalid_password)

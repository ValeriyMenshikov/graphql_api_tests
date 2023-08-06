import allure


@allure.suite("Тесты на проверку метода logout_account")
@allure.sub_suite("Позитивные проверки")
class TestLogoutAccountPositive:
    @allure.title("Проверка регистрации, авторизации и разлогина пользователя")
    def test_logout_account(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(login=login, email=email, password=password)
        access_token = logic.provider.graphql.dm_api_account.login_account(login=login, password=password).token
        response = logic.provider.graphql.dm_api_account.logout_account(access_token=access_token)

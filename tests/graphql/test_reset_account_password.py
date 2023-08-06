import allure


@allure.suite("Тесты на проверку метода reset_account_password")
@allure.sub_suite("Позитивные проверки")
class TestResetAccountPasswordPositive:
    @allure.title("Проверка сброса пароля")
    def test_reset_account_password(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(login=login, email=email, password=password)
        response = logic.provider.graphql.dm_api_account.reset_account_password(login=login, email=email)

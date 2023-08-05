import allure


@allure.suite("Тесты на проверку метода account_current")
@allure.sub_suite("Позитивные проверки")
class TestAccountCurrentPositive:
    @allure.title("Проверка регистрации, активации и получения информации о пользователе")
    def test_account_current(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(
            login=login,
            email=email,
            password=password
        )
        access_token = logic.provider.graphql.dm_api_account.login_account(
            login=login,
            password=password,
            remember_me=True
        ).token
        logic.provider.graphql.dm_api_account.account_current(access_token=access_token)

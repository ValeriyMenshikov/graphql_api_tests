import allure


@allure.suite("Тесты на проверку метода update_account")
@allure.sub_suite("Позитивные проверки")
class TestUpdateAccountPositive:
    @allure.title("Проверка изменения данных пользователя")
    def test_update_account(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(login=login, email=email, password=password)
        access_token = logic.provider.graphql.dm_api_account.login_account(login=login, password=password).token
        logic.provider.graphql.dm_api_account.update_account(access_token=access_token, name='Vasya')

import allure


@allure.suite("Тесты на проверку метода register_account")
@allure.sub_suite("Позитивные проверки")
class TestRegisterAccountPositive:
    @allure.title("Проверка регистрации пользователя")
    def test_register_user(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(login=login, email=email, password=password)

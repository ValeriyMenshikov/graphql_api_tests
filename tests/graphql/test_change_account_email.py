import allure


@allure.suite("Тесты на проверку метода change_account_email")
@allure.sub_suite("Позитивные проверки")
class TestChangeAccountEmailPositive:
    @allure.title("Проверка регистрации и смены email пользователя")
    def test_change_account_email(self, prepare_user, logic):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        logic.account_helper.register_account(login=login, email=email, password=password)
        new_email = 'new_' + email
        logic.account_graphql.change_account_email(login=login, password=password, email=new_email)

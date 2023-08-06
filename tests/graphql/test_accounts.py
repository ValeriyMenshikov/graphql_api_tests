import allure


@allure.suite("Тесты на проверку метода account")
@allure.sub_suite("Позитивные проверки")
class TestAccountsPositive:
    @allure.title("Проверка регистрации, активации и получения информации о пользователе")
    def test_accounts(self, logic):
        users_fields = ('user_id', 'email')
        paging_fields = ('total_pages_count', 'page_size')
        result = logic.provider.graphql.dm_api_account.accounts(
            users_fields=users_fields,
            paging_fields=paging_fields
        )

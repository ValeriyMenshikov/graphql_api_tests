import allure
from hamcrest import assert_that, has_properties

from modules.graphql.dm_api_account.schema import PagingResult


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
        assert_that(result.paging, has_properties(dict(page_size=10)))

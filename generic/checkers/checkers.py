from contextlib import contextmanager

from modules.graphql.dm_api_account.errors import GraphQLClientError
from hamcrest import assert_that, has_entries


@contextmanager
def message_checker(error_message):
    try:
        yield
        if error_message:
            raise AssertionError(f'Должно быть получено сообщение "{error_message}", но запрос прошел успешно!')
    except GraphQLClientError as err:
        for error in err.errors:
            assert_that(error, has_entries(
                dict(message=error_message)
            ))

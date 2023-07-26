from schema import dm_api_schema
from graphql_client.client import GraphQLClient


class AccountApi(GraphQLClient):
    def __init__(self):
        super().__init__()

    def register_user(self, request: dm_api_schema.RegistrationInput):
        query_request = self.mutation(name='registerAccount')
        query_request.register_account(registration=request)
        return self.request(query=query_request)


if __name__ == '__main__':
    request: dm_api_schema.RegistrationInput = dm_api_schema.RegistrationInput(
        login='book_title',
        email='book_author@mail.ru',
        password='book_author'
    )
    AccountApi().register_user(request=request)

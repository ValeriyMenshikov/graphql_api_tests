from schema import schema
from base_client import GraphQLClient


class AccountApi(GraphQLClient):
    def __init__(self):
        super().__init__()

    def register_user(self, request: schema.RegistrationInput):
        query_request = self.mutation(name='registerAccount')
        query_request.register_account(registration=request)
        return self.request(query=query_request)


if __name__ == '__main__':
    request: schema.RegistrationInput = schema.RegistrationInput(
        login='book_title',
        email='book_author@mail.ru',
        password='book_author'
    )
    AccountApi().register_user(request=request)

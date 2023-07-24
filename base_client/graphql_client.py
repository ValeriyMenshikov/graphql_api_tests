from typing import Any, Dict
from sgqlc.endpoint.http import HTTPEndpoint
from utils.utils import log_graphql_request
from sgqlc.operation import Operation
from schema import schema


class GraphQLClient:

    def __init__(
            self,
            service_name="http://localhost:5051/",
            endpoint="graphql/",
            disable_log: bool = False
    ):
        self.schema = schema
        self.disable_log = disable_log
        self.service_name = service_name
        self.endpoint = endpoint
        self._endpoint = HTTPEndpoint(self.service_name + self.endpoint, base_headers=self.authorize())

    @staticmethod
    def authorize() -> dict:
        """Headers to add to every request."""
        return {}

    @staticmethod
    def query(name: str) -> Operation:
        """Generate operation of type Query."""
        return Operation(schema.Query, name)

    @staticmethod
    def mutation(name: str) -> Operation:
        """Generate operation of type Mutation."""
        return Operation(schema.Mutation, name)

    @log_graphql_request
    def request(self, query: Operation) -> Dict[str, Any]:
        """Make a request."""
        return self._endpoint(query)


if __name__ == '__main__':
    client = GraphQLClient()
    # Создать мутацию add_book
    query_request = client.mutation(name='registerAccount')
    # Создать входные данные для запроса
    register_request = schema.RegistrationInput(
        login='book_title',
        email='book_author@mail.ru',
        password='book_author'
    )
    query_request.register_account(registration=register_request)
    client.request(query=query_request)

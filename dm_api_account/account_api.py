from schema.dm_api_schema import dm_api_schema, RegistrationInput, AccountRegisterResponse
from graphql_client.client import GraphQLClient


class GraphQLAccountApi:
    def __init__(
            self,
            service_name: str = '',
            endpoint: str = "graphql/",
            disable_log: bool = False,
            base_headers: dict = None
    ):
        self.client = GraphQLClient(
            service_name=service_name,
            endpoint=endpoint,
            disable_log=disable_log,
            base_headers=base_headers,
            schema=dm_api_schema
        )

    def register_user(self, login=None, email=None, password=None) -> AccountRegisterResponse:
        mutation_request = self.client.mutation(name='registerAccount')
        registration_input = RegistrationInput(
            login=login,
            email=email,
            password=password,
        )
        mutation_request.register_account(registration=registration_input)
        json_data = self.client.request(query=mutation_request)["data"]["registerAccount"]
        result = AccountRegisterResponse(json_data)
        return result

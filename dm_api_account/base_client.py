from typing import Any
from sgqlc.operation import Operation
from graphql_client.client import BaseGraphQLClient
from graphql_client.utils import log_graphql_request
from dm_api_account.schema import schema


class AccountClient(BaseGraphQLClient):
    service_name = 'http://5.63.153.31:5051'
    endpoint = "/graphql"

    def __init__(self, disable_log: bool = False):
        self.schema = schema
        self.disable_log = disable_log
        super().__init__()

    def authorize(self) -> dict:
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
    def request(self, query: Operation) -> dict[str, Any]:
        """Make a request."""
        return super().make_request(query)

from typing import Any, Dict
from sgqlc.endpoint.http import HTTPEndpoint
from graphql_client.utils import log_graphql_request
from sgqlc.operation import Operation
from sgqlc.types import Schema


class GraphQLClient:

    def __init__(
            self,
            schema: Schema,
            service_name: str,
            endpoint: str = "graphql/",
            disable_log: bool = False,
            base_headers: dict = None
    ):
        self.schema = schema
        self.disable_log = disable_log
        self.service_name = service_name
        self.endpoint = endpoint
        self._endpoint = HTTPEndpoint(self.service_name + self.endpoint)

        if base_headers:
            self._endpoint.base_headers = base_headers

    def set_headers(self, headers: dict) -> None:
        self._endpoint.base_headers = headers

    def query(self, name: str) -> Operation:
        return Operation(self.schema.Query, name)

    def mutation(self, name: str) -> Operation:
        return Operation(self.schema.Mutation, name)

    @log_graphql_request
    def request(self, query: Operation) -> Dict[str, Any]:
        return self._endpoint(query)

from commons.graphql_client.utils import log_graphql_request
from sgqlc.operation import Operation
from sgqlc.types import Schema
from sgqlc.endpoint.websocket import WebSocketEndpoint
from typing import Generator


class GraphQLWebSocketClient:

    def __init__(
            self,
            schema: Schema,
            service_name: str,
            endpoint: str = "/graphql",
            disable_log: bool = False,
            timeout: int = 10,
    ):
        self.schema = schema
        self.disable_log = disable_log
        self.service_name = service_name
        self.endpoint = endpoint
        self.web_socket = WebSocketEndpoint(url=self.service_name + self.endpoint, timeout=timeout)

    def subscription_operation(self) -> Operation:
        return Operation(self.schema.Subscription)

    def subscription(self, query) -> Generator:
        return self.web_socket(query)

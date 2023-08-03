import json

from websocket import WebSocketTimeoutException

from commons.graphql_client.web_socket import GraphQLWebSocketClient
from modules.graphql.dm_api_account.schema import schema, LoginEvent


class GraphQLWebSocketAccountApi:
    def __init__(
            self,
            service_name: str = '',
            endpoint: str = "/graphql/",
            disable_log: bool = False,
            # allure_attach: bool = True,
            timeout: int = 10,
    ):
        self.client = GraphQLWebSocketClient(
            service_name=service_name,
            endpoint=endpoint,
            disable_log=disable_log,
            timeout=timeout,
            schema=schema
        )
        self.messages = []

    def user_login_subscription(self) -> LoginEvent:
        subscription = self.client.subscription_operation()
        subscription.user_login()
        try:
            for message in self.client.subscription(query=subscription):
                model = LoginEvent(message['data']['userLogin'])
                self.messages.append(model)
                return model
        except WebSocketTimeoutException:
            raise AssertionError('Сообщение не было найдено!')

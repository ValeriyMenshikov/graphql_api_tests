from functools import cached_property
from modules.graphql.dm_api_account.client import GraphQLAccountApi
from modules.graphql.dm_api_account.ws_client import GraphQLWebSocketAccountApi
from vyper import v


class GraphQLConnector:

    @cached_property
    def dm_api_account(self) -> GraphQLAccountApi:
        return GraphQLAccountApi(service_name=v.get('service.dm_api_account_graphql'))

    @cached_property
    def dm_api_account_ws(self) -> GraphQLWebSocketAccountApi:
        return GraphQLWebSocketAccountApi(service_name=v.get('service.dm_api_account_graphql_ws'))

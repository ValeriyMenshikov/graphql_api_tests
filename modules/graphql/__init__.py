from functools import cached_property
from modules.graphql.dm_api_account.client import GraphQLAccountApi
from config.config import Config


class GraphQLConnector:

    @cached_property
    def dm_api_account(self) -> GraphQLAccountApi:
        return GraphQLAccountApi(service_name=Config.dm_api_account_graphql)
